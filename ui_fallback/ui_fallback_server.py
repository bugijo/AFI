#!/usr/bin/env python3
"""Lightweight fallback UI server for AFI."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from environment import load_settings
from editor_video import executar_modo_simulado

UI_DIR = Path(__file__).parent


class FallbackHandler(SimpleHTTPRequestHandler):
    settings = load_settings()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def _send_json(self, payload: dict[str, object], status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _list_output(self) -> list[dict[str, object]]:
        entries: list[dict[str, object]] = []
        for item in sorted(self.settings.output_dir.glob("*")):
            if item.is_file():
                stat = item.stat()
                entries.append(
                    {
                        "name": item.name,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    }
                )
        return entries

    def _latest_log(self) -> dict[str, object]:
        log_dir = self.settings.log_dir
        if not log_dir.exists():
            return {"file": None, "content": ""}

        latest = max(
            (f for f in log_dir.glob("*.log") if f.is_file()),
            default=None,
            key=lambda f: f.stat().st_mtime,
        )
        if not latest:
            return {"file": None, "content": ""}

        try:
            content = latest.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = latest.read_text(errors="ignore")
        return {"file": latest.name, "content": content[-4000:]}

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            payload = {
                "no_deps_mode": self.settings.no_deps,
                "input_dir": str(self.settings.input_dir),
                "output_dir": str(self.settings.output_dir),
                "log_dir": str(self.settings.log_dir),
                "output_count": len(self._list_output()),
            }
            self._send_json(payload)
            return

        if parsed.path == "/api/output":
            self._send_json({"files": self._list_output()})
            return

        if parsed.path == "/api/log":
            query = parse_qs(parsed.query)
            response = self._latest_log()
            if "file" in query:
                requested = (self.settings.log_dir / query["file"][0]).resolve()
                if requested.is_file():
                    response = {
                        "file": requested.name,
                        "content": requested.read_text(errors="ignore")[-4000:],
                    }
            self._send_json(response)
            return

        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/generate_dummy":
            executar_modo_simulado()
            self._send_json({"status": "ok"})
            return

        self.send_error(404, "Endpoint nao encontrado")


def serve(host: str, port: int) -> None:
    server = ThreadingHTTPServer((host, port), FallbackHandler)
    print(f"Fallback UI em http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Encerrando servidor fallback...")
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Servidor HTTP fallback para a UI")
    parser.add_argument("--host", default="127.0.0.1", help="Interface para escutar (padrao 127.0.0.1)")
    parser.add_argument("--port", type=int, default=load_settings(create_dirs=False).port, help="Porta para o servidor")
    args = parser.parse_args(argv)
    serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

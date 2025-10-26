#!/usr/bin/env python3
"""Convenient local preview server for the Sintaxe Digital landing page."""

from __future__ import annotations

import argparse
import http.server
import socket
import sys
import threading
import webbrowser
from functools import partial
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve the landing page locally and open it in a browser."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the preview server on (default: 8000).",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open the browser after starting the server.",
    )
    return parser.parse_args()


def ensure_port_available(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError as exc:
            raise OSError(
                f"Port {port} is already in use. Specify a different port with --port."
            ) from exc


def main() -> None:
    args = parse_args()

    try:
        ensure_port_available(args.port)
    except OSError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    base_dir = Path(__file__).resolve().parent
    handler_cls = partial(http.server.SimpleHTTPRequestHandler, directory=str(base_dir))
    server = http.server.ThreadingHTTPServer(("0.0.0.0", args.port), handler_cls)

    url = f"http://127.0.0.1:{args.port}/index.html"
    print(f"Serving Sintaxe Digital preview at {url}")
    print("The page will open in your default browser automatically.")
    print("Press CTRL+C here to stop the preview server when you're done.")

    if not args.no_browser:
        threading.Timer(1.0, webbrowser.open, args=(url,)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down preview server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

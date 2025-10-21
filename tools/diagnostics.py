#!/usr/bin/env python3
"""Quick diagnostics helper for the AFI offline bundle."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from datetime import datetime
from pathlib import Path

from environment import ROOT_DIR, load_settings


def _detect_ffmpeg(ffmpeg_dir: Path) -> str | None:
    if not ffmpeg_dir.exists():
        return None

    for candidate in ffmpeg_dir.rglob("ffmpeg*"):
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def _dir_summary(path: Path) -> dict[str, int]:
    files = 0
    total_size = 0
    if path.exists():
        for entry in path.rglob("*"):
            if entry.is_file():
                files += 1
                try:
                    total_size += entry.stat().st_size
                except OSError:
                    continue
    return {"files": files, "size_bytes": total_size}


def gather_diagnostics() -> dict[str, object]:
    settings = load_settings()
    ffmpeg_binary = _detect_ffmpeg(settings.ffmpeg_dir)

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "platform": platform.platform(),
        "python": sys.version,
        "python_executable": sys.executable,
        "no_deps_mode": settings.no_deps,
        "paths": {
            "root": str(settings.input_dir.parent.parent),
            "input": str(settings.input_dir),
            "output": str(settings.output_dir),
            "logs": str(settings.log_dir),
            "knowledge_base": str(settings.knowledge_base_dir),
            "third_party": str(settings.third_party_dir),
            "ffmpeg_dir": str(settings.ffmpeg_dir),
        },
        "ffmpeg_binary": ffmpeg_binary,
        "disk_usage": {
            "input": _dir_summary(settings.input_dir),
            "output": _dir_summary(settings.output_dir),
            "logs": _dir_summary(settings.log_dir),
            "knowledge_base": _dir_summary(settings.knowledge_base_dir),
        },
        "shutil_available": hasattr(shutil, "copy2"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AFI diagnostics reporter")
    parser.add_argument("--json", action="store_true", help="Emit diagnostics as JSON instead of text.")
    args = parser.parse_args(argv)

    data = gather_diagnostics()

    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print("AFI diagnostics")
    print("-" * 40)
    print(f"Timestamp:       {data['timestamp']}")
    print(f"Platform:        {data['platform']}")
    print(f"Python:          {data['python']}")
    print(f"Executable:      {data['python_executable']}")
    print(f"NO_DEPS mode:    {data['no_deps_mode']}")
    print(f"Input dir:       {data['paths']['input']}")
    print(f"Output dir:      {data['paths']['output']}")
    print(f"Logs dir:        {data['paths']['logs']}")
    print(f"Knowledge base:  {data['paths']['knowledge_base']}")
    print(f"FFmpeg dir:      {data['paths']['ffmpeg_dir']}")
    print(f"FFmpeg binary:   {data['ffmpeg_binary'] or 'not found'}")
    print("-" * 40)
    print("Directory usage (files, size bytes)")
    for label, summary in data["disk_usage"].items():
        print(f"  {label:<14} {summary['files']:>5} files, {summary['size_bytes']:>10} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

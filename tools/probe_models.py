#!/usr/bin/env python3
"""Probes optional ML dependencies to report availability."""

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path

from environment import load_settings

DEFAULT_MODULES = (
    "llama_index",
    "sentence_transformers",
    "torch",
    "transformers",
)


def check_module(name: str) -> bool:
    try:
        importlib.import_module(name)
        return True
    except Exception:
        return False


def summarize_models(modules: tuple[str, ...] = DEFAULT_MODULES) -> dict[str, bool]:
    return {name: check_module(name) for name in modules}


def knowledge_base_snapshot(root: Path) -> list[str]:
    if not root.exists():
        return []
    entries: list[str] = []
    for item in sorted(root.rglob("*")):
        if item.is_file():
            entries.append(str(item.relative_to(root)))
    return entries


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Probe optional ML dependencies and knowledge base assets.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit results as JSON for automation.",
    )
    args = parser.parse_args(argv)

    settings = load_settings(create_dirs=False)
    modules = summarize_models()
    kb_files = knowledge_base_snapshot(settings.knowledge_base_dir)

    payload = {
        "no_deps_mode": settings.no_deps,
        "modules": modules,
        "knowledge_base_files": kb_files,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print("AFI model probe")
    print("-" * 32)
    print(f"NO_DEPS mode: {settings.no_deps}")
    print("Modules:")
    for name, available in payload["modules"].items():
        status = "ok" if available else "missing"
        print(f"  - {name}: {status}")
    print("-" * 32)
    print(f"Knowledge base ({len(kb_files)} arquivos)")
    for entry in kb_files[:10]:
        print(f"  - {entry}")
    if len(kb_files) > 10:
        print(f"  ... {len(kb_files) - 10} mais arquivo(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

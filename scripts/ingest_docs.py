#!/usr/bin/env python3
"""Utility to ingest documents into the AFI knowledge base."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from environment import load_settings

VALID_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}


def iter_sources(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return [item for item in path.rglob("*") if item.is_file()]


def should_copy(path: Path) -> bool:
    return path.suffix.lower() in VALID_EXTENSIONS


def ingest(source: Path, destination: Path) -> list[Path]:
    copied: list[Path] = []
    for item in iter_sources(source):
        if not should_copy(item):
            continue
        target = destination / item.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied.append(target)
    return copied


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest documents into the AFI knowledge base.")
    parser.add_argument("path", type=Path, help="File or directory to ingest.")
    args = parser.parse_args(argv)

    settings = load_settings()
    if not args.path.exists():
        parser.error(f"Caminho inexistente: {args.path}")

    copied = ingest(args.path, settings.knowledge_base_dir)

    if not copied:
        print("Nenhum arquivo valido encontrado para ingestao.")
        return 1

    print(f"{len(copied)} arquivo(s) copiado(s) para {settings.knowledge_base_dir}")
    for item in copied:
        print(f" - {item.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

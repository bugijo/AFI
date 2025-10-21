"""Helpers for configuring the AFI offline environment."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_PORT = 8507


def _normalize_path(value: str | None, *fallback: Path) -> Path:
    if value:
        candidate = Path(value).expanduser()
        if not candidate.is_absolute():
            return (ROOT_DIR / candidate).resolve()
        return candidate
    if not fallback:
        raise ValueError("fallback path is required when value is empty")
    return fallback[0].resolve()


def _ensure(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _strtobool(raw: str | None) -> bool:
    if raw is None:
        return False
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AFISettings:
    port: int
    input_dir: Path
    output_dir: Path
    log_dir: Path
    knowledge_base_dir: Path
    third_party_dir: Path
    ffmpeg_dir: Path
    no_deps: bool

    def all_dirs(self) -> Iterable[Path]:
        return (
            self.input_dir,
            self.output_dir,
            self.log_dir,
            self.knowledge_base_dir,
            self.third_party_dir,
            self.ffmpeg_dir,
        )


def load_settings(create_dirs: bool = True) -> AFISettings:
    port = int(os.getenv("AFI_PORT", DEFAULT_PORT))

    default_data = ROOT_DIR / "data"
    default_logs = ROOT_DIR / "logs"
    default_kb = ROOT_DIR / "knowledge_base"
    default_third_party = ROOT_DIR / "third_party"
    default_ffmpeg = default_third_party / "ffmpeg"

    input_dir = _normalize_path(os.getenv("AFI_INPUT_DIR"), default_data / "input")
    output_dir = _normalize_path(os.getenv("AFI_OUTPUT_DIR"), default_data / "output")
    log_dir = _normalize_path(os.getenv("AFI_LOG_DIR"), default_logs)
    knowledge_base_dir = _normalize_path(os.getenv("AFI_KB_DIR"), default_kb)
    third_party_dir = _normalize_path(os.getenv("AFI_THIRD_PARTY_DIR"), default_third_party)
    ffmpeg_dir = _normalize_path(os.getenv("AFI_FFMPEG_DIR"), default_ffmpeg)

    settings = AFISettings(
        port=port,
        input_dir=input_dir,
        output_dir=output_dir,
        log_dir=log_dir,
        knowledge_base_dir=knowledge_base_dir,
        third_party_dir=third_party_dir,
        ffmpeg_dir=ffmpeg_dir,
        no_deps=_strtobool(os.getenv("NO_DEPS", "0")),
    )

    if create_dirs:
        for directory in settings.all_dirs():
            _ensure(directory)

    return settings


def no_deps_mode() -> bool:
    return load_settings(create_dirs=False).no_deps


__all__ = ["AFISettings", "load_settings", "no_deps_mode", "ROOT_DIR", "DEFAULT_PORT"]

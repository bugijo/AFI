from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path('.').resolve()
RELEASE = ROOT / 'afi_v3_no_deps_release.zip'
INCLUDE_DIRS = [
    'scripts',
    'ui_fallback',
    'tools',
    'data',
    'logs',
    'third_party',
]
INCLUDE_FILES = [
    '.env.example',
    'README.md',
    'Dockerfile',
    'docker-compose.yml',
    'requirements.txt',
]
EXCLUDE_DIR_NAMES = {'.git', '.venv', 'wheels', '__pycache__', '.pytest_cache', '.trae'}
EXCLUDE_FILES = {'afi_v3_no_deps_release.zip'}

if RELEASE.exists():
    RELEASE.unlink()

with zipfile.ZipFile(RELEASE, 'w', zipfile.ZIP_DEFLATED) as zf:
    def should_skip(path: Path) -> bool:
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDE_DIR_NAMES for part in rel.parts):
            return True
        if rel.name in EXCLUDE_FILES:
            return True
        return False

    def add_directory(dir_path: Path) -> None:
        rel = dir_path.relative_to(ROOT).as_posix().rstrip('/') + '/'
        if rel not in zf.namelist():
            zf.writestr(rel, '')

    def add_file(file_path: Path) -> None:
        if should_skip(file_path):
            return
        rel = file_path.relative_to(ROOT).as_posix()
        if rel in zf.namelist():
            return
        zf.write(file_path, rel)

    for dir_name in INCLUDE_DIRS:
        dir_path = ROOT / dir_name
        if not dir_path.exists():
            continue
        add_directory(dir_path)
        for item in dir_path.rglob('*'):
            if should_skip(item):
                continue
            if item.is_dir():
                add_directory(item)
            elif item.is_file():
                add_file(item)

    for file_name in INCLUDE_FILES:
        file_path = ROOT / file_name
        if file_path.exists():
            add_file(file_path)

    for py_file in ROOT.glob('*.py'):
        add_file(py_file)

"""Minimal PEP 517/660 build backend for this educational package.

The repository intentionally has no mandatory runtime dependencies.  This small
backend keeps ``pip install -e .`` usable in constrained teaching environments
where setuptools may not already be installed.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

NAME = "quantum_bb84"
DIST = "quantum_bb84-0.1.0.dist-info"
VERSION = "0.1.0"


def _metadata() -> str:
    return "\n".join(
        [
            "Metadata-Version: 2.3",
            "Name: quantum-bb84",
            f"Version: {VERSION}",
            "Summary: Quantum Key Distribution Simulation Lab for BB84 and simplified E91 finite-shot simulations",
            "Requires-Python: >=3.10",
            "License-File: LICENSE",
            "",
        ]
    )


def _wheel() -> str:
    return "\n".join(
        [
            "Wheel-Version: 1.0",
            "Generator: quantum_bb84_build",
            "Root-Is-Purelib: true",
            "Tag: py3-none-any",
            "",
        ]
    )


def _entry_points() -> str:
    return "[console_scripts]\nquantum-bb84 = quantum_bb84.cli:main\n"


def _hash(data: bytes) -> tuple[str, str]:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
    return f"sha256={digest}", str(len(data))


def _write_wheel(path: Path, files: dict[str, bytes]) -> None:
    records: list[tuple[str, str, str]] = []
    for arcname, data in sorted(files.items()):
        digest, size = _hash(data)
        records.append((arcname, digest, size))
    record_name = f"{DIST}/RECORD"
    records.append((record_name, "", ""))
    import io

    record_buffer = io.StringIO()
    writer = csv.writer(record_buffer, lineterminator="\n")
    writer.writerows(records)
    files[record_name] = record_buffer.getvalue().encode()

    with ZipFile(path, "w", ZIP_DEFLATED) as zf:
        for arcname, data in sorted(files.items()):
            zf.writestr(arcname, data)


def _dist_info_files() -> dict[str, bytes]:
    return {
        f"{DIST}/METADATA": _metadata().encode(),
        f"{DIST}/WHEEL": _wheel().encode(),
        f"{DIST}/entry_points.txt": _entry_points().encode(),
    }


def get_requires_for_build_wheel(config_settings=None) -> list[str]:
    return []


def get_requires_for_build_editable(config_settings=None) -> list[str]:
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None) -> str:
    dist = Path(metadata_directory) / DIST
    dist.mkdir(parents=True, exist_ok=True)
    (dist / "METADATA").write_text(_metadata())
    (dist / "WHEEL").write_text(_wheel())
    (dist / "entry_points.txt").write_text(_entry_points())
    return DIST


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None) -> str:
    root = Path(__file__).resolve().parent
    wheel_name = f"quantum_bb84-{VERSION}-py3-none-any.whl"
    files = _dist_info_files()
    for path in sorted((root / NAME).rglob("*.py")):
        files[str(path.relative_to(root)).replace(os.sep, "/")] = path.read_bytes()
    license_path = root / "LICENSE"
    if license_path.exists():
        files[f"{DIST}/licenses/LICENSE"] = license_path.read_bytes()
    _write_wheel(Path(wheel_directory) / wheel_name, files)
    return wheel_name


def build_editable(wheel_directory, config_settings=None, metadata_directory=None) -> str:
    root = Path(__file__).resolve().parent
    wheel_name = f"quantum_bb84-{VERSION}-0.editable-py3-none-any.whl"
    files = _dist_info_files()
    files["quantum_bb84_editable.pth"] = f"{root}\n".encode()
    license_path = root / "LICENSE"
    if license_path.exists():
        files[f"{DIST}/licenses/LICENSE"] = license_path.read_bytes()
    _write_wheel(Path(wheel_directory) / wheel_name, files)
    return wheel_name

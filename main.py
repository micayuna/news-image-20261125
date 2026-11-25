#!/usr/bin/env python3
"""Deliver the 25 November 2026 news front page (entry.png) to /output."""

import hashlib
import os
import sys

MAX_BYTES = 1_048_576  # 1 MiB cap for the entry image
JPEG_MAGIC = b"\xff\xd8\xff"
ENTRY_NAME = "entry.png"


def _fingerprint(data: bytes) -> str:
    """Return the lowercase hex SHA-256 of data."""
    return hashlib.sha256(data).hexdigest()


def _human_size(size: int) -> str:
    """Render a byte count as a short human-readable string."""
    if size < 1024:
        return f"{size} B"
    return f"{size / 1024:.1f} KiB"


def _report(name: str, size: int, digest: str) -> str:
    """Build the one-line delivery report for the image."""
    return f"entry: {name} | size: {size} bytes ({_human_size(size)}) | sha256: {digest}"


def _check_jpeg(data: bytes) -> None:
    """Raise ValueError unless data looks like a non-empty JPEG within the cap."""
    if not data:
        raise ValueError("entry.png is empty")
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} byte cap")
    if data[:3] != JPEG_MAGIC:
        raise ValueError("entry.png does not start with the JPEG magic bytes ff d8 ff")


def _verify_written(path: str, digest: str) -> None:
    """Re-read the delivered file and confirm its fingerprint still matches."""
    with open(path, "rb") as handle:
        written = handle.read()
    if _fingerprint(written) != digest:
        raise ValueError(f"{path} changed while writing (fingerprint mismatch)")


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ENTRY_NAME)
    with open(source, "rb") as handle:
        data = handle.read()
    _check_jpeg(data)
    digest = _fingerprint(data)
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, ENTRY_NAME)
    with open(target, "wb") as handle:
        handle.write(data)
    _verify_written(target, digest)
    print(_report(ENTRY_NAME, len(data), digest))
    print(f"wrote {target} (verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

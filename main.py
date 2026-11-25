"""Deliver the 25 November 2026 front page as /output/entry.png.

Reads the bundled entry.png next to this file, verifies it, and writes it
to /output/entry.png for the grader. Prints a short report.
"""

import hashlib
import os
import sys

MAX_ENTRY_BYTES = 1_048_576


def _fingerprint(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _report(name: str, size: int, digest: str) -> str:
    return f"{name}: {size} bytes, sha256 {digest}"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if not data.startswith(b"\xff\xd8\xff"):
        print("entry.png is not a JPEG", file=sys.stderr)
        return 1
    if not 0 < len(data) <= MAX_ENTRY_BYTES:
        print(f"entry.png size {len(data)} out of range", file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    dst = "/output/entry.png"
    with open(dst, "wb") as f:
        f.write(data)
    print(_report("entry.png", len(data), _fingerprint(data)))
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

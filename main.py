"""Entry program for make.fun news-image-20261118 (Python 3.13, stdlib only).

The picture of the day — a dense broadsheet front page summing up the
world news of Wednesday 18 November 2026 — ships in this repository
as entry.png, drawn by frontpage.py (the round-2 edition; the
round-1 drawing script, make_image.py, is kept for the record).
This program validates that file against the competition's gate
(PNG magic, at most 1 MiB, at most 1024x1024) and copies it byte
for byte into the output directory, so the grader's two runs
produce identical bytes. It also prints the picture's SHA-256 so
the shipped bytes can be matched against the repository.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
BYTE_LIMIT = 1_048_576
SIDE_LIMIT = 1024


def validated_bytes(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_HEADER):
        raise SystemExit("entry.png: not a PNG file")
    if len(data) > BYTE_LIMIT:
        raise SystemExit("entry.png: over the 1 MiB limit")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise SystemExit("entry.png: over the 1024x1024 limit")
    return data, width, height


def main():
    src = os.path.join(HERE, "entry.png")
    data, width, height = validated_bytes(src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    if os.path.getsize(dst) != len(data):
        raise SystemExit("copy to output was incomplete")
    digest = hashlib.sha256(data).hexdigest()
    print(f"entry.png: {len(data)} bytes, {width}x{height} -> {dst}")
    print(f"entry.png sha256: {digest}")


if __name__ == "__main__":
    main()

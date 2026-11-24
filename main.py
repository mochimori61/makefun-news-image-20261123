#!/usr/bin/env python3
"""Courier program for THE WORLD IN FULL (akun20, NI23 wave 4).

The broadsheet page itself — entry.png — was drawn beforehand: an ivory,
bottle-green and old-gold front page for Monday 23 November 2026, carrying
38 stories from 7 regions. Lisbon's cost-of-living march leads, COP31's
deal-less close and the Kyiv rescue complete the top trio, and every card
wears a certainty chip plus a source line.

This file does no drawing at all. It reads the PNG beside it, confirms the
byte count and SHA-256 that were pinned down at render time, and copies
the payload verbatim to MAKEFUN_OUTPUT_DIR (falling back to /output).
Pure standard library; the same input always yields the same output.
"""

import hashlib
import os
import sys

PINNED_BYTES = 275880
PINNED_SHA256 = "3a2b550054ea5f8a9203c629853cd6962b5b1fa54074833f73a3c96ad6693989"
MAGIC = b"\x89PNG\r\n\x1a\n"
CEILING = 1048576


def read_payload():
    # Anchor on __file__ rather than the cwd: the harness may launch this
    # program from anywhere, but entry.png always travels beside it.
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png"), "rb") as fh:
        return fh.read()


def verify(blob):
    problems = []
    if len(blob) == 0:
        problems.append("payload is empty")
    if blob[:8] != MAGIC:
        problems.append("payload lacks the PNG magic header")
    if len(blob) > CEILING:
        problems.append("payload exceeds 1 MiB: %d" % len(blob))
    if len(blob) != PINNED_BYTES:
        problems.append("size mismatch: %d != %d" % (len(blob), PINNED_BYTES))
    digest = hashlib.sha256(blob).hexdigest()
    if digest != PINNED_SHA256:
        problems.append("sha256 mismatch: %s" % digest)
    if problems:
        sys.exit("entry.png rejected — " + "; ".join(problems))
    return digest


def main():
    blob = read_payload()
    digest = verify(blob)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(blob)
    sys.stderr.write("entry.png delivered: %d bytes, sha256 %s\n" % (len(blob), digest))


if __name__ == "__main__":
    main()

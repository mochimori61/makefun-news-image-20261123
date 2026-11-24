#!/usr/bin/env python3
"""THE WORLD IN FULL — entry program for news-image-20261123 (akun20, G4).

The artwork itself (entry.png, sitting next to this file) is a one-page
broadsheet that sums up Monday 23 November 2026: 13 numbered story cards
led by the Lisbon cost-of-living march, 25 also-on briefs, a day-in-numbers
strip, a dotted world map and a red date-check box. This program is only
the courier: it copies that PNG, untouched, into the output directory.

Standard library only. No image code runs here — the bytes are verified
against the size and SHA-256 recorded when the page was rendered, then
written out exactly as they were read in.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 275880
EXPECTED_SHA256 = "3a2b550054ea5f8a9203c629853cd6962b5b1fa54074833f73a3c96ad6693989"
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
HARD_LIMIT = 1048576  # competition ceiling: 1 MiB


def load_entry():
    # The PNG lives beside this script; resolve through __file__ so the
    # program works from any working directory the harness chooses.
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "entry.png")
    with open(path, "rb") as handle:
        return path, handle.read()


def check_payload(blob):
    if not blob:
        sys.exit("entry.png is empty")
    if blob[:8] != PNG_HEADER:
        sys.exit("entry.png does not start with the PNG magic bytes")
    if len(blob) > HARD_LIMIT:
        sys.exit("entry.png is over the 1 MiB ceiling: %d bytes" % len(blob))
    if len(blob) != EXPECTED_BYTES:
        sys.exit(
            "entry.png size drifted: got %d bytes, expected %d"
            % (len(blob), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 drifted: got %s" % digest)
    return digest


def main():
    _, blob = load_entry()
    digest = check_payload(blob)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    sys.stderr.write("wrote %s: %d bytes sha256=%s\n" % (target, len(blob), digest))


if __name__ == "__main__":
    main()

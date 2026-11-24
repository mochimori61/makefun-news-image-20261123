#!/usr/bin/env python3
"""Entry program for THE GLOBE IN ONE DAY (akun20, @mochimori0172).

Front page of THE GLOBE IN ONE DAY for Monday 23 November 2026: forty
stories on a single sheet, the lead being gold's slide to $3,538 an
ounce after touching its 2026 record. This little program is the
delivery boy, nothing more — it carries the finished entry.png from
beside itself into the output directory, and it will not carry a
substitute: the byte count and SHA-256 below were pinned when the
page was printed, and any file that disagrees is turned away.

Standard library only (hashlib, os, sys). No picture is drawn here;
the picture is freight.
"""

import hashlib
import os
import sys

# Pinned at print time for the THE GLOBE IN ONE DAY front page.
PINNED_SIZE = 271120
PINNED_SHA256 = "048eef8eb5d523f868aa5870c6a09f5c76981f14f607c414740297cb7db59a8e"
SIZE_CAP = 1024 * 1024  # competition ceiling: one mebibyte
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fetch_page():
    """Load entry.png from this program's own folder."""
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.png"), "rb") as fh:
        return fh.read()


def inspect_page(blob):
    """Verify the page is the exact sheet that left the press.

    Returns the verified digest; exits with a message otherwise.
    """
    if not blob.startswith(PNG_MAGIC):
        sys.exit("refusing: entry.png lacks the PNG signature")
    if len(blob) > SIZE_CAP:
        sys.exit("refusing: entry.png exceeds the 1 MiB cap (%d bytes)" % len(blob))
    if len(blob) != PINNED_SIZE:
        sys.exit(
            "refusing: entry.png is %d bytes, pinned size is %d"
            % (len(blob), PINNED_SIZE)
        )
    digest = hashlib.sha256(blob).hexdigest()
    if digest != PINNED_SHA256:
        sys.exit("refusing: entry.png sha256 %s != pinned %s" % (digest, PINNED_SHA256))
    # Independent cross-check on the IHDR: the sheet must be square 1024.
    if len(blob) < 24:
        sys.exit("refusing: entry.png too short for an IHDR chunk")
    w = int.from_bytes(blob[16:20], "big")
    h = int.from_bytes(blob[20:24], "big")
    if (w, h) != (1024, 1024):
        sys.exit("refusing: entry.png measures %dx%d, expected 1024x1024" % (w, h))
    return digest


def deliver(blob, digest):
    """Copy the verified page into MAKEFUN_OUTPUT_DIR (default /output)."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(blob)
    sys.stderr.write(
        "THE GLOBE IN ONE DAY delivered: %s (%d bytes, sha256=%s)\n"
        % (dest, len(blob), digest)
    )


def main():
    blob = fetch_page()
    deliver(blob, inspect_page(blob))


if __name__ == "__main__":
    main()

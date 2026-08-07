#!/usr/bin/env python3
"""Resize source photos into web-sized versions and regenerate photos/photos.json.

Source photos are full-resolution camera JPEGs (several MB each), which are far
too heavy to serve to a phone. This downscales them, strips metadata, and writes
the manifest the slideshow reads.

Usage:  python3 tools/build-photos.py [source_dir]
"""

import glob
import json
import os
import sys

from PIL import Image, ImageOps

DEFAULT_SRC = os.path.expanduser("~/Dropbox/Escape Room/photoSlide")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "photos")
MAX_EDGE = 1200
QUALITY = 82


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    if not os.path.isdir(src):
        sys.exit(f"source directory not found: {src}")

    os.makedirs(OUT, exist_ok=True)
    files = sorted(
        f for ext in ("JPG", "jpg", "JPEG", "jpeg", "PNG", "png")
        for f in glob.glob(os.path.join(src, f"*.{ext}"))
    )
    if not files:
        sys.exit(f"no images found in {src}")

    for stale in glob.glob(os.path.join(OUT, "*.jpg")):
        os.remove(stale)

    manifest = []
    for path in files:
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
        name = os.path.splitext(os.path.basename(path))[0].lower() + ".jpg"

        # Copying pixel data into a fresh image drops EXIF, including any GPS tags.
        clean = Image.new("RGB", im.size)
        clean.putdata(list(im.getdata()))
        clean.save(os.path.join(OUT, name), "JPEG", quality=QUALITY, optimize=True, progressive=True)
        manifest.append(name)

    with open(os.path.join(OUT, "photos.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)

    total = sum(os.path.getsize(os.path.join(OUT, n)) for n in manifest)
    print(f"wrote {len(manifest)} photos ({total / 1e6:.1f} MB) to {OUT}")


if __name__ == "__main__":
    main()

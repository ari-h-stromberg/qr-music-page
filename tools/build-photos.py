#!/usr/bin/env python3
"""Resize source photos into web-sized versions and regenerate photos/photos.json.

Source photos are full-resolution camera JPEGs (several MB each), which are far
too heavy to serve to a phone. This downscales them, strips metadata, and writes
the manifest the slideshow reads, ordered oldest photo first.

Usage:  python3 tools/build-photos.py [source_dir]
"""

import datetime
import glob
import json
import os
import sys

from PIL import Image, ImageOps

EXIF_SUB_IFD = 0x8769
DATE_TIME_ORIGINAL = 36867   # when the shutter fired
DATE_TIME_DIGITIZED = 36868  # when it was digitised, same as above for digital cameras

# Tag 306 (DateTime) is deliberately not consulted: it records when the file was
# last written, so edited or exported photos report the edit date rather than
# when they were taken.


def taken_at(path):
    """When the photo was taken, falling back to the file's timestamp."""
    try:
        exif = Image.open(path).getexif()
        # These normally live in the Exif sub-IFD, not at the top level.
        for source in (exif.get_ifd(EXIF_SUB_IFD), exif):
            for tag in (DATE_TIME_ORIGINAL, DATE_TIME_DIGITIZED):
                raw = source.get(tag)
                if raw:
                    return datetime.datetime.strptime(str(raw)[:19], "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return datetime.datetime.fromtimestamp(os.path.getmtime(path))

DEFAULT_SRC = os.path.expanduser("~/Dropbox/Escape Room/photoSlide")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "photos")
MAX_EDGE = 1200
QUALITY = 82


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    if not os.path.isdir(src):
        sys.exit(f"source directory not found: {src}")

    os.makedirs(OUT, exist_ok=True)
    found = {
        f for ext in ("JPG", "jpg", "JPEG", "jpeg", "PNG", "png")
        for f in glob.glob(os.path.join(src, f"*.{ext}"))
    }
    if not found:
        sys.exit(f"no images found in {src}")

    # Oldest first, so the slideshow runs chronologically.
    files = sorted(found, key=taken_at)

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
    print(f"date range: {taken_at(files[0]):%Y-%m-%d} to {taken_at(files[-1]):%Y-%m-%d}")


if __name__ == "__main__":
    main()

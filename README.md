# QR Music Page

A minimal static page listing 4 tappable tracks — meant to be scanned via a printed QR code, letting whoever scans it pick a song to play.

## How it works

- `index.html` — the page with the track list and player
- `audio/track1.mp3` … `audio/track4.mp3` — the four tracks

Current mapping (display name → source file):

| On the page | File | Original |
| --- | --- | --- |
| Track X | `audio/track1.mp3` | 01 Lightning Bolt |
| Track Y | `audio/track2.mp3` | 03 All My Love |
| Track Z | `audio/track3.mp3` | 03 Skinny Love |
| Track Q | `audio/track4.mp3` | 26 The Prophecy |

Sources were `.m4a` (AAC), transcoded to 128 kbps MP3 to keep downloads fast over cellular.

## Updating the tracks

1. Replace the files in `audio/`, keeping the `track1.mp3` … `track4.mp3` names (or update the `src` values and titles in the `tracks` array near the bottom of `index.html`)
2. Commit and push — GitHub Pages redeploys automatically within a minute or two

## Hosting

Served via [GitHub Pages](https://pages.github.com/) at **https://can-lizzy-escape.us**, with HTTPS enforced via a Let's Encrypt certificate that GitHub renews automatically.

The domain is registered at Cloudflare, which also hosts its DNS. The apex points at GitHub Pages with `A` records (185.199.108–111.153) and `AAAA` records (2606:50c0:8000–8003::153). These must stay **DNS only** (grey cloud) in Cloudflare — proxying them breaks the TLS handshake with GitHub.

The old `ari-h-stromberg.github.io/qr-music-page` address still works and 301-redirects here.

## QR code

`assets/qr-code.png` encodes `HTTPS://CAN-LIZZY-ESCAPE.US`. The uppercase is deliberate: URLs are case-insensitive, and uppercase lets the QR use alphanumeric encoding mode instead of byte mode, which shrinks the grid from 33×33 to 29×29 and makes each printed square proportionally larger and easier to scan.

Open `assets/print.html` and print it for a ready-made 3.5 inch version.

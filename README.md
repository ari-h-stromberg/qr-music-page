# QR Music Page

A minimal static page listing 4 tappable tracks — meant to be scanned via a printed QR code, letting whoever scans it pick a song to play.

## How it works

- `index.html` — the page with the track list and player
- `audio/track1.mp3` … `audio/track4.mp3` — the four tracks (currently placeholders; add your own files here)

## Updating the tracks

1. Add your 4 MP3 files to the `audio/` folder, named `track1.mp3` through `track4.mp3` (or update the `src` values and titles in the `tracks` array near the bottom of `index.html` if you want different filenames/names)
2. Commit and push — GitHub Pages redeploys automatically within a minute or two

## Hosting

This repo is served via [GitHub Pages](https://pages.github.com/).

## Custom domain

To point a custom domain at this site later:

1. Add a `CNAME` file to the repo root containing just your domain (e.g. `music.example.com`)
2. In your DNS provider, add either:
   - A `CNAME` record for a subdomain pointing to `<username>.github.io`, or
   - `A` records for an apex domain pointing to GitHub Pages' IPs (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153)
3. In the repo's GitHub Settings → Pages, set the custom domain and enable "Enforce HTTPS" once DNS propagates

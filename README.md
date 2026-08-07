# QR Music Page

A minimal static page that autoplays a custom MP3 when opened — meant to be scanned via a printed QR code.

## How it works

- `index.html` — the page with the audio player
- `audio/song.mp3` — the track that gets played (add your own file here)

## Updating the track

1. Replace `audio/song.mp3` with your MP3 (keep the same filename, or update the `src` in `index.html`)
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

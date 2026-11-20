# Tarkov PvE Terminal Alternative Route Guide

A static GitHub Pages site that plays the route guide video with chapters and a route map.

- `index.html`: player, chapter list (edit `CHAPTERS` near the top of the script), and route map.
- `video/`: HLS stream (1080p60 and 540p, 4 second segments) made with ffmpeg from the original MP4.
- `route.json`: pins and route lines per chapter. Use "Edit route" on the page, then "Download route.json" and replace this file.
- `sw.js`: service worker that caches watched video segments so seeking back is instant.

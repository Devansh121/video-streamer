# video-streamer

A video streaming backend built with FastAPI, FFmpeg, S3, and CloudFront.

Handles upload, transcoding to HLS, multi-bitrate adaptive streaming, and CDN delivery.

## Stack

- **FastAPI** — async API layer
- **FFmpeg** — video transcoding and HLS segmentation
- **Amazon S3** — segment and manifest storage
- **CloudFront** — CDN delivery at the edge
- **ARQ + Redis** — async job queue for transcoding

## Getting started

```bash
# coming soon
```

## Architecture

Upload → Transcode (FFmpeg) → HLS segments → S3 → CloudFront → Player

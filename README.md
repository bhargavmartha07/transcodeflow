# TranscodeFlow

A resilient, parallel video transcoding pipeline that simulates adaptive bitrate streaming systems like YouTube and Netflix.

## 🚀 Overview

TranscodeFlow monitors an input directory for uploaded `.mp4` files and processes them into multiple resolutions in parallel.

It demonstrates:

- Worker pool concurrency control
- Fault isolation
- Atomic manifest generation
- Docker containerization
- Docker Compose orchestration
- Health check endpoint

---

## 🏗 Architecture

1. Directory watcher monitors `input/`
2. For each video:
   - Creates output folder
   - Launches parallel transcoding jobs (360p, 480p, 720p, 1080p)
   - Concurrency limited via `MAX_WORKERS`
3. Results collected
4. Atomic `manifest.json` generated
5. Health endpoint exposed at `/health`

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| MAX_WORKERS | Max parallel transcoding jobs | 2 |
| FAIL_RESOLUTION | Resolution to intentionally fail | "" |
| APP_PORT | Service port | 8080 |

---

## 🐳 Running the Project

### Step 1: Clone Repository

```bash
git clone <repo-url>
cd TranscodeFlow

# 🎬 TranscodeFlow

A resilient, parallel video transcoding pipeline that simulates adaptive bitrate streaming systems used by platforms like YouTube and Netflix.

---

## 🚀 Overview

TranscodeFlow monitors an `input/` directory for uploaded `.mp4` files and processes them into multiple resolutions in parallel.

It demonstrates:

- ✔ Worker pool concurrency control
- ✔ Fault isolation
- ✔ Atomic manifest generation
- ✔ Docker containerization
- ✔ Docker Compose orchestration
- ✔ Health check endpoint integration

---

## 🏗 System Architecture

1. Directory watcher continuously monitors `input/`
2. For each detected `.mp4` file:
   - Creates a corresponding output directory
   - Launches parallel transcoding jobs (360p, 480p, 720p, 1080p)
   - Limits concurrency using `MAX_WORKERS`
3. Collects exit status from each job
4. Generates an atomic `manifest.json`
5. Exposes `/health` endpoint for container health checks

---

## 📂 Project Structure

```
TranscodeFlow/
│
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
│
├── source_code/
│   └── app.py
│
├── scripts/
│   └── transcode.sh
│
├── input/
├── output/
└── tests/ (optional)
```

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| MAX_WORKERS | Maximum parallel transcoding jobs | 2 |
| FAIL_RESOLUTION | Resolution to intentionally fail (e.g., 720p) | "" |
| APP_PORT | Application port | 8080 |

---

## 🐳 Running the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/bhargavmartha07/transcodeflow.git
cd transcodeflow
```

---

### 2️⃣ Start the Application

```bash
docker-compose up --build
```

This will:

- Build the Docker image
- Start the transcoding service
- Mount `input/` and `output/` directories
- Expose port `8080`
- Enable health checks

---

### 3️⃣ Verify Service

Open your browser:

```
http://localhost:8080
```

You should see:

```json
{
  "service": "TranscodeFlow",
  "status": "running",
  "health_endpoint": "/health"
}
```

Health endpoint:

```
http://localhost:8080/health
```

Returns:

```json
{"status":"healthy"}
```

---

### 4️⃣ Test Transcoding

Create a test file:

```
input/video1.mp4
```

The system will automatically:

- Process the video
- Generate multiple resolutions
- Create `manifest.json`

Check:

```
output/video1/
```

Example:

```
360p.mp4
480p.mp4
720p.mp4
1080p.mp4
manifest.json
```

---

## 📄 Example Manifest Output

```json
{
  "video": "video1.mp4",
  "results": {
    "360p": "success",
    "480p": "success",
    "720p": "failed",
    "1080p": "success"
  }
}
```

---

## 🔬 Design Highlights

- **Parallel Execution** using `ThreadPoolExecutor`
- **Concurrency Throttling** via `MAX_WORKERS`
- **Fault Isolation** (failure of one resolution does not affect others)
- **Atomic File Writes** using temporary file replacement
- **Container Healthcheck Integration**
- **Environment-driven Configuration**

---

## 🛠 Tech Stack

- Python
- Flask
- Bash
- Docker
- Docker Compose

---

## 📌 Notes

- `.env` is not committed to version control.
- `.env.example` documents required configuration.
- `input/` and `output/` are mounted as Docker volumes.

---

## 🎯 Learning Objectives Demonstrated

- Concurrent worker pool design
- Fault-tolerant parallel processing
- Atomic state management
- Container orchestration
- Production-style configuration handling

---

## 🏁 Stopping the Application

```bash
docker-compose down
```

---


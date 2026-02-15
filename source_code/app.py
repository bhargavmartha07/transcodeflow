import os
import time
import json
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, jsonify

# ------------------------------------------
# Configuration (Environment Variables)
# ------------------------------------------
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 2))
FAIL_RESOLUTION = os.getenv("FAIL_RESOLUTION", "")
APP_PORT = int(os.getenv("APP_PORT", 8080))

INPUT_DIR = "input"
OUTPUT_DIR = "output"
RESOLUTIONS = ["360p", "480p", "720p", "1080p"]

processed_files = set()
service_ready = False

app = Flask(__name__)

# ------------------------------------------
# Root Endpoint (For Evaluators)
# ------------------------------------------
@app.route("/")
def home():
    return jsonify({
        "service": "TranscodeFlow",
        "status": "running",
        "health_endpoint": "/health"
    }), 200


# ------------------------------------------
# Health Endpoint (Docker Healthcheck)
# ------------------------------------------
@app.route("/health")
def health():
    if service_ready:
        return jsonify({"status": "healthy"}), 200
    return jsonify({"status": "starting"}), 503


# ------------------------------------------
# Atomic Manifest Writer
# ------------------------------------------
def atomic_write(filepath, data):
    temp_path = filepath + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(data, f, indent=4)
    os.replace(temp_path, filepath)


# ------------------------------------------
# Transcoding Worker
# ------------------------------------------
def transcode_video(input_path, output_path, resolution):
    cmd = [
        "bash",
        "scripts/transcode.sh",
        input_path,
        output_path,
        resolution,
        FAIL_RESOLUTION
    ]

    result = subprocess.run(cmd)
    return resolution, result.returncode == 0


# ------------------------------------------
# Process Single Video
# ------------------------------------------
def process_video(filename):
    video_name = os.path.splitext(filename)[0]
    input_path = os.path.join(INPUT_DIR, filename)
    video_output_dir = os.path.join(OUTPUT_DIR, video_name)

    os.makedirs(video_output_dir, exist_ok=True)

    print(f"\n📹 Processing video: {filename}")
    print(f"🔧 MAX_WORKERS = {MAX_WORKERS}")
    print(f"⚠ FAIL_RESOLUTION = {FAIL_RESOLUTION}")

    results = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []

        for resolution in RESOLUTIONS:
            output_file = os.path.join(video_output_dir, f"{resolution}.mp4")

            futures.append(
                executor.submit(
                    transcode_video,
                    input_path,
                    output_file,
                    resolution
                )
            )

        for future in as_completed(futures):
            resolution, success = future.result()
            results[resolution] = "success" if success else "failed"

    manifest_path = os.path.join(video_output_dir, "manifest.json")

    manifest_data = {
        "video": filename,
        "results": results
    }

    atomic_write(manifest_path, manifest_data)

    print(f"✅ Finished processing {filename}")
    print(f"📄 Manifest written to {manifest_path}")


# ------------------------------------------
# Directory Watcher
# ------------------------------------------
def watch_directory():
    global service_ready

    print("👀 Watching input directory for new videos...")
    service_ready = True

    while True:
        files = [
            f for f in os.listdir(INPUT_DIR)
            if f.endswith(".mp4")
        ]

        for file in files:
            if file not in processed_files:
                processed_files.add(file)
                process_video(file)

        time.sleep(3)


# ------------------------------------------
# Main Entry Point
# ------------------------------------------
if __name__ == "__main__":
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    watcher_thread = threading.Thread(target=watch_directory)
    watcher_thread.daemon = True
    watcher_thread.start()

    app.run(host="0.0.0.0", port=APP_PORT)

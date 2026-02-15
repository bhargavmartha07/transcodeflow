#!/bin/bash
# scripts/transcode.sh

# Exit immediately if any unexpected command fails
set -e

# -----------------------------
# Arguments
# -----------------------------
INPUT_FILE=$1
OUTPUT_FILE=$2
RESOLUTION=$3
FAIL_RESOLUTION=$4   # Resolution that should intentionally fail

# -----------------------------
# Configuration
# -----------------------------
PROCESSING_TIME=5

# -----------------------------
# Validation
# -----------------------------
if [[ -z "$INPUT_FILE" || -z "$OUTPUT_FILE" || -z "$RESOLUTION" ]]; then
  echo "Usage: $0 <input_file> <output_file> <resolution> <fail_resolution>"
  exit 2
fi

# -----------------------------
# Start Processing
# -----------------------------
echo "[$(date +'%T')] Starting transcoding:"
echo "    Input: $INPUT_FILE"
echo "    Output: $OUTPUT_FILE"
echo "    Resolution: $RESOLUTION"
echo "    Will Fail If Resolution = $FAIL_RESOLUTION"
echo "[$(date +'%T')] Simulating processing for ${PROCESSING_TIME}s..."

sleep $PROCESSING_TIME

# -----------------------------
# Simulate Failure
# -----------------------------
if [[ "$RESOLUTION" == "$FAIL_RESOLUTION" && -n "$FAIL_RESOLUTION" ]]; then
  echo "[$(date +'%T')] ❌ Transcoding FAILED for $RESOLUTION" >&2
  exit 1
fi

# -----------------------------
# Simulate Success
# -----------------------------
mkdir -p "$(dirname "$OUTPUT_FILE")"
touch "$OUTPUT_FILE"

echo "[$(date +'%T')] ✅ Transcoding SUCCEEDED for $RESOLUTION"
exit 0

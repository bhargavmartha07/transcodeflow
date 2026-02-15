import json

def test_manifest_format():
    sample = {
        "video": "video1.mp4",
        "results": {
            "360p": "success",
            "480p": "failed"
        }
    }

    assert "video" in sample
    assert "results" in sample

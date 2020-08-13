# Getting Started

This document provides a quick guide for getting 
started with the Element Human Biometrics client.  

## Instantiate Client

First we will need to instantiate the client.
This can be done as follows:

```python linenums="1"
from pathlib import Path
from biometrics_client import ElementHumanBiometrics

client = ElementHumanBiometrics(
    access_key="YOUR-ACCESS-KEY-HERE", 
    secret_key="YOUR-SECRET-KEY-HERE"
)
```

## Apply

With the client instantiated, we can now submit a video
for analysis.

```python linenums="8"
response = client.apply(
    video_file_path=Path("path/to/video/file.mp4"), 
    analyses=["emotion"]
)
```

where `response` is an object that looks like this:

```json
{"response": {"task_id": "TASK-ID"}, "version": "0.5.0"}
```

## Results

The `task_id` in the response payload above can be used
to fetch the results.

```python linenums="12"
analysis = client.results(response["response"]["task_id"])
```

If the results are not yet ready, the `.results()`
endpoint will raise a `BiometricsApiResultsNotReadyError`.

Alternatively, you can combine the steps above running:

```python linenums="1"
analysis = client.apply_and_wait(
    video_file_path=Path("path/to/video/file.mp4"), 
    analyses=["emotion"]
)
```

## Sample Analysis

The `analysis` payload you receive will be similar to the example provided below.

```json linenums="1"
{
  "response": {
    "frames": {
      "emotion_anger": [
        0.0,
        0.0,
        0.0
      ],
      "emotion_disgust": [
        0.0,
        0.0,
        0.06841050328746918
      ],
      "emotion_fear": [
        0.0,
        0.0,
        0.0
      ],
      "emotion_happy": [
        0.3209093087420444,
        0.04277153451128254,
        0.0
      ],
      "emotion_sad": [
        0.0,
        0.0,
        0.0
      ],
      "emotion_surprise": [
        0.0,
        0.0,
        0.0
      ],
      "timestamp": [
        0.0,
        1.0,
        2.0
      ]
    },
    "summary": {
      "files": {
        "calibration": null
      },
      "metrics": {
        "proportion_present_face": 1.0,
        "proportion_present_left_eye": 1.0,
        "proportion_present_right_eye": 1.0,
        "average_bitrate": 134585.88,
        "frames_per_second": 15.02,
        "duration_seconds": 1.997
      }
    }
  },
  "version": "0.5.0"
}
```

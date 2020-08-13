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

This gives us a response object that looks like the following:

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
      "predictions_emotion_normalized_anger": [
        0.0,
        0.0,
        0.0
      ],
      "predictions_emotion_normalized_arousal": [
        0.08945174887776375,
        0.13123975053895265,
        0.1314315510292848
      ],
      "predictions_emotion_normalized_disgust": [
        0.0,
        0.0,
        0.06841050328746918
      ],
      "predictions_emotion_normalized_expression": [
        0.0,
        0.0,
        0.0
      ],
      "predictions_emotion_normalized_fear": [
        0.0,
        0.0,
        0.0
      ],
      "predictions_emotion_normalized_happy": [
        0.3209093087420444,
        0.04277153451128254,
        0.0
      ],
      "predictions_emotion_normalized_sad": [
        0.0,
        0.0,
        0.0
      ],
      "predictions_emotion_normalized_surprise": [
        0.0,
        0.0,
        0.0
      ],
      "predictions_emotion_normalized_valence": [
        0.23482961976720432,
        -0.12330629512847913,
        -0.28168490505026234
      ],
      "predictions_emotion_raw_anger": [
        0.006295658027132352,
        0.022384132840670645,
        0.024185805891950924
      ],
      "predictions_emotion_raw_arousal": [
        0.08945174887776375,
        0.13123975053895265,
        0.1314315510292848
      ],
      "predictions_emotion_raw_disgust": [
        0.009831455536186695,
        0.06364473630674183,
        0.10028434793154399
      ],
      "predictions_emotion_raw_expression": [
        0.9173897206783295,
        0.609102126210928,
        0.43368252118428546
      ],
      "predictions_emotion_raw_fear": [
        0.006468637380748987,
        0.013182169786887243,
        0.015840270866950352
      ],
      "predictions_emotion_raw_happy": [
        0.8234855383634567,
        0.3372399490326643,
        0.09032581249872844
      ],
      "predictions_emotion_raw_neutral": [
        0.0826102818051974,
        0.39089787658303976,
        0.5663174788157145
      ],
      "predictions_emotion_raw_sad": [
        0.031000592435399692,
        0.10014854627661407,
        0.13517327855030695
      ],
      "predictions_emotion_raw_surprise": [
        0.042127889270583786,
        0.07503655855543911,
        0.07150404527783394
      ],
      "predictions_emotion_raw_valence": [
        0.43470364809036255,
        0.07656773319467902,
        -0.08181087672710419
      ],
      "metadata_video_timestamp_raw": [
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

# BiometricsClient

Client Library for the Element Human BiometricsAPI

## Installation

```shell script
pip install git+ssh://git@gitlab.com/elementhuman/biometrics_client.git
```

## Example Usage

```python
from pathlib import Path
from biometrics_client import ElementHumanBiometrics

biometrics = ElementHumanBiometrics(
    access_key="YOUR-ACCESS-KEY-HERE",
    secret_key="YOUR-SECRET-KEY-HERE"
)

result = biometrics.apply_and_wait(
    video_file_path=Path("path/to/video/file.mp4"),
    analyses=["emotion"]
)
```

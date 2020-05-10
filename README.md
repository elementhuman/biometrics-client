# BiometricsClient

Client Library for the Element Human BiometricsAPI

## Installation

```shell script
pip install git+ssh://git@gitlab.com/elementhuman/biometricsclient.git
```

## Example Usage

```python
from pathlib import Path
from biometrics_client import Auth1, ElementHumanBiometrics

biometrics = ElementHumanBiometrics(
    auth=Auth1(
        access_key="YOUR-ACCESS-KEY-HERE", 
        secret_key="YOUR-SECRET-KEY-HERE"
    )
)

response = biometrics.apply_and_wait(
    video_file_path=Path("path/to/video/file.mp4"), 
    analyses=["emotion"]
)
```

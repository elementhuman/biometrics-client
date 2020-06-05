"""

    Tests
    ~~~~~

"""
from pathlib import Path

TEST_VIDEO_PATH = Path("tests/_fixtures/camera_200_2200.webm").absolute()
assert TEST_VIDEO_PATH.exists()

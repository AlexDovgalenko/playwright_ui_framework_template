from enum import Enum
from pathlib import Path
from typing import Dict, List

LOG_DIR: Path = Path("logs")  # Directory for log files
VIDEO_DIR: Path = Path("videos")  # Directory for video recordings
DATA_DIR = Path("test_data")  # Directory for test data files
LOG_MESSAGE_FORMAT = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
LOG_TIME_FORMAT = "%H:%M:%S"


class StrEnum(str, Enum):
    """Base class for string enums to ensure consistent string representation."""

    def __str__(self) -> str:
        return self.value

    @classmethod
    def values(cls) -> List[str]:
        return [element.value for element in cls]


class BrowserType(StrEnum):
    """Supported browser types for testing."""

    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"
    EDGE = "edge"  # Adding Edge browser support


# instead of providing `get_dimensions` method assign resolution for each class attibute e.g. `HD = {"width": 1280, "height": 720}` instead of `HD = auto()`
class Resolution(Enum):
    HD = {"width": 1280, "height": 720}
    FHD = {"width": 1920, "height": 1080}
    QHD = {"width": 2560, "height": 1440}
    UHD = {"width": 3840, "height": 2160}
    FULLSCREEN = None  # Uses full screen size

    @classmethod
    def values(cls) -> List[Dict[str, int] | None]:
        return [element.value for element in cls]

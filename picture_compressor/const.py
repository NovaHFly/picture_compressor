from enum import Enum, auto


class Mode(Enum):
    """Picture shrink mode."""

    LESSER_SIZE = auto()
    GREATER_SIZE = auto()
    MULTIPLIER = auto()


class Orientation(Enum):
    """Possible picture orientations."""

    LANDSCAPE = auto()
    PORTRAIT = auto()
    SQUARE = auto()


ALLOWED_FORMATS = ('jpg', 'jpe', 'jpeg', 'png', 'webp', 'tif')

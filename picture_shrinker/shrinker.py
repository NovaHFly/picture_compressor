from enum import Enum, auto
from pathlib import Path

import PIL.Image as img
from PIL import UnidentifiedImageError

ALLOWED_FORMATS = ('jpg', 'jpe', 'jpeg', 'png', 'webp', 'tif')
RESULT_PATH = Path('./Shrunk')

# TODO: Option to skip pictures bigger than provided size
# TODO: Add logging


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


def detect_orientation(image: img.Image) -> Orientation:
    """Detect picture orientation.

    Args:
        image (Image): Image which orientation we need to get.

    Returns:
        Orientation: picture orientation.
    """
    if image.width > image.height:
        return Orientation.LANDSCAPE
    if image.width < image.height:
        return Orientation.PORTRAIT
    return Orientation.SQUARE


class FixedRatioPicture:
    """Adapter which simpler resize interface to Pillow's Image.

    This adapter ensures that its image aspect ratio is preserved.
    """

    def __init__(self, image: img.Image) -> None:
        """Adapter which provides simpler interface to Pillow's Image.

        Args:
            image (Image): Image file to manipulate.
        """
        self.image = image

    def resize_to_multiplier(self, multiplier: float) -> None:
        """Resize picture to a multiplier."""
        self.width = round(self.width * multiplier)

    @property
    def side_ratio(self) -> float:
        """Picture width to height ratio."""
        return self.width / self.height

    @property
    def orientation(self) -> Orientation:
        """Picture orientation."""
        return detect_orientation(self.image)

    @property
    def width(self) -> int:
        """Picture width in px."""
        return self.image.width

    @width.setter
    def width(self, new_width: int) -> None:
        new_size = (new_width, round(new_width / self.side_ratio))
        self.image = self.image.resize(new_size)

    @property
    def height(self) -> int:
        """Picture height in px."""
        return self.image.height

    @height.setter
    def height(self, new_height: int) -> None:
        new_size = (round(new_height * self.side_ratio), new_height)
        self.image = self.image.resize(new_size)

    @property
    def lesser_size(self) -> int:
        """Picture lesser size in px."""
        if self.orientation is Orientation.PORTRAIT:
            return self.width

        return self.height

    @lesser_size.setter
    def lesser_size(self, new_size: int) -> None:
        if self.orientation is Orientation.PORTRAIT:
            self.width = new_size
            return

        self.height = new_size

    @property
    def greater_size(self) -> int:
        """Picture greater size in px."""
        if self.orientation is Orientation.PORTRAIT:
            return self.height

        return self.width

    @greater_size.setter
    def greater_size(self, new_size: int) -> None:
        if self.orientation is Orientation.PORTRAIT:
            self.height = new_size
            return

        self.width = new_size

    @property
    def size(self) -> tuple[int, int]:
        """Picture width and height."""
        return self.width, self.height


def _open_image(path: Path) -> img.Image:
    try:
        return img.open(path)
    except UnidentifiedImageError:
        # TODO: Some indication that error has happened
        raise


def _shrink_picture(
    picture: FixedRatioPicture, mode: Mode, size: float
) -> None:
    if mode is Mode.MULTIPLIER:
        picture.resize_to_multiplier(size)
    elif mode is Mode.GREATER_SIZE:
        picture.greater_size = int(size)
    elif mode is Mode.LESSER_SIZE:
        picture.lesser_size = int(size)


def _save_picture(picture: FixedRatioPicture, source_path: Path) -> None:
    # TODO: Both paths may be dynamic

    new_path = RESULT_PATH / source_path
    new_path.parent.mkdir(exist_ok=True, parents=True)
    picture.image.save(new_path)


def process_picture(
    path: Path,
    mode: Mode,
    size: float,
) -> None:
    """Shrink a picture to set size/ratio.

    Args:
        path (Path): Path to picture file.
        mode (Mode): Shrink mode to use.
        size (float): Shrink size (abs or ratio).
    """
    image = _open_image(path)
    picture = FixedRatioPicture(image)

    _shrink_picture(picture, mode=mode, size=size)
    _save_picture(picture, source_path=path)

    new_path = RESULT_PATH / path
    new_path.parent.mkdir(exist_ok=True, parents=True)
    image.save(new_path)

    image.close()

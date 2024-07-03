
from PIL import Image as img

from .const import Orientation


class BasePicture:
    """Base class for all picture adapters."""

    def __init__(self, image: img.Image) -> None:
        """Create a new picture adapter."""
        self.image = image


class FixedRatioPicture(BasePicture):
    """Adapter which simpler resize interface to Pillow's Image.

    This adapter ensures that its image aspect ratio is preserved.
    """

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
        if self.image.width > self.image.height:
            return Orientation.LANDSCAPE
        if self.image.width < self.image.height:
            return Orientation.PORTRAIT
        return Orientation.SQUARE

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

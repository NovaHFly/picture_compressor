import pytest
from PIL import Image as img

from picture_compressor.picture import FixedRatioPicture


def _get_picture(size: tuple[int, int]) -> FixedRatioPicture:
    return FixedRatioPicture(img.new('RGBA', size))


@pytest.fixture
def size_landscape():
    return (4000, 3000)


@pytest.fixture
def size_portrait():
    return (3000, 4000)


@pytest.fixture
def size_square():
    return (4000, 4000)


@pytest.fixture
def landscape_picture(size_landscape):
    return _get_picture(size_landscape)


@pytest.fixture
def portrait_picture(size_portrait):
    return _get_picture(size_portrait)


@pytest.fixture
def square_picture(size_square):
    return _get_picture(size_square)

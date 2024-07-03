import pytest
from pytest_lazyfixture import lazy_fixture as lf

from picture_shrinker.shrinker import (
    Orientation,
    detect_orientation,
)


@pytest.mark.parametrize(
    'picture, orientation',
    (
        (lf('landscape_picture'), Orientation.LANDSCAPE),
        (lf('portrait_picture'), Orientation.PORTRAIT),
        (lf('square_picture'), Orientation.SQUARE),
    ),
)
def test_detect_orientation(picture, orientation):
    assert detect_orientation(picture.image) is orientation


@pytest.mark.parametrize(
    'picture, expected_size',
    (
        (lf('landscape_picture'), (2000, 1500)),
        (lf('portrait_picture'), (1500, 2000)),
        (lf('square_picture'), (2000, 2000)),
    ),
)
def test_shrink_picture_to_ratio(picture, expected_size):
    picture.resize_to_multiplier(0.5)
    assert picture.size == expected_size


@pytest.mark.parametrize(
    'picture, new_size',
    (
        (lf('landscape_picture'), (1800, 1350)),
        (lf('portrait_picture'), (1800, 2400)),
        (lf('square_picture'), (1800, 1800)),
    ),
)
def test_change_width(picture, new_size):
    picture.width = new_size[0]
    assert picture.size == new_size


@pytest.mark.parametrize(
    'picture, new_size',
    (
        (lf('landscape_picture'), (2400, 1800)),
        (lf('portrait_picture'), (1350, 1800)),
        (lf('square_picture'), (1800, 1800)),
    ),
)
def test_change_height(picture, new_size):
    picture.height = new_size[1]
    assert picture.size == new_size

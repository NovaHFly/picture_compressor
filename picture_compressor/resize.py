import shutil
from pathlib import Path

import PIL.Image as img
from PIL import UnidentifiedImageError

from .const import ALLOWED_FORMATS, Mode
from .picture import FixedRatioPicture

RESULT_PATH = Path('./_resized_pictures')

# TODO: Option to skip pictures bigger than provided size
# TODO: Add logging


def _open_image(path: Path) -> img.Image:
    try:
        return img.open(path)
    except UnidentifiedImageError:
        # TODO: Some indication that error has happened
        raise


def _resize_picture(
    picture: FixedRatioPicture, mode: Mode, size: float
) -> None:
    if mode is Mode.MULTIPLIER:
        picture.resize_to_multiplier(size)
    elif mode is Mode.GREATER_SIZE:
        picture.greater_size = int(size)
    elif mode is Mode.LESSER_SIZE:
        picture.lesser_size = int(size)


def process_directory(
    path: Path,
    mode: Mode,
    size: float,
) -> None:
    """Resize all pictures in folder. Copy all incompatible files."""
    for file_path in path.glob('**/*.*'):
        process_picture(file_path, mode, size)


def process_picture(
    path: Path,
    mode: Mode,
    size: float,
) -> None:
    """Resize a picture to set size/multiplier.

    Args:
        path (Path): Path to picture file.
        mode (Mode): Resize mode to use.
        size (float): Resize size (abs or multiplier).
    """
    new_path = RESULT_PATH / path
    new_path.parent.mkdir(exist_ok=True, parents=True)

    if path.suffix[1:] not in ALLOWED_FORMATS:
        print(f'Copying {path} as is.')
        shutil.copyfile(path, new_path)
        return

    with FixedRatioPicture.from_path(path) as picture:
        _resize_picture(picture, mode=mode, size=size)
        picture.image.save(new_path)
        print(f'{path} processed!.')

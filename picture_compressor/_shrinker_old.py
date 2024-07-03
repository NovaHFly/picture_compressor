import asyncio
import itertools
import math
import shutil
from pathlib import Path
from typing import Iterator

from PIL import Image, UnidentifiedImageError

ORIENT_LANDSCAPE = 'landscape'
ORIENT_PORTRAIT = 'portrait'
ORIENT_SQUARE = 'square'

TARGET_SIZE = 1800

PARENT_NAME = 'Images'
NEW_PARENT = 'Images-Processed'

ALLOWED_FORMATS = ('jpg', 'jpe', 'jpeg', 'png', 'webp', 'psd', 'tif')

logger = open('missing.txt', 'a')


def kb_size(path: Path) -> int:
    """Return path's file size in kilobytes."""
    kb_file_size = path.stat().st_size / 1024
    return math.ceil(kb_file_size)


def replace_node(path: Path, node_name: str, new_node_name: str) -> Path:
    """Replaces node_name with new_node_name.

    Returns new path.
    If node_name is not found returns initial path.
    """
    parts = list(path.parts)

    try:
        node_index = parts.index(node_name)
    except ValueError:
        return path

    parts[node_index] = new_node_name

    return Path(*parts)


def detect_orientation(image: Image.Image) -> str:
    """Detect image orientation. Returns orientation const."""
    if image.width > image.height:
        return ORIENT_LANDSCAPE
    if image.width < image.height:
        return ORIENT_PORTRAIT
    return ORIENT_SQUARE


def _resize_horizontal(image: Image.Image, lowest_size: int) -> Image.Image:
    ratio = image.width / image.height
    new_width = round(lowest_size * ratio)
    new_height = lowest_size

    new_size = (new_width, new_height)

    return image.resize(new_size)


def _resize_vertical(image: Image.Image, lowest_size: int) -> Image.Image:
    ratio = image.height / image.width
    new_width = lowest_size
    new_height = round(lowest_size * ratio)

    new_size = (new_width, new_height)

    return image.resize(new_size)


def _resize_square(image: Image.Image, lowest_size: int) -> Image.Image:
    return image.resize((lowest_size, lowest_size))


def shrink_image(image: Image.Image, lowest_size: int) -> Image.Image:
    """Proportionally shrink image for its minimal size to match lowest_size.

    Returns resized image.
    """
    if min(image.size) <= lowest_size:
        return image

    resize_function = {
        ORIENT_PORTRAIT: _resize_vertical,
        ORIENT_LANDSCAPE: _resize_horizontal,
        ORIENT_SQUARE: _resize_square,
    }.get(detect_orientation(image))

    return resize_function(image, lowest_size)


# TODO: Remove if not needed
def _all_images(directory: Path) -> Iterator[Path]:
    jpgs, jpegs, pngs, webps, psds, tifs = map(
        lambda x: directory.rglob(f'*.{x}'), ALLOWED_FORMATS
    )
    return itertools.chain(jpgs, jpegs, pngs, webps, psds, tifs)


async def copy_file(path: Path, new_path: Path) -> None:
    """Copy file to new_path."""
    new_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, new_path)


async def save_image(image: Image.Image, image_path: Path) -> None:
    """Save image into image_path."""
    image_path.parent.mkdir(parents=True, exist_ok=True)

    # TODO: Check if image has transparent pixels.
    # image.save(image_path.with_suffix('.png'))
    # return

    image.save(image_path.with_suffix('.jpg'))


async def shrink_and_convert_one(image: Image.Image) -> Image.Image:
    """Shrink one image and convert it into needed format."""
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image = shrink_image(image, TARGET_SIZE)

    return image


async def process_one(path: Path) -> None:
    """Process one path."""
    new_path = replace_node(path, PARENT_NAME, NEW_PARENT)

    if path.suffix not in tuple(map(lambda x: f'.{x}', ALLOWED_FORMATS)):
        await copy_file(path, new_path)
        return

    try:
        image = Image.open(path)
    except UnidentifiedImageError:
        logger.write(f'{path}\n')
        raise
    image_converted = await shrink_and_convert_one(image)

    await save_image(image_converted, new_path)


async def process_directory(parent_dir: Path) -> None:
    """Recursively process whole directory."""
    # XXX: Why?
    global PARENT_NAME
    PARENT_NAME = parent_dir.stem

    all_images = parent_dir.glob('**/*.*')

    process_tasks = (process_one(image_path) for image_path in all_images)

    await asyncio.gather(*process_tasks)


def main(from_: Path) -> None:
    """Process all images from path."""
    asyncio.run(process_directory(from_))
    logger.close()

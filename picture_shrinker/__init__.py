from pathlib import Path

import cloup

from picture_shrinker.shrinker import Mode, process_picture


@cloup.command()
@cloup.argument(
    'path',
    type=cloup.Path(exists=True, readable=True, path_type=Path),
)
def main_cli(path: Path) -> None:
    """Shrink image(s) from path."""
    if path.is_dir():
        print("Can't process dirs for now")
        return

    mode = Mode.MULTIPLIER
    desired_size = 1800
    multiplier = 0.5

    print(path)
    process_picture(path, mode, multiplier)

from pathlib import Path

import cloup

from picture_shrinker.shrinker import Mode, process_picture


@cloup.command()
@cloup.argument(
    'path',
    type=cloup.Path(exists=True, readable=True, path_type=Path),
)
@cloup.option_group(
    'mode',
    cloup.option('--greater', metavar='SIZE', type=cloup.INT),
    cloup.option('--lesser', metavar='SIZE', type=cloup.INT),
    cloup.option('--multiplier', metavar='MULTIPLIER', type=cloup.FLOAT),
    constraint=cloup.constraints.RequireExactly(1),
)
def main_cli(path: Path, greater: int, lesser: int, multiplier: float) -> None:
    """Shrink image(s) from path."""
    if path.is_dir():
        print("Can't process dirs for now")
        return

    size: float

    if greater is not None:
        mode = Mode.GREATER_SIZE
        size = greater

    if lesser is not None:
        mode = Mode.LESSER_SIZE
        size = lesser

    if multiplier is not None:
        mode = Mode.MULTIPLIER
        size = multiplier

    print(path)
    process_picture(path, mode, size)

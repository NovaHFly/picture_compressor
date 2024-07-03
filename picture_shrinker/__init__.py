from pathlib import Path

import cloup


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

    print(path)

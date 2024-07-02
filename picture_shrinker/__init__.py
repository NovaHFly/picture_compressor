from pathlib import Path

import cloup


@cloup.command()
@cloup.argument(
    'path',
    type=cloup.Path(
        exists=True, readable=True, resolve_path=True, path_type=Path
    ),
)
def main_cli(path: Path):
    print(type(path))
    print(path)

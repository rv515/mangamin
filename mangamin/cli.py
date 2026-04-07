import click

from pathlib import Path

from mangamin import MangaMin


@click.command()
@click.argument("path", type=Path)
@click.option(
    "--quality",
    default=75,
    type=click.IntRange(10, 100, clamp=True),
    help="The quality of the output image.",
)
def cli(path: Path, quality: int) -> None:
    """A console application for reducing the size of manga by converting scans to webp format."""
    app = MangaMin(path=path.absolute(), quality=quality)
    app.start()

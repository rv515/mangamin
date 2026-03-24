import os
from pathlib import Path
from zipfile import ZipFile, is_zipfile
from rarfile import RarFile
from PIL import Image


def exclude_folders(path: Path) -> list[Path]:
    files = filter(lambda child: child.is_file() == True, path.rglob("*"))
    return sorted(files)


def unpack_archive(src: Path, dst: Path) -> None:
    if is_zipfile(src):
        with ZipFile(src) as zip:
            zip.extractall(path=dst)
    else:
        with RarFile(src) as rar:
            rar.extractall(path=dst)


def convert_image(file: Path, to_save: Path, quality: int) -> None:
    WEBP_MAX_SIZE = 16383
    with Image.open(file) as img:
        if max(img.size) > WEBP_MAX_SIZE:
            img.save(to_save.with_suffix(".jpeg"), "JPEG", quality=quality)
        else:
            img.save(to_save, "WEBP", quality=quality)


def pack_archive(folder: Path) -> None:
    os.chdir(folder)
    with ZipFile(Path(f"{folder}.zip"), "a") as zf:
        for child in Path().rglob("*"):
            zf.write(child)

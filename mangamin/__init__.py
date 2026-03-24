import shutil
import filetype

from enum import Enum
from pathlib import Path
from tqdm import tqdm

from mangamin.utils import exclude_folders, unpack_archive, convert_image, pack_archive


class FileType(str, Enum):
    JPG = "image/jpeg"
    PNG = "image/png"
    ZIP = "application/zip"
    RAR = "application/x-rar-compressed"


class MangaMin:
    def __init__(self, path: Path, quality: int) -> None:
        self.path = path
        self.quality = quality
        self.dest_dir = Path(self.path.parent, "MangaMin")

    def start(self) -> None:
        self.dest_dir.mkdir(exist_ok=True)

        bar = tqdm(
            exclude_folders(self.path),
            desc=self.path.name,
            bar_format="{desc}: {n_fmt}/{total_fmt}, elapsed time: {elapsed}",
        )

        for file in bar:
            self.file_prosessing(file)
            bar.write(f" {file.relative_to(self.path)}")

    def file_prosessing(self, file: Path) -> None:
        file_type = filetype.guess(file)
        if file_type is None:
            exit(1)
        match file_type.mime:
            case FileType.ZIP | FileType.RAR:
                self.archive_processing(file)
            case FileType.JPG | FileType.PNG:
                self.image_processing(file)
            case _:
                exit(2)

    def archive_processing(self, archive: Path) -> None:
        unpacking_folder = Path(archive.parent, archive.stem)
        unpack_archive(archive, unpacking_folder)
        for file in exclude_folders(unpacking_folder):
            self.file_prosessing(file)
        shutil.rmtree(unpacking_folder)
        loc_mini_imgs = Path(
            self.dest_dir, unpacking_folder.relative_to(self.path.parent)
        )
        pack_archive(loc_mini_imgs)
        shutil.rmtree(loc_mini_imgs)

    def image_processing(self, image: Path) -> None:
        to_save = Path(self.dest_dir, image.relative_to(self.path.parent)).with_suffix(
            ".webp"
        )
        to_save.parent.mkdir(parents=True, exist_ok=True)
        convert_image(image, to_save, self.quality)

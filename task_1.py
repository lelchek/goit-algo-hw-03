import sys
from pathlib import Path
import os
import shutil


def unique_name(path: Path) -> Path:
    counter = 1
    new_path = path

    while new_path.exists():
        new_path = path.with_name(f"{path.stem}({counter}){path.suffix}")
        counter += 1

    return new_path


def copy_file(path: Path, dest_dir: Path):
    ext = path.suffix.lstrip(".")

    if not ext:
        ext = "unknown"

    dest_ext_dir = dest_dir / ext
    dest_ext_dir.mkdir(exist_ok=True)
    dest_file = unique_name(dest_ext_dir / path.name)

    try:
        shutil.copy2(path, dest_file)
    except OSError as e:
        print(f"Error: cannot copy '{path}' to '{dest_file}'. Reason: {e}")


def read_src(path: Path, dest_dir: Path):
    if path.is_file():
        if not os.access(path, os.R_OK):
            print(f"Cannot read file {path}")

        else:
            copy_file(path, dest_dir)
            return

    if path.is_dir():
        if not os.access(path, os.R_OK):
            print(f"Cannot read directory {path}")
            return

        try:
            for p in path.iterdir():
                read_src(p, dest_dir)

        except OSError as e:
            print(f"Error: cannot read directory '{path}'. Reason: {e}")


def main():
    if len(sys.argv) < 2:
        print("Error: please provide source directory path")
        print("Usage: python script.py <source_dir> [dest_dir]")
        return

    src = Path(sys.argv[1])

    if not src.exists():
        print("Error: path does not exist")
        return

    if not src.is_dir():
        print("Error: path is not a directory")
        return

    if not os.access(src, os.R_OK):
        print("Error: no read permissions for source directory")
        return

    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")

    if dest.exists():
        if dest.is_file():
            print(f"Error: destination '{dest}' is a file, not a directory.")
            return

        if not os.access(dest, os.W_OK):
            print(f"Error: destination directory '{dest}' is not writable.")
            return

    else:
        parent = dest.parent
        if not os.access(parent, os.W_OK):
            print(
                f"Error: cannot create directory '{dest}' — parent '{parent}' is not writable."
            )
            return

    src_resolved = src.resolve()
    dest_resolved = dest.resolve()

    if dest_resolved.is_relative_to(src_resolved):
        print("Error: destination directory cannot be inside source directory.")
        return

    try:
        dest.mkdir(parents=True, exist_ok=True)

    except OSError as e:
        print(f"Error: cannot create destination directory '{dest}'. Reason: {e}")

    read_src(src, dest)


if __name__ == "__main__":
    main()

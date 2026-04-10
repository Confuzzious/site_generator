import os
import shutil
import sys

from gencontent import generate_pages_recursive


def copy_static_to_public(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)

        else:
            copy_static_to_public(from_path, dest_path)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_static_to_public("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)


main()

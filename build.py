import contextlib
import os

from shutil import copy, copytree, rmtree, make_archive


def clean_build_dir():
    print('Cleaning up old build files...')
    with contextlib.suppress(FileNotFoundError):
        os.remove('.venv/Lib/site-packages/taps_aff.py')
        rmtree('.venv/Lib/site-packages/app')


def copy_app_to_build_dir():
    print('Copying app to build dir...')
    copy('taps_aff.py', '.venv/Lib/site-packages')
    copytree('app', '.venv/Lib/site-packages/app')


def build_app():
    print('Build app...')
    make_archive('dist/taps_aff.zip', 'zip', '.venv/Lib/site-packages')


if __name__ == '__main__':
    clean_build_dir()
    copy_app_to_build_dir()
    build_app()

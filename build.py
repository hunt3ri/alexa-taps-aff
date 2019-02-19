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
    print('Building app...')
    make_archive('dist/taps_aff.zip', 'zip', '.venv/Lib/site-packages')


if __name__ == '__main__':
    """ Little helper util to make process of creating a deployable faster.  .zip is created in local dist folder"""
    clean_build_dir()
    copy_app_to_build_dir()
    build_app()

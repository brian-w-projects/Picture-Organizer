from os import chdir, listdir, rename, walk, getcwd
from os.path import isfile, splitext, join, basename, isdir
from math import log, ceil
import argparse


class PictureOrganizer:

    def __init__(self, pathway, **kwargs):
        self.pathway = pathway
        self.options = kwargs
        if not isdir(self.pathway):
            raise ValueError('Provided pathway does not exist')

    def rename_folders(self):
        if self.options.get('recurse'):
            for root, dirs, _ in walk(self.pathway):
                for directory in dirs:
                    if directory not in self.options.get('folder_skip', []) and not directory.startswith('.'):
                        self.rename_folder(join(root, directory))
        self.rename_folder(self.pathway)

    def rename_folder(self, path=None):
        if path is None:
            path = self.pathway

        print(f'Renaming {path}')
        current_directory = getcwd()
        chdir(path)

        files = [f for f in listdir(path) if isfile(f) and splitext(f)[-1][1:] not in self.options.get('ext_skip', [])
                 and not f.startswith('.')]
        file_name_base = basename(path).lower().replace(' ', '_')
        digits = ceil(log(len(files), 10)) if len(files) > 0 else 0

        for i, file in enumerate(files, 1):
            new_name = f'{file_name_base}_{str(i).zfill(digits)}{splitext(file)[1]}'
            if not self.options.get('simulate'):
                rename(file, new_name)
            if self.options.get('verbose') or self.options.get('simulate'):
                print(f'Renaming {file} to {new_name}')

        chdir(current_directory)
        print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename files in folders for consistent naming schemes.')
    parser.add_argument('pathway', action='store', help='Folder pathway to modify. May contain other folders.')
    parser.add_argument('-e', nargs='*', dest='ext_skip', action='store',
                        help='List of extensions to skip')
    parser.add_argument('-f', nargs='*', dest='folder_skip', action='store',
                        help='List of folders to skip')
    parser.add_argument('-r', dest='recurse', action='store_true', default=False,
                        help='Identify whether to recurse through inner folders')
    parser.add_argument('-v', dest='verbose', action='store_true', default=False,
                        help='Verbose Output')
    parser.add_argument('-s', dest='simulate', action='store_true', default=False,
                        help='Simulates renaming (does not actually rename). Used for testing before changing names')

    po = PictureOrganizer(**vars(parser.parse_args()))
    po.rename_folders()

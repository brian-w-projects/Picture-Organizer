from os import chdir, listdir, getcwd, rename, walk
from os.path import isdir, split, isfile, splitext, join, dirname, basename
from math import log, ceil
import argparse


def rename_folder(working_path, base_name, skip_list=()):
    print('Working {}'.format(working_path))
    if isdir(working_path):
        chdir(working_path)
        files = [file for file in listdir(working_path) if isfile(file) and splitext(file)[-1] not in skip_list
                 and not file.startswith('.')]
        digits = ceil(log(len(files), 10)) if len(files) > 0 else 0
        for i in range(len(files)):
            file_name, file_ext = splitext(files[i])
            if file_ext not in skip_list:
                new_name = '{}_{}{}'.format(base_name, str(i).zfill(digits), file_ext)
                rename(files[i], new_name)
                print('Renaming {} to {}'.format(file_name, splitext(new_name)[0]))
        print('done...')
    else:
        print('Path does not exist')


def rename_folders(working_path, identify, skip_list, folder_skip_list):
    name_changes = {}
    for root, dirs, _ in walk(working_path):
        for d in [x for x in dirs if x not in folder_skip_list and not x.startswith('.')]:
            new_name = naming(root, d, identify)
            if new_name:
                name_changes[join(root, d)] = new_name
    for full_path in name_changes.keys():
        rename_folder(full_path, base_name=name_changes[full_path], skip_list=skip_list)


def naming(root, d, identify):
    full_path = join(root, d)
    if identify:
        new_name = input('"{}" should be labeled as: '.format(full_path)).replace(' ', '_')
        if new_name:
            return new_name
        else:
            print('Skipping "{}"'.format(full_path))
            return
    else:
        return d.lower().replace(' ', '_')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename files in folders for consistent naming schemes.')
    parser.add_argument('pathway', action='store', help='Folder pathway to modify. May contain other folders.')
    parser.add_argument('-i', action='store_true', dest='identify', default=False,
                        help='Identify file naming scheme. Default will use containing folder name.')
    parser.add_argument('-s', nargs='*', dest='skip', action='store',
                        help='List of extensions to skip')
    parser.add_argument('-f', nargs='*', dest='folder_skip', action='store',
                        help='List of folders to skip')
    parser.add_argument('-r', dest='recurse', action='store_true', default=False,
                        help='Identify whether to recurse through inner folders')
    results = parser.parse_args()

    if results.recurse:
        rename_folders(results.pathway, results.identify, results.skip or [], results.folder_skip or [])
    else:
        new_name = naming(dirname(results.pathway), basename(results.pathway), results.identify)
        if new_name:
            rename_folder(results.pathway, new_name, results.skip or [])

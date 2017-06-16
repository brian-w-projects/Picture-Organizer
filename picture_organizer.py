from os import chdir, listdir, getcwd, rename, walk
from os.path import isdir, split, isfile, splitext, join
from math import log
import argparse


def rename_folder(working_path, base_name='', skip_list=()):
    print('Working {}'.format(working_path))
    if isdir(working_path):
        chdir(working_path)
        base_name = base_name or split(getcwd())[-1].replace(' ', '_')
        files = [file for file in listdir(working_path) if isfile(file) and splitext(file)[-1] not in skip_list
                 and not file.startswith('.')]
        digits = int(log(len(files)))
        for i in range(len(files)):
            file_name, file_ext = splitext(files[i])
            if file_ext not in skip_list:
                new_name = '{}_{}{}'.format(base_name, str(i).zfill(digits), file_ext)
                rename(files[i], new_name)
                print('Renaming {} to {}'.format(file_name, splitext(new_name)[0]))
        print('done...')
    else:
        print('Path does not exist')


def rename_folders(working_path, identify, skip_list, folder_skip_list=()):
    name_changes = {}
    for root, dirs, files in walk(working_path):
        for d in [x for x in dirs if x not in folder_skip_list]:
            full_path = join(root, d)
            if identify:
                new_name = input('"{}" should be labeled as: '.format(full_path)).replace(' ', '_')
                if new_name:
                    name_changes[full_path] = new_name
                else:
                    print('Skipping {}'.format(full_path))
            else:
                name_changes[full_path] = d.lower()
    for full_path in name_changes.keys():
        rename_folder(full_path, base_name=name_changes[full_path], skip_list=skip_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename files in folders for consistent naming schemes.')
    parser.add_argument('pathway', action='store', help='Folder pathway to modify. May contain other folders.')
    parser.add_argument('-i', action='store_true', dest='identify', default=False,
                        help='Identify file naming scheme. Default will use containg folder name.')
    parser.add_argument('-s', nargs='*', dest='skip', action='store',
                        help='List of extensions to skip')
    parser.add_argument('-f', nargs='*', dest='folder_skip', action='store',
                        help='List of folders to skip')
    results = parser.parse_args()

    rename_folders(results.pathway, results.identify, results.skip or [], results.folder_skip or [])

<h1>Picture Organizer</h1>
<h2>Quick Script for renaming files for better organization</h2>

<pre>
usage: picture_organizer.py [-h] [-i] [-s [SKIP [SKIP ...]]]
                            [-f [FOLDER_SKIP [FOLDER_SKIP ...]]]
                            pathway

Rename files in folders for consistent naming schemes.

positional arguments:
  pathway               Folder pathway to modify. May contain other folders.

optional arguments:
  -h, --help            show this help message and exit
  -i                    Identify file naming scheme. Default will use containg
                        folder name.
  -s [SKIP [SKIP ...]]  List of extensions to skip
  -f [FOLDER_SKIP [FOLDER_SKIP ...]]
                        List of folders to skip
</pre>
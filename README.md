<h1>Picture Organizer</h1>
<h3>This program will rename files inside an indicated folder. Great for organizing photos.</h2>

<pre>
usage: picture_organizer.py [-h] [-s [EXT_SKIP [EXT_SKIP ...]]]
                            [-f [FOLDER_SKIP [FOLDER_SKIP ...]]] [-r] [-v]
                            pathway

Rename files in folders for consistent naming schemes.

positional arguments:
  pathway               Folder pathway to modify. May contain other folders.

optional arguments:
  -h, --help            show this help message and exit
  -s [EXT_SKIP [EXT_SKIP ...]]
                        List of extensions to skip
  -f [FOLDER_SKIP [FOLDER_SKIP ...]]
                        List of folders to skip
  -r                    Identify whether to recurse through inner folders
  -v                    Verbose Output
</pre>
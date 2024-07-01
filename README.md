# compass
This is a folder-mapping software meant for folder structures that would otherwise be tedious to navigate.

It shows folders in a given directory, as well as the sub-folders (up to three levels "deep", up to 15 rows per subfolder-tree).

![Image showing two embedded proxies in conversation](/screenshot.png)

## Features
- Click a folder to open it in the file explorer.
- Right-click to select a new folder as the default directory, or input a directory manually.
- Four color schemes including a colorblind-optimized one.

## Usage
Currently Linux-only, but there's plans to make a Windows release as well.
Download the newest release, unzip, run "main". (Alternatively, if you use source code directly, you'll need wxPython.)

## Notes
Not tested with significantly larger folder structures *yet.* Works for most directories with a soft(?) suggested(?) max of 40 subfolders on the first level - can't guarantee it'll work past that. *Yet.*

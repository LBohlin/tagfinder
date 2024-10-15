# tagfinder
This is a quick and dirty prototype to allow tagging of arbitrary folders with keywords and render a preview picture.

## function
The program uses find to search for files named info.txt and associates included keywords with a preview picture (represented by a symbolic link named pic).

## dependencies
The program is written in python3 and uses tkinter, pil and pil.imagetk. dep.sh can be used to install the needed dependencies on debian(bookworm).

## todo
Quite a bit. This is only a proof of concept at this time. The base structure needs a rework, the distances of object are hard coded, etc.

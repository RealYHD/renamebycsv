# renamebycsv

A simple program that renames files by using a spreadsheet in CSV format as a dictionary for the files to be renamed.

## Features

 - Rename files recursively within a directory to a desired string
 - Desired string is set by a CSV where one column is the original string, and another column is the string to replace the original string with
 - Uses a REGEX capture group to select file and the portion of the filename to rename
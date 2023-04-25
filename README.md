# renamebycsv

A simple program that renames files by using a spreadsheet in CSV format as a dictionary for the files to be renamed.

## Features

 - Rename files recursively within a directory to a desired string
 - Replace only the REGEX match portion
 - Desired string is set by a CSV where one column is the original string, and another column is the string to replace the original string with
 - Uses a REGEX capture group to select file and the portion of the filename to rename
 - Ability to define file extension

## Installing using `pip`

1. Run `pip install --index-url https://git.reslate.systems/api/packages/ydeng/pypi/simple renamebycsv` in any `python3` enabled terminal.

2. Run `renamebycsv -h` to see the help and confirm installation was successful.

## Advanced Usage: What is REGEX?

This program makes heavy use of REGEX, also known as Regular Expression to give users the flexibility to choose which portion of any given filename should be the portion used by the program to look up in the CSV. It is therefore critical for users of this script to understand how REGEX works. Here are some key pointers to get you started:

 - REGEX works by matching one string to another, this is just like if you used any in-text search function.
 - Where it differs is the ability to use one REGEX string to match many strings.
   - i.e, the REGEX "`abc\d+`" will match with "`abc1`", "`abc2`", "`abc12`", but not "`ac12`" or "`abc`".
 - Many characters can be used as normal and will match a string literally (character for character), but some will be treated as special characters (such as the previously used `\`, which indicates that the letter afterwards should be treated specially, such as a token)
   - Common tokens to be aware of: `.` for any character, `\d` for single digits, `\w` for word characters, `\s` for space characters (tabs, spaces, linebreaks, etc.). Tokens can be repeated by using `+`, indicating "one or more", `*` indicating "none or more".
 - A capture group is a way of "selecting" a part of a text and is formed by using `(` and `)` around the REGEX that should be selected.

 Now for a few examples:

Let's say we have files `run325-a-1.vcf`, `run326-b-2.vcf`, and `run327-b-3.vcf`. If we know that all that matters is the `1` after the `run[numbers]-[character]-`, we can write `run\d+-\w-(\d).vcf` which will match with all 3 of the above examples, and select the last digit. The program can then use a given CSV to look up the selected digits and replace the name with what is given by the CSV.

For learning and testing your own REGEX, checkout [regex101.com](https://regex101.com/), which allows you to write the strings that you're trying to match, and the REGEX. It will show you live which parts of the strings match to what, if any parts match.
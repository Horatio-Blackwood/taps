# Author:       Adam Anderson
# Date:         Mar 24, 2016
# Module:       tools.py
# Python:       3.4.2

def read_word_file(file):
    """
    Reads a file full of words (one word per line) and puts them into a list.  Any lines that begin with a '#'
    character are ignored.

    :rtype: List of words read in from the file.
    """
    words = []
    with open(file, 'r') as wordfile:
        w = wordfile.readlines()

    for word in w:
        word = word.strip()
        if not word.startswith("#") and len(word) > 0:
            words.append(word.lower())

    return words



def sort_file(infile, outfile=None):
    """
    Reads in a file line by line, and sorts the lines alphabetically.

    :param infile -  the name of the file that has lines to be sorted.
    :param outfile - the name of the file to write the data to, if no file is provided writes to the same
                     file name as inflie.

    :return: None -  but does write out the sorted file
    """
    words = read_word_file(infile)
    words.sort()

    out = infile
    if outfile is not None:
        out = outfile

    with open(out, 'w') as writefile:
        for word in words:
            writefile.write(word)
            writefile.write("\n")
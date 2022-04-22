from os import path, makedirs, listdir
from click import echo


def read_dir(dir, filter):
    """Reads a list of files from a directory filtered by the provided string.

    :param dir: directory path
    :type dir: string
    :param filter: a filter string to limit results
    :type filter: string
    :return: a list of file paths OR False
    :rtype: list or False

    """
    from fnmatch import fnmatch
    dir = path.expanduser(dir)
    echo(dir)
    if not path.exists(dir):
        echo(f'no directory: {dir}')
        return False

    files = []

    for f in listdir(dir):
        fp = path.join(dir, f)
        if path.isfile(fp) and fnmatch(f, filter):
            files.append(fp)

    return files


def create_dir(dir):
    """Creates a directory structure if none exists.

    :param dir: directory path
    :type dir: string
    """
    echo(f'creating directory: {dir}')
    if not path.exists(dir):
        makedirs(dir)
    else:
        echo('directory exists... skipping')


def read_to_array(fp):
    """Reads the contents of a file to an array (list) seperated by line.

    :param fp: path to file
    :type fp: string
    :return: list of the contents of the file
    :rtype: list<string>

    """
    fp = path.expanduser(fp)
    if not path.exists(fp):
        echo(f'path does not exist: {fp}')
        return []
    echo('title file found, reading contents')
    file = open(fp, 'r')
    titles = file.read().splitlines()
    file.close()
    return titles

from os import path, makedirs, listdir
from click import echo


def read_dir(dir, filter):
    """Reads files from a directory.

    Parameters
    ----------
    dir : <string>
        Path of directory.
    filter : <string>
        Filter for valid files.

    Returns
    -------
    <array> or False
        An array of the contents of the directory that match the filter.
        Returns false if the directory does not exist.
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
    """Creates a directory.

    Parameters
    ----------
    dir : <string>
        Path to directory.
    """
    echo(f'creating directory: {dir}')
    makedirs(dir)


def read_to_array(fp):
    fp = path.expanduser(fp)
    if not path.exists(fp):
        echo(f'path does not exist: {fp}')
        return []
    echo('title file found, reading contents')
    file = open(fp, 'r')
    titles = file.read().splitlines()
    file.close()
    return titles

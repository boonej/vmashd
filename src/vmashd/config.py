import configparser
import shutil


def load():
    """Reads the application configuration file. If the file does not exist,
    a default file is created.

    Returns
    -------
    <ConfigParser>
        Parsed configuration file containing folder locations and environment
        details.

    """
    from os import path
    config_file = path.expanduser('~') + '/.videoautomator.ini'

    if not path.isfile(config_file):
        shutil.copyfile('default_config.ini', config_file)

    config = configparser.ConfigParser()
    config.read(config_file)
    return config

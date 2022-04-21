import configparser
import shutil
import click
from os import path

config_file = path.expanduser('~') + '/.vmashd.ini'


def load():
    """Reads the application configuration file. If the file does not exist,
    a default file is created.

    Returns
    -------
    <ConfigParser>
        Parsed configuration file containing folder locations and environment
        details.

    """
    global config_file

    if not path.isfile(config_file):
        shutil.copyfile('default_config.ini', config_file)

    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def show_config():
    """Displays the location and current configuration of the config file.
    """
    global config_file
    config = load()
    click.echo(f'The configuration file can be modified at {config_file}')
    for section in config.sections():
        click.echo(f'\n[{section}]')
        for(k, v) in config.items(section):
            click.echo(f'{k:20}{v}')

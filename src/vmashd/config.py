import configparser
import click
from os import path
from click import echo

config_file = path.expanduser('~') + '/.vmashd.ini'


def create_config():
    """Creates a config file with default parameters.

    """
    global config_file
    config = configparser.ConfigParser()
    config['Environment'] = {
            'LogLevel': 'Warning',
            'TempDirectory': path.expanduser('~/va_temp'),
        }
    config['Video'] = {
            'Directory': path.expanduser('~/va_video'),
            'Filter': '*.m*',
            'Width': 854,
            'Height': 480,
            'Unweighted': '*uw_*',
            'Captions': path.expanduser('~/va_video/captions.txt'),
            'MinLength': 0.8,
            'MaxLength': 4.8,
        }
    config['Audio'] = {
            'Directory': path.expanduser('~/va_audio'),
            'Filter': '*.mp3'
        }

    with open(config_file, 'w') as fobj:
        config.write(fobj)
    echo(f'created config file at {config_file}')


def load():
    """Reads the application configuration file. If the file does not exist,
    a default file is created.

    :return: current configuration file contents
    :rtype: ConfigParser

    """
    global config_file

    if not path.isfile(config_file):
        create_config()

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

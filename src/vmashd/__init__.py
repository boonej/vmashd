import click
import vmashd.main as main

__version__ = '0.1.0'
__author__ = 'Jonathan Boone'


@click.command()
@click.option(
    '--randomeffects',
    default=True,
    help='Include random video effects'
    )
@click.option(
    '--motionblur',
    default=True,
    help='Add motion blur to all frames'
    )
def avcollage(randomeffects):
    main.makemusicvideo()


@click.command()
def config():
    print('To implement')

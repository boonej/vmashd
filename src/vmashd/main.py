from vmashd.audioutility import AudioUtility
from vmashd.videoutility import VideoUtility
import vmashd.config as config
import logging
import click

logger = logging.getLogger('videoautomator')
logger.setLevel(logging.DEBUG)
logger.info("created logger")


@click.group()
def cli():
    pass


@click.command()
@click.argument(
    '--randfx/--no-randfx',
    default=False,
    help='Applies a random video effect to a subset of clips.'
)
@click.option(
    '--blur/--no-blur',
    default=True,
    help='Applies motion blur to resulting video.'
    )
def musicvid(randomeffects, motionblur):
    """Instructs vmashd to create a video collage set to music. The length of
    the is set by concatenating the audio found in the audio directory
    specified in the configuration file.
    """
    cfg = config.load()
    audio = AudioUtility(cfg).load()
    print("Audio duration: %f" % audio.duration)
    vu = VideoUtility(cfg)
    if (vu.video_with_length(audio.duration)):
        vu.add_audio(audio)


cli.add_command(musicvid)

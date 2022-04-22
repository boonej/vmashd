import vmashd.audioutility as au
import vmashd.videoutility as vu
from vmashd.files import read_to_array, read_dir, create_dir
import vmashd.config as vconfig
import click
from click import echo
from os import path
import random

_randfx = False
_blur = False
cfg = vconfig.load()


def load_audio():
    """Loads and concatenates audio files from directory.

    :return: concatenated audio files
    :rtype: moviepy.editor.AudioClip

    """
    global cfg
    afl = au.load_audio(cfg['Audio']['Directory'], cfg['Audio']['Filter'])
    if not afl:
        echo('no files present... please add files to the audio directory')
        return False
    audio = au.join_audio(afl)
    echo("Audio duration: %f" % audio.duration)
    return audio


def load_videos():
    """Loads an array of video files weighted by length

    :return: List of video clips
    :rtype: list
    """
    global cfg
    vfl = read_dir(cfg['Video']['Directory'], cfg['Video']['Filter'])
    if not vfl:
        create_dir(cfg['Video']['Directory'])
        return False
    size = (
        float(cfg['Video']['Width']),
        float(cfg['Video']['Height'])
        )
    vl = vu.load_video(vfl, size)
    return vu.weight_videos(vl, vfl, cfg['Video']['Unweighted'])


def load_video_clip(vids):
    """Loads a short clip to include in video collage

    :param vids: list of video files
    :type vids: list

    :return: a short video clip
    :rtype: moviepy.editor.VideoClip
    """
    global _randfx
    video = random.choice(vids)
    return vu.video_clip(
        video,
        float(cfg['Video']['MinLength']),
        float(cfg['Video']['MaxLength']),
        _randfx)


def video_with_duration(duration):
    """Collects video clips until a specified duration is achieved

    :param duration: targeted length of video
    :type duration: float

    :return: list of video clips to include in video
    :rtype: list
    """
    time = 0.0
    vids = load_videos()
    if not vids:
        return False
    output = []
    while time < duration:
        v = load_video_clip(vids)
        time = float(time) + float(v.duration)
        output.append(v)
    return output


def write_video(varray, audio, filepath):
    """ writes video to file

    :param varray: array of videos
    :type varray: list

    :param audio: audio file to merge with video
    :type audio: moviepy.editor.AudioClip

    :param filepath: path to output file
    :type filepath: string
    """
    global _blur
    vu.write_videofile(
        varray,
        audio,
        filepath,
        _blur,
        cfg['Environment']['TempDirectory']
    )
    return


def write_tempvideo(varray, filepath):
    """Writes video to a temporary file

    :param varray: array of clips to write
    :type varray: list
    :param filepath: output file path
    :type filepath: string
    """
    write_video(varray, False, filepath)
    return


@ click.group()
def cli():
    pass


@ click.command()
@ click.option(
    '--randfx/--no-randfx',
    default=False,
    help='Applies a random video effect to a subset of clips.'
    )
@ click.option(
    '--blur/--no-blur',
    default=True,
    help='Applies motion blur to resulting video.'
    )
@click.option(
    '--filename', '-f',
    default='video.mp4',
    help='Output file name for process'
    )
def mash(randfx, blur, filename):
    """Instructs vmashd to create a video collage set to music. The length of
    the is set by concatenating the audio found in the audio directory
    specified in the configuration file.

    :param randfx: determines if effects are applied at random
    :type randfx: bool
    :param blur: determines if a blur effect is applied [not implemented]
    :type blur: bool
    :param filename: path to output the final file
    :type filename: string
    """
    global _randfx, _blur, cfg
    _randfx = randfx
    _blur = blur
    audio = load_audio()
    if not audio:
        return
    vu.set_titles(read_to_array(cfg['Video']['Captions']))
    vids = video_with_duration(audio.duration)
    if not vids:
        echo('no video files, exiting')
        return
    echo('writing temp file')
    tempfile = path.join(
        path.expanduser(cfg['Environment']['TempDirectory']),
        'temp.mp4'
        )
    write_tempvideo(vids, tempfile)
    v = vu.read_videofile(tempfile)
    echo('writing file with audio')
    write_video(v, audio, path.expanduser(filename))


@click.command()
def config():
    """Displays the location and current contents of the config file.
    """
    vconfig.show_config()


@click.command()
def makedirs():
    """Creates all directories listed in the config file.
    """
    global cfg
    video_dir = cfg['Video']['Directory']
    audio_dir = cfg['Audio']['Directory']
    temp_dir = cfg['Environment']['TempDirectory']
    create_dir(video_dir)
    create_dir(audio_dir)
    create_dir(temp_dir)


cli.add_command(mash)
cli.add_command(config)
cli.add_command(makedirs)

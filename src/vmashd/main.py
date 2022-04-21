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
    """Loads audio files from directory.

    Returns
    -------
    <AudioClip>
        AudioClip of concatenated audio files.

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

    Returns
    -------
    <array>
        Array of VideoClips

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

    Parameters
    ----------
    vids : <array>
        Array of video files.

    Returns
    -------
    <VideoClip>
        A short video clip

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

    Parameters
    ----------
    duration : type
        Description of parameter `duration`.

    Returns
    -------
    type
        Description of returned object.

    """
    time = 0.0
    vids = load_videos()
    if not vids:
        return False
    output = []
    while time < duration:
        echo(f'current length is {time}')
        v = load_video_clip(vids)
        echo(f'file duration is {v.duration}')
        time = float(time) + float(v.duration)
        output.append(v)
    return output


def write_video(varray, audio, filepath):
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
    filepath = path.join(
        path.expanduser(cfg['Video']['OutputDirectory']),
        filename
        )
    write_video(v, audio, filepath)


@ click.command()
def config():
    """Displays the location and current contents of the config file.
    """
    vconfig.show_config()


cli.add_command(mash)
cli.add_command(config)

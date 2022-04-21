import random
import moviepy
import moviepy.video.fx.all as vfx
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from os import path
from click import echo
from vmashd.files import read_dir


titles = []


def set_titles(t):
    """Sets value for global titles object

    Parameters
    ----------
    t : <array>
        An array of caption strings.
    """
    global titles
    titles = t


def roll():
    """Generates a random integer from 0 - 100

    Returns
    -------
    <int>
        Integer between 0 and 100.

    """
    return random.uniform(0, 100)


def file_list(p, f):
    d = read_dir(p, f)
    if not d:
        echo('no files exist... exiting')
    return d


def load_video(dir, size):
    echo('load video directory')
    video = []
    for f in dir:
        if path.exists(f):
            video.append(VideoFileClip(f).resize(size))
    return video


def weight_videos(v, n, f):
    from math import ceil
    from fnmatch import fnmatch
    echo('weighting videos based on length')
    c = 0
    for i in range(0, len(n)):
        name = str(n[i])
        if fnmatch(name, f):
            c = 1
            echo(f'{name} will be excluded from weighting')
        else:
            c = ceil(v[i].duration/20)
            echo(f'{name} will be weighted {c}x')
        for it in range(0, c):
            v.append(v[it])
    return v


def has_titles():
    global titles
    return len(titles) > 0


def get_cliplength(titles, min, max):
    return random.uniform(min, max)


def get_title(v):
    global titles
    if (len(titles) == 0):
        echo('tried applying title but no titles found')
        return v
    echo('applying title effect')
    random.shuffle(titles)
    cap = titles.pop()
    txt_clip = TextClip(
        cap,
        method="caption",
        color='white',
        size=(600, 60),
        align="center",
        font="Keep-Calm-Medium",
        kerning=-2,
        interline=-1
        ).set_pos('center').set_duration(v.duration)
    return CompositeVideoClip([v, txt_clip])


def get_fx(v, r):
    if r < 10 or r > 90:
        return vfx.blackwhite(v)
    elif r > 90:
        d = v.duration * random.uniform(0.7, 1.8)
        m = 1
        if (d > 0):
            m = -1
        a = random.uniform(0.3, 1.0) * m
        s = random.uniform(0.6, 1.2)
        return vfx.accel_decel(v, d, a, s)
    return v


def video_clip(vid, min, max, fx):
    global titles
    r = roll()
    ht = r < 20 and has_titles()
    length = round(get_cliplength(ht, min, max), 2)
    start = round(random.uniform(0, vid.duration - length), 2)
    v = vid.subclip(start, start + length)

    if r < 20:
        v = get_title(v)
    if fx:
        v = get_fx(v, r)

    return v


def read_videofile(path):
    return VideoFileClip(path)


def write_videofile(v, a, filepath, blur, temp):
    temp = path.expanduser(temp)
    # TODO: Implement blur
    if not a:
        cv = moviepy.editor.concatenate_videoclips(v)
        cv.write_videofile(path.expanduser(filepath), audio=False)
    else:
        if v.duration > a.duration:
            v = v.subclip(0.0, a.duration)
        v.audio = a
        v = vfx.fadeout(v, 5.0)
        echo(f'writing video output to {path}')
        v.write_videofile(
                    path.expanduser(filepath),
                    audio_codec='aac',
                    temp_audiofile=path.join(
                        temp, 'audio.m4a'),
                    remove_temp=True
                    )

import random
import moviepy
import moviepy.video.fx.all as vfx
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from os import path
from click import echo
from vmashd.files import read_dir


titles = []


def set_titles(t):
    """Sets the global titles property

    :param t: list of title strings
    :type t: string

    """
    global titles
    titles = t


def roll():
    """Generates a random integer between 0 and 100.

    :return: random integer between 0 and 100
    :rtype: int

    """
    return random.uniform(0, 100)


def file_list(p, f):
    """Gets a list of video files from the video input directory.

    :param p: path to input directory
    :type p: string
    :param f: filter for excluded file types
    :type f: string
    :return: a list of the files or False
    :rtype: list<string> or False

    """
    d = read_dir(p, f)
    if not d:
        echo('no files exist... exiting')
    return d


def load_video(dir, size):
    """Loads a video and resizes it to the specified size.

    :param dir: list of files
    :type dir: list<string>
    :param size: size to resize videos
    :type size: tuple(float, float)
    :return: array of video clips
    :rtype: array<moviepy.editor.VideoClip>

    """
    echo('load video directory')
    video = []
    for f in dir:
        if path.exists(f):
            video.append(VideoFileClip(f).resize(size))
    return video


def weight_videos(v, n, f):
    """Weights videos according to duration, excluding files whose names match
    the filter conditions.

    :param v: list of video files
    :type v: list<moviepy.editor.VideoClip>
    :param n: list of video file names
    :type n: list<string>
    :param f: filter for files to exclude from weighting
    :type f: string
    :return: list of video files, weighted by length
    :rtype: list<moviepy.editor.VideoClip>

    """
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
    """Determines if titles are present.

    :return: True if titles are present
    :rtype: bool

    """
    global titles
    return len(titles) > 0


def get_cliplength(titles, min, max):
    """Gets targeted video clip duration.

    :param titles: whether there will be a title on the clip
    :type titles: bool
    :param min: minimum length of clip
    :type min: float
    :param max: maximum length of clip
    :type max: float
    :return: targeted length of clip
    :rtype: float

    """
    if (titles):
        return random.uniform(2.9, 3.6)
    return random.uniform(min, max)


def get_title(v):
    """Adds a title to a video clip.

    :param v: video clip
    :type v: moviepy.editor.VideoClip
    :return: video clip with title applied
    :rtype: moviepy.editor.VideoClip

    """
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
    """Creates a video clip with a random video effect applied if a random
    number falls within range.

    :param v: video clip
    :type v: moviepy.editor.VideoClip
    :param r: random number between 0 and 100
    :type r: int
    :return: video clip with fx applied if necessary
    :rtype: moviepy.editor.VideoClip

    """
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
    """Creates a video clip from a full length video.

    :param vid: full length video clip
    :type vid: moviepy.editor.VideoClip
    :param min: minimum length of clip
    :type min: float
    :param max: maximum length of clip
    :type max: float
    :param fx: determines if random effects are applied
    :type fx: bool
    :return: a video clip with any effects or titles applied
    :rtype: moviepy.editor.VideoClip

    """
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
    """Reads a video file from a specified path.

    :param path: path to video file
    :type path: string
    :return: video clip found at path
    :rtype: moviepy.editor.VideoClip

    """
    return VideoFileClip(path)


def write_videofile(v, a, filepath, blur, temp):
    """Writes a video to a specified output.

    :param v: video to write
    :type v: moviepy.editor.VideoClip
    :param a: audio to merge with video
    :type a: moviepy.editor.AudioClip
    :param filepath: output file path
    :type filepath: string
    :param blur: determines if blur is applied [not implemented]
    :type blur: bool
    :param temp: path to temporary directory
    :type temp: string

    """
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

from os import path
from moviepy.editor import AudioFileClip, CompositeAudioClip
from moviepy.audio.fx import all as afx
from click import echo
from vmashd.files import read_dir


def load_audio(p, f):
    """Short summary.

    :param p: directory path
    :type p: string
    :param f: file filter
    :type f: string
    :return: audio file
    :rtype: AudioClip

    """
    echo('reading audio directory')
    dir = read_dir(p, f)
    if not dir:
        return False
    audio = []
    for f in dir:
        if path.exists(f):
            audio.append(AudioFileClip(f, 200000, 2, 44100))
    return audio


def join_audio(audio):
    """Joins a set of audio clips into a single clip

    :param audio: list of audio files
    :type audio: list
    :return: a concatenated audio clip
    :rtype: moviepy.editor.AudioClip

    """
    echo('joining audio files')
    length = len(audio)
    if length == 0:
        return False
    elif length == 1:
        return afx.audio_normalize(audio[0])
    else:
        comp = []
        st = 0.00

        for a in audio:
            a.set_start(st)
            comp.append(a)
            st = st + a.duration
        return afx.audio_normalize(CompositeAudioClip(comp))

from videoautomator.audioutility import AudioUtility
from videoautomator.videoutility import VideoUtility
import videoautomator.config as config
import logging

logger = logging.getLogger('videoautomator')
logger.setLevel(logging.DEBUG)
logger.info("created logger")


def makemusicvideo():
    cfg = config.load()
    audio = AudioUtility(cfg).load()
    print("Audio duration: %f" % audio.duration)
    vu = VideoUtility(cfg)
    if (vu.video_with_length(audio.duration)):
        vu.add_audio(audio)


def add_audio():
    cfg = config.load()
    audio = AudioUtility(cfg).load()
    print("Audio duration: %f" % audio.duration)
    vu = VideoUtility(cfg)
    vu.add_audio(audio)

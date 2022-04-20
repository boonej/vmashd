import logging
import random
import moviepy
import moviepy.video.fx.all as vfx
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from os import path

module_logger = logging.getLogger('videoautomator.audioutility')


class VideoUtility(object):

    def __init__(self, config):
        print('initializing')
        self.folder = path.expanduser(config['Video']['Directory'])
        self.outputname = path.join(path.expanduser(
            config['Environment']['OutputDirectory']), 'video_out.mp4')
        self.temppath = path.expanduser(config['Environment']['TempDirectory'])
        self.tempfile = path.join(self.temppath, 'temp.mp4')
        self.titlepath = path.join(self.folder, 'titles.txt')
        self.titles = []
        self.ext = config['Video']['Filter']
        self.unweighted = config['Video']['Unweighted']
        self.accel_threshold = 80
        self.title_threshold = 15
        self.min_length = 1.20
        self.max_length = 4.8
        self.size = (
            float(config['Video']['Width']),
            float(config['Video']['Height'])
            )
        self.file_list = []
        self.outputs = []
        self.logger = logging.getLogger(
            'videoautomator.videoutility.VideoUtility')
        self.d_roll = 50

    def load_titles(self):
        if path.exists(self.titlepath):
            file = open(self.titlepath, 'r')
            self.titles = file.read().splitlines()
            file.close()
            print('Loaded title file')
        else:
            print('No title file found')

    def roll(self):
        self.d_roll = random.uniform(1, 100)

    def video_with_length(self, length, randomeffects, motionblur):
        self.logger.info("creating video with length: %f" % length)
        self.load_titles()
        self.target_length = length
        self.randomeffects = randomeffects
        self.motionblur = motionblur
        self.load_videos()
        self.outputs = []
        t = 0.00
        while (t < length):
            c = self.get_video_clip()
            t = t + c.duration
            self.outputs.append(c)
        print("Starting writing file with %f of video." % t)
        self.write_video_with_length(length)
        return True

    def add_audio(self, audio):
        self.logger.info("merging audio with video")
        self.audio = audio
        v = VideoFileClip(self.tempfile)
        if v.duration > audio.duration:
            v = v.subclip(0.0, audio.duration)
        v.audio = self.audio
        v = vfx.fadeout(v, 5.0)

        v.write_videofile(
            self.outputname,
            audio_codec='aac',
            temp_audiofile=path.join(self.temppath, 'audio.m4a'),
            remove_temp=True
            )

    def get_video_clip(self):
        self.roll()
        v = random.choice(self.videos)
        length = self.get_cliplength()
        start = round(random.uniform(0, v.duration - length), 2)
        clip = v.subclip(start, start + length)
        return self.apply_visualeffects(clip)

    def get_cliplength(self):
        if self.d_roll < self.title_threshold:
            return random.uniform(2.8, 4.0)
        return random.uniform(self.min_length, self.max_length)

    def read_videodir(self):
        print("reading input directory")
        self.logger.info("reading input directory")
        if not self.get_create_dir():
            return

    def get_create_dir(self):
        from os import path, makedirs, listdir
        from fnmatch import fnmatch
        vd = self.folder
        if not path.exists(vd):
            self.logger.info("%s does not exist... creating directory" % vd)
            makedirs(vd)
            self.logger.info("video directory created... exiting.")
            return False
        self.file_list = []
        for f in listdir(vd):
            fp = path.join(vd, f)
            if path.isfile(fp) and fnmatch(f, self.ext):
                self.file_list.append(fp)
        if len(self.file_list) > 0:
            self.logger.info("video files found... processing videos")
            return True
        else:
            print("no files present... exiting")
            return False

    def load_videos(self):
        self.read_videodir()
        self.logger.info('loading video data')
        self.videos = []
        for file in self.file_list:
            self.videos.append(VideoFileClip(file).resize(self.size))
        self.weight_videos()

    def weight_videos(self):
        self.logger.info('weighting videos based on length')
        from fnmatch import fnmatch
        from math import ceil
        for i in range(0, len(self.file_list)):
            name = str(self.file_list[i])
            if fnmatch(name, self.unweighted):
                count = 1
                print('{0} will be excluded from weighting'.format(name))
            else:
                count = ceil(self.videos[i].duration/50)
                print(
                    '{0} will be weighted {1} times an\
                    unweighted video'.format(
                        self.file_list[i], count
                      )
                    )
            for it in range(0, count):
                self.videos.append(self.videos[i])

    def apply_visualeffects(self, clip):
        if self.randomeffects:
            if self.d_roll < 10 or self.d_roll > 94:
                clip = self.desaturate(clip)
            if self.d_roll < 20:
                return self.title(clip)
            elif self.d_roll > 90:
                return self.accel(clip)
        return clip

    def desaturate(self, clip):
        return vfx.blackwhite(clip)

    def draw(self, clip):
        return vfx.painting(clip, saturation=2.0, black=0.000)

    def accel(self, clip):
        self.logger.info('applying accelleration effect')
        d = clip.duration * random.uniform(0.7, 1.8)
        m = 1
        if (d > 0):
            m = -1
        a = random.uniform(0.3, 1.0) * m
        s = random.uniform(0.6, 1.2)
        return vfx.accel_decel(clip, d, a, s)

    def get_title(self):
        """Returns a random caption from a captions file (if provided). The
        caption is removed from the store to avoid duplication.

        Returns
        -------
        <string>
            A random caption from provided captions file.

        """
        random.shuffle(self.titles)
        return self.titles.pop()

    def title(self, clip):
        """Adds a random title to the provided clip.

        Parameters
        ----------
        clip : <VideoFileClip>
            video clip to be processed

        Returns
        -------
        <VideoFileClip>
            video clip with the title applied

        """
        if (len(self.titles) == 0):
            print('tried applying title but no titles found')
            return clip
        print('applying title effect')
        t = self.get_title()
        txt_clip = TextClip(
            t,
            method="caption",
            color='white',
            size=(600, 60),
            align="center",
            font="Keep-Calm-Medium",
            kerning=-2,
            interline=-1).set_pos('center').set_duration(clip.duration)
        return CompositeVideoClip([clip, txt_clip])

    def write_video_with_length(self, length):
        cv = moviepy.editor.concatenate_videoclips(self.outputs)
        if self.motionblur:
            cv = vfx.supersample(cv, 1, 1)
            
        print("Video duration is %f" % cv.duration)
        cv.write_videofile(self.tempfile, audio=False)

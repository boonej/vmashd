import logging
from os import path, makedirs, listdir
from moviepy.editor import AudioFileClip, CompositeAudioClip
from moviepy.audio.fx import all as afx

module_logger = logging.getLogger('videoautomator.audioutility')


class AudioUtility(object):

    def __init__(self, config):
        self.config = config
        self.file_list = []
        self.audio = []
        self.dir = path.expanduser(self.config['Audio']['Directory'])
        self.filter = self.config['Audio']['Filter']
        self.logger = logging.getLogger(
            'videoautomator.audioutility.AudioUtility'
            )

    def load(self):
        """Primary method to loads audio from audio directory.

        Returns
        -------
        <AudioFileClip>
            Processed audio clip. If multiple files are present in directory,
            they will be concatenated with a slight crossfade.

        """
        self.logger.info('starting audio processing')
        return self.process_audio()

    def find_files(self):
        self.logger.info('finding audio files')
        from fnmatch import fnmatch

        if not path.exists(self.dir):
            self.logger.info(
                "%s does not exist... creating directory" % self.dir)
            makedirs(self.dir)
            self.logger.warning(
                "no audio directory, created %s - \
                add audio files and try again"
                % self.dir)
            return False

        self.file_list = []
        for f in listdir(self.dir):
            fp = path.join(self.dir, f)
            if path.isfile(fp) and fnmatch(f, self.filter):
                self.file_list.append(fp)
        if len(self.file_list) > 0:
            self.logger.info("video files found... processing videos")
            return True
        else:
            print("no files present... exiting")
            return False

    def load_audioclips(self):
        self.find_files()
        self.audio = []
        self.logger.info('loading audio clips')
        for f in self.file_list:
            self.audio.append(AudioFileClip(f, 200000, 2, 44100))

    def process_audio(self):
        self.load_audioclips()

        if len(self.audio) == 1:
            return afx.audio_normalize(self.audio[0])

        comp = []
        st = 0.00

        for a in self.audio:
            a.set_start(st)
            comp.append(a)
            st = a.duration

        return afx.audio_normalize(CompositeAudioClip(comp))

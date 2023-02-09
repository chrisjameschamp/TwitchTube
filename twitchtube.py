import logging
import multiprocessing
import os
import sys
import util

from util import colargulog, constants, dialogue, functions, streamlink

DEBUG = False

class twitchTube:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        dialogue.intro()
        self.location = os.path.dirname(os.path.realpath(__file__))
        self.preferences = functions.prefs()
        self.object = {}
        self.objectReset()
        self.twitch = util.twitch()
        self.ffmpeg = util.ffmpeg(self.location)
        self.ffmpeg.check()
        if self.preferences['youtube']['enable']:
            self.youtube = util.youtube()
        self.chooseVideo()

    def chooseVideo(self):
        video = self.twitch.getVideos()
        video['stream'] = streamlink.getStream(video['url'])
        self.object['video'] = video
        self.chooseOptions()

    def chooseOptions(self):
        self.object['options'] = self.ffmpeg.setOptions()
        if self.object['youtube']['unique']:
            self.object['youtube']['options'] = self.ffmpeg.setOptions(channel='youtube', options=self.object['options'])
        self.renderVideo()

    def renderVideo(self):
        if self.object['youtube']['unique'] and self.object['youtube']['options'] == self.object['options']:
            self.logger.info('Both Youtube and generic videos are the same')
            user_input = dialogue.query('Y/N', 'Would you like to render the generic video (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                self.ffmpeg.render(self.object)
                self.object['rendered'] = True
            else:
                self.logger.info('Skipping the generic render')
        else:
            self.ffmpeg.render(self.object)
            self.object['rendered'] = True
            
        if self.object['youtube']['enable']:
            self.ffmpeg.render(self.object, type='youtube')
        self.qcVideo()

    def qcVideo(self):
        if self.object['rendered']:
            if not self.ffmpeg.qc(self.object):
                self.chooseVideo()
        if self.object['youtube']['enable']:
            if not self.ffmpeg.qc(self.object, type='youtube'):
                self.chooseVideo()
        self.metadata()

    def metadata(self):
        if self.object['youtube']['enable']:
            self.object['meta'] = functions.setOptions(self.object['video'], self.youtube)
        if self.object['youtube']['enable']:
            self.uploadVideo()
        else:
            self.cleanUp()

    def uploadVideo(self):
        if self.object['youtube']['enable']:
            self.youtube.upload(self.object)
        self.cleanUp()

    def cleanUp(self):
        if self.object['rendered']:
            user_input = dialogue.query('Y/N', 'Would you like to save a copy of the generic rendered video to your computer (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                self.logger.info('Please select the destination folder...')
                folder_path = functions.selectDestFolder()
                filename, ext = os.path.splitext(self.object['video']['filename'])
                functions.copy(constants.RENDER_LOCATION+'generic/'+self.object['video']['filename'], folder_path+'/'+filename+'_gen'+ext, chunk_size=1024)
        if self.object['youtube']['enable']:
            user_input = dialogue.query('Y/N', 'Would you like to save a copy of the youtube rendered video to your computer (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                self.logger.info('Please select the destination folder...')
                folder_path = functions.selectDestFolder()
                filename, ext = os.path.splitext(self.object['video']['filename'])
                functions.copy(constants.RENDER_LOCATION+'youtube/'+self.object['video']['filename'], folder_path+'/'+filename+'_yt'+ext, chunk_size=1024)

        user_input = dialogue.query('Y/N', 'Would you like to process another video (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            self.chooseVideo()
        else:
            functions.closeTT()

    def objectReset(self):
        functions.cleanUp()
        self.object = {'video': {}, 'options': {}, 'rendered': False, 'youtube': self.preferences['youtube']}

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        DEBUG = True

    multiprocessing.freeze_support()
    
    # SETUP LOG LEVEL - DEBUG: debug message | INFO: info message | WARNING: warn message | ERROR: error message
    console_handler = logging.StreamHandler(stream=sys.stdout)
    if DEBUG:
        colored_formatter = colargulog.ColorizedArgsFormatter(constants.TERMINAL_FORMAT_DEBUG)
    else:
        colored_formatter = colargulog.ColorizedArgsFormatter(constants.TERMINAL_FORMAT, constants.TERMINAL_DATE_FMT)
    console_handler.setFormatter(colored_formatter)
    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger()
    logger.name = 'TwitchTube'
    logger.addHandler(console_handler)
    if DEBUG:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug('-------------------DEBUG ACTIVE-------------------')

    try:
        twitchTube()
    except Exception as e:
        logger.error('{}', e)
    except KeyboardInterrupt:
        logger.info('Exiting...')
    finally:
        sys.exit()
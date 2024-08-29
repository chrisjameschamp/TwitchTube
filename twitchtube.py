import logging
import multiprocessing
import os
import sys
import util

from util import colargulog, constants, dialogue, functions, streamlink

DEBUG = True

class twitchTube:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        dialogue.intro()
        self.location = os.path.dirname(os.path.realpath(__file__))
        self.object = {}
        self.objectReset()
        self.twitch = util.twitch()
        self.ffmpeg = util.ffmpeg(self.location)
        self.ffmpeg.check()
        self.chooseVideo()

    def chooseVideo(self):
        video = self.twitch.getVideos()
        video['stream'] = streamlink.getStream(video['url'])
        self.object['video'] = video
        self.chooseOptions()

    def chooseOptions(self):
        self.object['options'] = self.ffmpeg.setOptions()
        self.renderVideo()

    def renderVideo(self):
        self.ffmpeg.render(self.object)
        self.object['rendered'] = True
        self.qcVideo()

    def qcVideo(self):
        if self.object['rendered']:
            if not self.ffmpeg.qc(self.object):
                self.chooseVideo()
        self.metadata()

    def metadata(self):
        self.object['meta'] = functions.setOptions(self.object['video'])
        self.uploadVideo()

    def uploadVideo(self):
        functions.uploadVideo(self.object)
        self.cleanUp()

    def cleanUp(self):
        user_input = dialogue.query('Y/N', 'Would you like to process another video (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            self.chooseVideo()
        else:
            functions.closeTT()

    def objectReset(self):
        functions.cleanUp()
        self.object = {'video': {}, 'options': {}, 'rendered': False}

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
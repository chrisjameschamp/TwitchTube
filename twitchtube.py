import util

from util import constants

class twitchTube:
    def __init__(self):

        util.intro()

        self.object = {}
        self.objectReset()

        self.twitch = util.twitch()
        self.ffmpeg = util.ffmpeg()
        self.youtube = util.youtube()
        
        progress = util.getFile('progress')
        if progress:
            user_input = util.query('Y/N', 'Would you like to continue where you previously left off (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                self.object = progress
                if not self.object['options']:
                    self.chooseOptions()
                elif not self.object['rendered']:
                    self.renderVideo()
                elif not self.object['qc']:
                    if self.ffmpeg.verifyFile(self.object['video']['filename']):
                        self.qcVideo()
                    else: 
                        self.renderVideo()
                elif self.object['youtube'] is None:
                    self.youtubeOptions()
                elif not self.object['metadata']:
                    self.metadata()
                elif not self.object['yt_uploaded']:
                    if self.ffmpeg.verifyFile(self.object['video']['filename']):
                        self.uploadVideo()
                    else:
                        self.renderVideo()
                else:
                    self.cleanUp()
            else:
                util.deleteProgress(progress)
                self.objectReset()
                self.chooseVideo()
        else:
            print('Starting Fresh\n')
            self.chooseVideo()

    def chooseVideo(self):
        video = self.twitch.getVideos()
        video['stream'] = util.getStream(video['url'])
        self.object['video'] = video
        util.saveFile('progress', self.object)
        self.chooseOptions()

    def chooseOptions(self):
        self.object['options'] = self.ffmpeg.setOptions(self.object['video'])
        util.saveFile('progress', self.object)
        self.renderVideo()

    def renderVideo(self):
        if self.ffmpeg.render(self.object):
            self.object['rendered'] = True
        util.saveFile('progress', self.object)
        self.qcVideo()

    def qcVideo(self):
        if self.ffmpeg.qc(self.object):
            self.object['qc'] = True
            self.youtubeOptions()
        else:
            util.deleteProgress(self.object)
            self.chooseVideo()

    def youtubeOptions(self):
        prefs = util.getFile(constants.PREFS_FILE)

        if prefs is not None and 'youtube' in prefs and prefs['youtube']:
            user_input = util.query('Y/N', 'Would you like to upload to youtube again (Y/n)? ', default='Y', prePrint='Your current preferences are to upload to Youtube.')
            if user_input.casefold().startswith('y'):
                prefs = {'youtube': True}
            else:
                prefs = {'youtube': False}
        elif prefs is not None and 'youtube' in prefs:
            user_input = util.query('Y/N', 'Would you like to upload to youtube this time(y/N)? ', default='N', prePrint='Your current preferences are to NOT upload to Youtube.')
            if user_input.casefold().startswith('y'):
                prefs = {'youtube': True}
            else:
                prefs = {'youtube': False}
        else:
            user_input = util.query('Y/N', 'Would you like to upload the resulting video to Youtube (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                prefs = {'youtube': True}
            else:
                prefs = {'youtube': False}
        util.saveFile(constants.PREFS_FILE, prefs)

        if prefs['youtube']:
            self.object['youtube'] = True
            self.metadata()
        else:
            self.object['youtube'] = False
            self.cleanUp()

    def metadata(self):
        self.object['meta'] = util.setOptions(self.object['video'], self.object['youtube'], self.youtube)
        util.saveFile('progress', self.object)
        self.uploadVideo()

    def uploadVideo(self):
        ##if self.youtube.upload(self.object):
        ##    self.object['yt_uploaded'] = True
        ##    util.saveFile('progress', self.object)
        self.cleanUp()

    def cleanUp(self):
        user_input = util.query('Y/N', 'Would you like to save a copy of the rendered video to your computer (y/N)? ', default='N')
        if user_input.casefold().startswith('y'):
            print('Please select the destination folder...')
            folder_path = util.selectDestFolder()
            util.copy(constants.APPDATA_FOLDER+'/tmp/'+self.object['video']['filename'], folder_path+'/'+self.object['video']['filename'], chunk_size=1024)
        util.deleteProgress(self.object)
        user_input = util.query('Y/N', 'Would you like to process another video (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            self.chooseVideo()
        else:
            util.closeTT()

    def objectReset(self):
        self.object = {'video': {}, 'options': {}, 'meta': {}, 'youtube': None, 'rendered': False, 'qc': False, 'yt_uploaded': False}

if __name__ == '__main__':
    twitchTube()
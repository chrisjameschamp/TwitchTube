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
                elif not self.object['youtube']:
                    self.youtubeOptions()
                elif not self.object['uploaded']:
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
        self.object['youtube'] = self.youtube.setOptions(self.object['video'])
        util.saveFile('progress', self.object)
        self.uploadVideo()

    def uploadVideo(self):
        if self.youtube.upload(self.object):
            pass
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
        self.object = {'video': {}, 'options': {}, 'youtube': {}, 'rendered': False, 'qc': False, 'uploaded': False}

if __name__ == '__main__':
    twitchTube()
import os
import util

from util import constants, dialogue, functions, streamlink

class twitchTube:
    def __init__(self):
        dialogue.intro()
        self.preferences = functions.prefs()
        self.object = {}
        self.objectReset()
        self.twitch = util.twitch()
        self.ffmpeg = util.ffmpeg()
        if self.preferences['youtube']['enable']:
            self.youtube = util.youtube()
        self.chooseVideo()

    def chooseVideo(self):
        video = self.twitch.getVideos()
        video['stream'] = streamlink.getStream(video['url'])
        self.object['video'] = video
        functions.saveFile('progress', self.object)
        self.chooseOptions()

    def chooseOptions(self):
        self.object['options'] = self.ffmpeg.setOptions()
        if self.object['youtube']['unique']:
            self.object['youtube']['options'] = self.ffmpeg.setOptions(channel='youtube', options=self.object['options'])
        if self.object['facebook']['unique']:
            self.object['facebook']['options'] = self.ffmpeg.setOptions(channel='facebook', options=self.object['options'])
        self.renderVideo()

    def renderVideo(self):
        if self.object['youtube']['unique'] and self.object['facebook']['unique']:
            print('Both Youtube and Facebook videos are unique')
            user_input = dialogue.query('Y/N', 'Would you like to render the generic video (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                self.ffmpeg.render(self.object)
                self.object['rendered'] = True
            else:
                print('Skipping the generic render\n')
        elif self.object['youtube']['unique'] and not self.object['facebook']['enable']:
            print('The Youtube video is unique and Facebook is disabled')
            user_input = dialogue.query('Y/N', 'Would you like to render the generic video (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                self.ffmpeg.render(self.object)
                self.object['rendered'] = True
            else:
                print('Skipping the generic render\n')
        elif self.object['facebook']['unique'] and not self.object['youtube']['enable']:
            print('The Facebook video is unique and Youtube is disabled')
            user_input = dialogue.query('Y/N', 'Would you like to render the generic video (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                self.ffmpeg.render(self.object)
                self.object['rendered'] = True
            else:
                print('Skipping the generic render\n')
        else:
            self.ffmpeg.render(self.object)
            self.object['rendered'] = True
            
        if self.object['youtube']['enable']:
            self.ffmpeg.render(self.object, type='youtube')
        if self.object['facebook']['enable']:
            self.ffmpeg.render(self.object, type='facebook')
        self.qcVideo()

    def qcVideo(self):
        if self.object['rendered']:
            if not self.ffmpeg.qc(self.object):
                self.chooseVideo()
        if self.object['youtube']['enable']:
            if not self.ffmpeg.qc(self.object, type='youtube'):
                self.chooseVideo()
        if self.object['facebook']['enable']:
            if not self.ffmpeg.qc(self.object, type='facebook'):
                self.chooseVideo()
        self.metadata()

    def metadata(self):
        if self.object['youtube']['enable']:
            self.object['meta'] = functions.setOptions(self.object['video'], self.youtube)
        elif self.object['facebook']['enable']:
            self.object['meta'] = functions.setOptions(self.object['video'], None)
        if self.object['youtube']['enable'] or self.object['facebook']['enable']:
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
                print('Please select the destination folder...')
                folder_path = functions.selectDestFolder()
                filename, ext = os.path.splitext(self.object['video']['filename'])
                functions.copy(constants.RENDER_LOCATION+'generic/'+self.object['video']['filename'], folder_path+'/'+filename+'_gen'+ext, chunk_size=1024)
        if self.object['youtube']['enable']:
            user_input = dialogue.query('Y/N', 'Would you like to save a copy of the youtube rendered video to your computer (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                print('Please select the destination folder...')
                folder_path = functions.selectDestFolder()
                filename, ext = os.path.splitext(self.object['video']['filename'])
                functions.copy(constants.RENDER_LOCATION+'youtube/'+self.object['video']['filename'], folder_path+'/'+filename+'_yt'+ext, chunk_size=1024)
        if self.object['facebook']['enable']:
            user_input = dialogue.query('Y/N', 'Would you like to save a copy of the facebook rendered video to your computer (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                print('Please select the destination folder...')
                folder_path = functions.selectDestFolder()
                filename, ext = os.path.splitext(self.object['video']['filename'])
                functions.copy(constants.RENDER_LOCATION+'facebook/'+self.object['video']['filename'], folder_path+'/'+filename+'_fb'+ext, chunk_size=1024)

        user_input = dialogue.query('Y/N', 'Would you like to process another video (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            self.chooseVideo()
        else:
            functions.closeTT()

    def objectReset(self):
        functions.cleanUp()
        self.object = {'video': {}, 'options': {}, 'rendered': False, 'youtube': self.preferences['youtube'], 'facebook': self.preferences['facebook']}

if __name__ == '__main__':
    twitchTube()
import logging
import requests

from datetime import datetime
from util import constants, dialogue, functions

class twitch:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client_id = 0
        self.oauth = None
        self.channel = None
        self.channel_id = 0
        self.getCredentials()

    def getCredentials(self):
        # Compiled Credentials - if the application is bundled and the user is downloading an executable file, this should get the credentials no problem
        try:
            import creds
            self.client_id = creds.TWITCH_CLIENT_ID
            self.oauth = creds.TWITCH_OAUTH
        except:
            self.logger.warn('Pre Packaged Credentials Missing')
            creds = functions.getFile(constants.TWITCH_CREDS_FILE)
            self.manualCredentials(creds)
            creds = {'client_id': self.client_id, 'oauth': self.oauth}
            functions.saveFile(constants.TWITCH_CREDS_FILE, creds)

    def manualCredentials(self, creds):
        if creds is not None and 'client_id' in creds:
            self.client_id = creds['client_id']
        else:
            self.logger.info('Enter the Twitch Client ID for you app. If you do not have a Client ID visit https://dev.twitch.tv/docs/api')
            self.client_id = dialogue.query('Required', 'Twitch Client ID: ')

        if creds is not None and 'oauth' in creds:
            self.oauth = creds['oauth']
        else:
            self.logger.info('Enter the Twitch Oauth code.  If you do not have an Oauth code visit https://twitchapps.com/tokengen/')
            self.oauth = 'Bearer '+dialogue.query('Required', 'Twitch Oauth Code: Bearer ')

    def enterChannel(self):
        channel = functions.getFile(constants.TWITCH_CHANNEL_FILE)
        if channel is not None and 'channel' in channel:
            self.logger.info('On file the Twitch Channel you would like to download videos from is: {}', channel['channel'])
            user_input = dialogue.query('Y/N', 'Would you like to keep using that Channel (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                self.channel = channel['channel']
                return True
        self.logger.info('Enter the Channel Name you would like to download videos from')
        self.channel = dialogue.query('Required', 'Channel Name: ')
        functions.saveFile(constants.TWITCH_CHANNEL_FILE, {'channel': self.channel})

    def testCredentials(self):
        self.logger.debug('Testing credentials...')
        
        try:
            result = self.getTwitchData(constants.TWITCH_USERINFO+self.channel)
            if 'error' in result or not result['data']:
                if 'error' in result:
                    self.logger.error('{} {}', result['status'], result['message'])
                self.logger.warning('Please verify the supplied credentials and try again later')
                functions.clostTT()
            else:
                self.logger.debug('Success!')
                self.channel_id = result['data'][0]['id']
        except:
            self.logger.error('Error connecting to network to test credentials')
            self.logger.warning('Please try again later')
            functions.closeTT()

    def getVideos(self):
        self.enterChannel()
        self.testCredentials()

        self.logger.info('Getting recent highlights from Twitch for user: {}...', self.channel)
        videos = self.getTwitchData(constants.TWITCH_VIDEOS+self.channel_id)

        if not videos['data']:
            self.logger.error('There are no recent videos available for {}', self.channel)
            functions.closeTT()

        self.logger.debug('Filtering for just Highlights...')
        highlights = []

        for video in videos['data']:
            if video['type'] == 'highlight':
                highlights.append({'title': video['title'], 'url': video['url'], 'duration': functions.seconds(video['duration']), 'filename': video['user_login']+'_'+video['id']+'.mp4'})

        if not highlights:
            self.logger.error('There are no recent highlights available for {}', self.channel)
            functions.closeTT()

        count = len(highlights)

        self.logger.info('We have found {} highlights to choose from', count)
        self.logger.info('Please choose the corresponding number to which video you would like to select')
        self.logger.info('Or you can choose other to manually enter a twitch video')
        for i, item in enumerate(highlights, 1):
            self.logger.info('  {}) {}', i, item['title'])
        self.logger.info('  {}) Other', count+1)
        user_input = dialogue.query('Numeric', 'Video Number: ', min=1, max=count+1)
        if int(user_input) == count+1:
            while True:
                user_input = dialogue.query('Required', 'Enter the URL for the video you would like to use: ')
                twitch_id = functions.parseTwitchUrl(user_input)
                video = self.getTwitchData(constants.TWITCH_VIDEO+twitch_id)

                if 'data' in video and video['data']:
                    video = video['data'][0]
                    video = {'title': video['title'], 'url': video['url'], 'duration': functions.seconds(video['duration']), 'filename': video['user_login']+'_'+video['id']+'.mp4'}
                    self.logger.info('We found a video that matches')
                    self.logger.info('{}', video['title'])
                    user_input = dialogue.query('Y/N', 'Is that the video you were looking for (Y/n)? ', default='Y')
                    if user_input.casefold().startswith('y'):
                        break
                else:
                    self.logger.error('We Could not find a video with that URL, Try Again')
        else:
            video = highlights[int(user_input)-1]

            self.logger.info('Awesome you selected {}) {}', int(user_input), video['title'])

        return video

    def getTwitchData(self, url):
        headers = {'Authorization': self.oauth, 'Client-Id': self.client_id, }
        return requests.get(url, headers=headers).json()
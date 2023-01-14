import requests

from datetime import datetime
from util import constants, dialogue, functions

class twitch:
    def __init__(self):
        self.client_id = 0
        self.oauth = None
        self.channel = None
        self.channel_id = 0
        self.getCredentials()

    def getCredentials(self):
        creds = functions.getFile(constants.TWITCH_CREDS_FILE)

        self.enterCredentials(creds)

        self.testCredentials(creds)

        creds = {'client_id': self.client_id, 'oauth': self.oauth, 'channel': self.channel, 'channel_id': self.channel_id}
        functions.saveFile(constants.TWITCH_CREDS_FILE, creds)

    def enterCredentials(self, creds):
        if creds is not None and 'client_id' in creds:
            self.client_id = creds['client_id']
        else:
            self.client_id = dialogue.query('Required', 'Twitch Client ID: ', prePrint='Enter the Twitch Client ID for you app.  If you do not have a Client ID visit https://dev.twitch.tv/docs/api')

        if creds is not None and 'oauth' in creds:
            self.oauth = creds['oauth']
        else:
            self.oauth = 'Bearer '+dialogue.query('Required', 'Twitch Oauth Code: Bearer ', prePrint='Enter the Twitch Oauth code.  If you do not have an Oauth code visit https://twitchapps.com/tokengen/')

        if creds is not None and 'channel' in creds:
            self.channel = creds['channel']
        else:
            print('Ok so we have a Client ID and an Authorization code to access data from Twtich')
            self.channel = dialogue.query('Required', 'Channel Name: ', prePrint='Enter the Channel Name you would like to download videos from')

    def testCredentials(self, creds):
        print('Testing credentials...')
        result = self.getTwitchData(constants.TWITCH_USERINFO+self.channel)
        
        try:
            while True:
                if 'error' in result or not result['data']:
                    if 'error' in result:
                        print('Error: '+str(result['status'])+' '+result['message']+'\n')
                    print('Please verify the supplied credentials and try again\n')

                    self.enterCredentials(creds)
                else:
                    print('Success!\n')
                    self.channel_id = result['data'][0]['id']
                    break
        except:
            print('Error connecting to network to test credentials\nPlease try again later\n')
            functions.closeTT()

    def getVideos(self):

        print('On file the Twitch Channel you would like to download videos from is: '+self.channel)
        user_input = dialogue.query('Y/N', 'Would you like to keep using that Channel (Y/n)? ', default='Y')
        if user_input.casefold().startswith('n'):
            creds = functions.getFile(constants.TWITCH_CREDS_FILE)
            self.channel = dialogue.query('Required', 'Channel Name: ', prePrint='Enter the Channel Name you would like to download videos from')
            creds['channel'] = self.channel

            self.testCredentials(creds)

            functions.saveFile(constants.TWITCH_CREDS_FILE, creds)

        print('Getting recent highlights from Twitch for user: '+self.channel+'...')
        videos = self.getTwitchData(constants.TWITCH_VIDEOS+self.channel_id)

        if not videos['data']:
            print('There are no recent videos available for '+self.channel+'\n')
            functions.closeTT()

        print('Filtering for just Highlights...')
        highlights = []

        for video in videos['data']:
            if video['type'] == 'highlight':
                highlights.append({'title': video['title'], 'url': video['url'], 'duration': functions.seconds(video['duration']), 'filename': video['user_login']+'_'+video['id']+'.mp4'})

        if not highlights:
            print('There are no recent highlights available for '+self.channel+'\n')
            functions.closeTT()

        count = len(highlights)
        print('')

        print('We have found '+str(count)+' highlights to choose from')
        print('Please choose the corresponding number to which video you would like to select\nOr you can choose other to manually enter a twitch video\n')
        for i, item in enumerate(highlights, 1):
            print(str(i)+') '+item['title'])
        print(str(count+1)+') Other')
        user_input = dialogue.query('Numeric', 'Video Number: ', min=1, max=count+1)
        if int(user_input) == count+1:
            while True:
                user_input = dialogue.query('Required', 'Enter the URL for the video you would like to use: ')
                twitch_id = functions.parseTwitchUrl(user_input)
                video = self.getTwitchData(constants.TWITCH_VIDEO+twitch_id)

                if 'data' in video and video['data']:
                    video = video['data'][0]
                    video = {'title': video['title'], 'url': video['url'], 'duration': functions.seconds(video['duration']), 'filename': video['user_login']+'_'+video['id']+'.mp4'}
                    print('We found a video that matches\n'+video['title'])
                    user_input = dialogue.query('Y/N', 'Is that the video you were looking for (Y/n)? ', default='Y')
                    if user_input.casefold().startswith('y'):
                        break
                else:
                    print('We Could not find a video with that URL, Try Again')
        else:
            video = highlights[int(user_input)-1]

            print('Awesome you selected '+str(int(user_input))+') '+video['title']+'\n')

        return video

    def getTwitchData(self, url):
        headers = {'Authorization': self.oauth, 'Client-Id': self.client_id, }
        return requests.get(url, headers=headers).json()
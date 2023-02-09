import os

from appdirs import *

VERSION = '1.9.1'

# App Data Folder
APPDATA_FOLDER = user_data_dir('TwitchTube', 'ChrisJamesChamp')
RENDER_LOCATION = APPDATA_FOLDER+'/tmp/'

# Preferences
PREFS_FILE = 'preferences'
TERMINAL_FORMAT = "%(asctime)s [%(levelname)s] - %(message)s"
TERMINAL_FORMAT_DEBUG = "%(asctime)s [%(levelname)s] %(name)-25s - %(message)s"
TERMINAL_DATE_FMT = '%H:%M:%S'

# Twitch
TWITCH_CREDS_FILE = 'twitch_credentials'
TWITCH_USERINFO = 'https://api.twitch.tv/helix/users?login='
TWITCH_VIDEO = 'https://api.twitch.tv/helix/videos?id='
TWITCH_VIDEOS = 'https://api.twitch.tv/helix/videos?user_id='

# Youtube
YOUTUBE_API_FILE = 'youtube_api_key'
YOUTUBE_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
YOUTUBE_CATEGORIES = 'https://www.googleapis.com/youtube/v3/videoCategories'
YOUTUBE_CREDS_FILE = 'youtube_credentials'
YOUTUBE_REDIRECT_URIS = []
YOUTUBE_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
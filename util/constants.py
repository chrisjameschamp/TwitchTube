import os

from appdirs import *

VERSION = 0.2

# App Data Folder
APPDATA_FOLDER = user_data_dir('TwitchTube', 'ChrisJamesChamp')

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
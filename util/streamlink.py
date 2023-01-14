import streamlink

from util import functions

def getStream(url):
    print('Getting streams for video...')
    print(url)
    streams = streamlink.streams(url)
    if streams:
        print('Success\n')
        return streams['best'].url
    else:
        print('Error: Cannot get stream URL from StreamLink\nPlease try again later\n')
        functions.closeTT()

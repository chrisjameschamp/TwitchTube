import logging
import streamlink

from util import functions

logger = logging.getLogger(__name__)

def getStream(url):
    logging.info('Getting streams for video...')
    logging.info(url)
    streams = streamlink.streams(url)
    if streams:
        logging.info('Success')
        return streams['best'].url
    else:
        logging.error('Cannot get stream URL from StreamLink')
        logging.warning('Please try again later')
        functions.closeTT()

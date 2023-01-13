import httplib2
import io
import mimetypes
import os
import random
import requests
import subprocess
import time
import tqdm
import util

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.http import DEFAULT_CHUNK_SIZE
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from util import constants

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = constants.APPDATA_FOLDER+'/'+constants.YOUTUBE_CREDS_FILE+'.json'

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

class youtube:
    def __init__(self):
        self.creds = {}
        self.apiKey = None
        self.uploadLocation = constants.APPDATA_FOLDER+'/tmp/'

        self.verifyCredentials()
        self.youtube = self.get_authenticated_service()

    def verifyCredentials(self):
        creds = util.getFile(constants.YOUTUBE_CREDS_FILE)

        if creds is not None and not creds['web']['authorized']:
            creds = None

        if creds is not None and 'client_id' in creds['web']:
            self.creds['client_id'] = creds['web']['client_id']
        else:
            self.creds['client_id'] = util.query('Required', 'Youtube Client ID: ', prePrint='Enter the Youtube Client ID for you app.  If you do not have a Client ID visit https://developers.google.com/youtube/registering_an_application')

        if creds is not None and 'client_secret' in creds['web']:
            self.creds['client_secret'] = creds['web']['client_secret']
        else:
            self.creds['client_secret'] = util.query('Required', 'Youtube Client Secret: ', prePrint='Enter the Youtube Client Secret for you app.  If you do not have a Client Secret visit https://developers.google.com/youtube/registering_an_application')

        self.creds['redirect_uris'] = constants.YOUTUBE_REDIRECT_URIS
        self.creds['auth_uri'] = constants.YOUTUBE_AUTH_URI
        self.creds['token_uri'] = constants.YOUTUBE_TOKEN_URI
        self.creds['authorized'] = False

        util.saveFile(constants.YOUTUBE_CREDS_FILE, {'web': self.creds})

        api = util.getFile(constants.YOUTUBE_API_FILE)

        if api is not None:
            self.apiKey = api
        else:
            self.apiKey = {'api_key': util.query('Required', 'API Key: ', prePrint='Enter the API Key for you app.  If you do not have a API Key visit https://developers.google.com/youtube/v3/getting-started')}

        util.saveFile(constants.YOUTUBE_API_FILE, self.apiKey)

    def getCategories(self):
        url = constants.YOUTUBE_CATEGORIES
        params = {
            'part': 'snippet',
            'regionCode': 'US',
            'key': self.apiKey,
        }

        categories = requests.get(url, params=params).json()['items']

        count = len(categories)
        print('We have found '+str(count)+' categories to choose from')
        print('Please choose the corresponding number to which category you would like to select\n')
        
        for i, item in enumerate(categories, 1):
            print(str(i)+') '+item['snippet']['title'])
        user_input = util.query('Numeric', 'Category Number: ', min=1, max=count)

        return categories[int(user_input)-1]['id']

    def get_authenticated_service(self):
        print('Confirming Youtube Credentials...')
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
            scope=YOUTUBE_UPLOAD_SCOPE,
            message=MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage(constants.APPDATA_FOLDER+'/youtube_oauth2.json')
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        print('')
        self.creds['authorized'] = True
        util.saveFile(constants.YOUTUBE_CREDS_FILE, {'web': self.creds})

        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()), static_discovery=False)

    def upload(self, object):
        print('Preparing Upload...')
        try:
            self.initialize_upload(object)
            return True
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            return False

    def initialize_upload(self, object):
        youtube = self.get_authenticated_service()
        description = ''
        if object['youtube']['shortDesc']:
            description += object['youtube']['shortDesc']
            if object['youtube']['description']:
                description += '\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n'
                
        if object['youtube']['description']:
            description += object['youtube']['description']
            if object['youtube']['keywords']:
                description += '\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n'

        if object['youtube']['keywords']:
            for keyword in object['youtube']['keywords']:
                description += '#'+keyword+' '

        body=dict(
            snippet=dict(
                title=object['youtube']['title'],
                description=description,
                tags=object['youtube']['keywords'],
                categoryId=str(object['youtube']['category'])
            ),
            status=dict(
                privacyStatus=object['youtube']['privacy']
            )
        )

        pbar = tqdm.tqdm(total=1024, desc='Uploading', unit='B', unit_scale=True, unit_divisor=1024)

        # Call the API's videos.insert method to create and upload the video.
        media = MediaFileUploadWithProgressBar(self.uploadLocation+object['video']['filename'], chunksize=-1, resumable=True, progressBar=pbar)
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting "chunksize" equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=media
        )

        self.resumable_upload(insert_request, pbar)

    # This method implements an exponential backoff strategy to resume a
    # failed upload.
    def resumable_upload(self, insert_request, pbar):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                
                if response is not None:
                    if 'id' in response:
                        pbar.close()
                        print("Video id '%s' was successfully uploaded." % response['id'])
                    else:
                        pbar.close()
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                pbar.close()
                if e.resp.status in RETRIABLE_STATUS_CODES:
                        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                        e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS as e:
                pbar.close()
                error = "A retriable error occurred: %s" % e

            if error is not None:
                pbar.close()
                print(error)
                retry += 1
                if retry > MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

class MediaFileUploadWithProgressBar(MediaIoBaseUpload):
    def __init__(self, file, mimetype=None, chunksize=DEFAULT_CHUNK_SIZE,
                resumable=False, progressBar=None):
        fp = FileReaderWithProgressBar(file, progressBar)
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(file)
        super().__init__(fp, mimetype, chunksize=chunksize, resumable=resumable)

class FileReaderWithProgressBar(io.BufferedReader):
    def __init__(self, file, pbar):
        raw = io.FileIO(file)
        buffering = io.DEFAULT_BUFFER_SIZE
        stat = os.fstat(raw.fileno())
        size = stat.st_size
        self.total = 0
        self.pbar = pbar
        try:
            block_size = os.fstat(raw.fileno()).st_blksize
        except (OSError, AttributeError):
            pass
        else:
            if block_size > 1:
                buffering = block_size
        super().__init__(raw, buffering)
        self.pbar.total = size
    def seek(self, pos, whence=0):
        abspos = super().seek(pos, whence)
        return abspos
    def read(self, size=-1):
        result = super().read(size)
        change = self.tell() - self.total
        self.total = self.tell()
        self.pbar.update(change)
        return result
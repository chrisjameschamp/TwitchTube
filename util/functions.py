import logging
import json
import os
import pyperclip
import re
import requests
import subprocess
import sys
import tkinter
import tqdm
import urllib.parse

from packaging.version import Version
from tkinter import filedialog
from util import constants, dialogue

logger = logging.getLogger(__name__)

tkinter.Tk().withdraw()

def ensureAppDataFolder():
    folder = constants.APPDATA_FOLDER
    logger.debug('Ensuring App Data Folder Exists...')
    if not os.path.exists(folder):
        logger.warning('App Data Folder Does Not Exist')
        logger.debug('Creating App Data Folder...')

        try:
            os.makedirs(folder)
            logger.info('Created App Data Folder')
        except:
            logger.error('Could not open the App Data Folder')
            closeTT()

    else:
        logger.debug('App Data Folder Exists: {}', folder)
        pass

def ensureFolder(folder):
    logger.debug('Ensuring Folder Exists | {}', folder)
    if not os.path.exists(folder):
        logger.debug('Folder Does Not Exist | "{}"', folder)
        logger.debug('Creating Folder | "{}"...', folder)

        try:
            os.makedirs(folder)
            logger.debug('Created Folder | "{}"', folder)
        except:
            logger.error('Coud not create Folder | "{}"', folder)
            closeTT()

    else:
        logger.debug('Folder Exists | "{}"', folder)
        pass

def saveFile(dest, object):
    logger.debug('Saving {}...', dest)
    file = constants.APPDATA_FOLDER+'/'+dest+'.json'
    ensureAppDataFolder()

    with open(file, 'w') as outfile:

        json.dump(object, outfile)
    logger.info('{} saved to file', dest)

def getFile(dest):
    logger.debug('Checking existing {}...', dest)
    file = constants.APPDATA_FOLDER+'/'+dest+'.json'
    ensureAppDataFolder()

    try:
        with open(file) as infile:
            data = json.load(infile)
        logger.info('Loaded {}', dest)
        return data
    except:
        logger.error('File not found | {}', dest)
        return None

def closeTT():
    logger.info('Exiting TwitchTube...')
    sys.exit();

def seconds(duration):
    # Set the default values for the hours, minutes, and seconds to 0
    hours = 0
    minutes = 0
    seconds = 0

    # Split the string into tokens using the 'h', 'm', and 's' characters as delimiters
    match = re.findall(r'\d+', duration)

    if match:
        values = list(map(int, match))
        if len(values) == 1:
            seconds = values[0]
        elif len(values) == 2:
            minutes = values[0]
            seconds = values[1]
        else:
            hours = values[0]
            minutes = values[1]
            seconds = values[2]

    # Calculate the total number of seconds
    total_seconds = 3600 * hours + 60 * minutes + seconds

    return total_seconds

def time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    time_string = ""
    if hours > 0:
        time_string += f"{hours}h"
    if minutes > 0:
        time_string += f"{minutes}m"
    if seconds > 0:
        time_string += f"{seconds}s"
    return time_string

def parseTwitchUrl(url):
    # Parse the URL and extract the path component
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path

    # Split the path on the '/' character and get the last element in the list
    video_id = path.split('/')[-1]
    return video_id

def selectVideoFile():
    file_path = filedialog.askopenfilename(
        initialdir='',
        title='Select Intro File...',
        filetypes = (("all video formats", "*.mov"), ("all video formats", "*.mp4"), ("all video formats", "*.avi"), ("all video formats", "*.webm"))
    )
    return file_path

def selectDestFolder():
    folder_path = filedialog.askdirectory(
        initialdir='',
        title='Select Folder...'
    )
    return folder_path

def copy(src, dst, chunk_size=1024):
    dst_folder = os.path.split(dst)[0]
    ensureFolder(dst_folder)
    try:
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                status = 0
                total = os.path.getsize(src)

                pbar = tqdm.tqdm(total=total, desc='Copying', unit='B', unit_scale=True, unit_divisor=1024)
                while True:
                    chunk = fsrc.read(chunk_size)
                    if not chunk:
                        break

                    fdst.write(chunk)
                    pbar.update(chunk_size)
                    status += chunk_size

                if status!=total:
                    change = total - status
                    pbar.update(change)

                pbar.close()
        logger.info('Success')
        return True
    except:
        return False

def isValidTimeFormat(s):
    # Check if the string matches the time format pattern
    time_pattern = r'^(\d+h)?(\d+m)?(\d+s)?$'
    match = re.search(time_pattern, s)
    if match:
        return True
    return False

def setOptions(video):
    title = ''
    shortDesc = ''
    description = ''
    keywords = []
    logger.info('The title of this video from Twitch is "{}"', video['title'])
    user_input = dialogue.query('Y/N', 'Do you wish to keep that title (Y/n)? ', default='Y')
    if user_input.casefold().startswith('y'):
        title = video['title']
    else:
        user_input = dialogue.query('Required', 'What title would you like to give this video? ')
        title = user_input

    shortDesc = dialogue.query('Text', 'Enter a breif description for this specific video: ')

    logger.info('Do you want to include a longer description below the breif description?')
    user_input = dialogue.query('Y/N', 'This will only be used on youtube (Y/n) ', default='Y')
    if user_input.casefold().startswith('y'):
        logger.debug('Checking existing saved description...')
        file = constants.APPDATA_FOLDER+'/desc.txt'
        if os.path.exists(file):
            user_input = dialogue.query('Options', 'You have a long description on file, would you like to use it, or view / edit it (USE/edit)? ', default='Use', options=['use', 'edit', 'view'], errorMsg='Please just answer with either use, edit, or view')
            if user_input.casefold().startswith('use'):
                description = getDesc(file)
            else:
                subprocess.call(['open', '-e', file])
                user_input = dialogue.query('Y/N', 'Are you happy with the long desciprtion (Y/n)? ', default='Y')
                logger.info('Make sure to save the file and close it before continueing')
                user_input = dialogue.query('Y/N', 'Confirm that you saved the file (Y/n)? ', default='Y')
                description = getDesc(file)
        else:
            logger.warning('No saved description')
            if createFile(file):
                subprocess.call(['open', '-e', file])
                user_input = dialogue.query('Y/N', 'Are you happy with the long desciprtion (Y/n)? ', default='Y')
                logger.info('Make sure to save the file and close it before continueing')
                user_input = dialogue.query('Y/N', 'Confirm that you saved the file (Y/n)? ', default='Y')
                description = getDesc(file)
            else:
                logger.error('Could not create the description file')
                logger.warning('Proceeding as no long description will be included')

    logger.debug('Checking existing saved keywords...')
    file = constants.APPDATA_FOLDER+'/keywords.txt'
    if os.path.exists(file):
        user_input = dialogue.query('Options', 'You have saved keywords on file, would you like to use them, or edit it (USE/edit)? ', default='Use', options=['use', 'edit'], errorMsg='Please just answer with either use, or edit')
        if user_input.casefold().startswith('use'):
            keywords = getKeywords(file)
        else:
            subprocess.call(['open', '-e', file])
            user_input = dialogue.query('Y/N', 'Are you happy with the saved keywords (Y/n)? ', default='Y')
            logger.info('Make sure to save the file and close it before continueing')
            user_input = dialogue.query('Y/N', 'Confirm that you saved the file (Y/n)? ', default='Y')
            keywords = getKeywords(file)
    
    else:
        logger.warning('No saved keywords')
        if createFile(file):
            subprocess.call(['open', '-e', file])
            user_input = dialogue.query('Y/N', 'Are you happy with the saved keywords (Y/n)? ', default='Y')
            logger.info('Make sure to save the file and close it before continueing')
            user_input = dialogue.query('Y/N', 'Confirm that you saved the file (Y/n)? ', default='Y')
            keywords = getKeywords(file)

    logger.info('Existing Keywords: {}', keywords)
    keywords = list(map(str.strip, keywords.split(',')))

    logger.info('Enter additional keywords for this video, seperate them by , otherwise your going to have a whole mess of issues')
    user_input = dialogue.query('Text', 'Keywords: ')
    if user_input:
        add_keywords = list(map(str.strip, user_input.split(',')))
        add_keywords.reverse()
        if add_keywords:
            for keyword in add_keywords:
                if keyword not in keywords:
                    keywords.insert(0, keyword)

    return {'title': title, 'shortDesc': shortDesc, 'description': description, 'keywords': keywords}

def createFile(file):
    try:
        with open(file, 'w') as outfile:
            outfile.write('')
        logger.info('{} file created', file)
        return True
    except:
        return False

def getDesc(file):
    logger.debug('Getting saved description...')
    try:
        with open(file) as infile:
            data = infile.read()
        logger.info('Loaded descrption')
        return data
    except:
        logger.error('Could not get the saved description')
        return ''
    
def getKeywords(file):
    logger.debug('Getting saved keywords...')
    try:
        with open(file) as infile:
            data = infile.read()
        logger.info('Loaded keywords')
        return data
    except:
        logger.error('Could not get the saved keywords')
        return ''

def settings(channel, prefs):
    if channel in prefs:
        if prefs[channel]['enable']:
            logger.info('Your current preference is to upload to {}', channel)
            user_input = dialogue.query('Y/N', f'Would you like to continue to upload to {channel} (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                prefs[channel]['enable'] = True
                if prefs[channel]['unique']:
                    logger.info('Your current preference is to upload a unique version to {}', channel)
                    user_input = dialogue.query('Y/N', f'Would you like to continue to upload a unique version to {channel} (Y/n)? ', default='Y')
                    if user_input.casefold().startswith('y'):
                        prefs[channel]['unique'] = True
                    else:
                        prefs[channel]['unique'] = False
                else:
                    logger.info('Your current preference is to NOT upload a unique version to {}', channel)
                    user_input = dialogue.query('Y/N', f'Would you like to continue to NOT upload a unique version to {channel} (Y/n)? ', default='Y')
                    if user_input.casefold().startswith('y'):
                        prefs[channel]['unique'] = False
                    else:
                        prefs[channel]['unique'] = True
            else:
                prefs[channel]['enable'] = False
                prefs[channel]['unique'] = False
        else:
            logger.info('Your current preference is to NOT upload to {}', channel)
            user_input = dialogue.query('Y/N', f'Would you like to continue to NOT upload to {channel} (Y/n)? ', default='Y')
            if user_input.casefold().startswith('n'):
                prefs[channel]['enable'] = True
                if prefs[channel]['unique']:
                    logger.info('Your current preference is to upload a unique version to {}', channel)
                    user_input = dialogue.query('Y/N', f'Would you like to continue to upload a unique version to {channel} (Y/n)? ', default='Y')
                    if user_input.casefold().startswith('y'):
                        prefs[channel]['enable'] = True
                    else:
                        prefs[channel]['enable'] = False
                else:
                    logger.info('Your current preference is to NOT upload a unique version to {}', channel)
                    user_input = dialogue.query('Y/N', f'Would you like to continue to NOT upload a unique version to {channel} (Y/n)? ', default='Y')
                    if user_input.casefold().startswith('y'):
                        prefs[channel]['unique'] = False
                    else:
                        prefs[channel]['unique'] = True
            else:
                prefs[channel]['enable'] = False
                prefs[channel]['unique'] = False
    else:
        prefs[channel] = {'enable': False, 'unique': False}
        user_input = dialogue.query('Y/N', f'Would you like to upload to {channel} (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            prefs[channel]['enable'] = True
            user_input = dialogue.query('Y/N', f'Would you like to upload a unique, specific to {channel} version (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                prefs[channel]['unique'] = True
            else:
                prefs[channel]['unique'] = False
        else:
            prefs[channel]['enable'] = False
            prefs[channel]['unique'] = False

    if prefs[channel]['enable'] and prefs[channel]['unique']:
        logger.info('Preferences set to upload a unique version to {}', channel)
    elif prefs[channel]['enable']:
        logger.info('Preferences set to upload to {}', channel)
    else:
        logger.info('Preferences set to not upload to {}', channel)
    return prefs

def uploadVideo(object):
    logger.info('Thanks to recent changes to Google\'s Terms and Policies we can no longer upload automagically to Youtube.  However we have made step by step instructions based on your video that should make uploading your video to Youtube as straightforward as possible')
    logger.info('To get started head over to https://studio.youtube.com/ and click the button to upload a new video.')
    dialogue.query('Enter', 'Press any key to continue...')
    logger.info('First we must copy the rendered video somewhere on your computer so that you can easily access it and select it for upload.')
    logger.info('Please select the destination folder...')
    folder_path = selectDestFolder()
    filename, ext = os.path.splitext(object['video']['filename'])
    copy(constants.RENDER_LOCATION+'generic/'+object['video']['filename'], folder_path+'/'+filename+'_gen'+ext, chunk_size=1024)
    logger.info('Now on Youtube, press the {} button and navigate to where you just saved the video file and select it.', 'Select File')
    dialogue.query('Enter', 'Press any key to continue...')
    logger.info('Your video should now be uploading.  While it uploads we can fill out the details step by step.')
    pyperclip.copy(object['meta']['title'])
    logger.info('The {} has been copied to your clipboard, paste it into the {} field', 'Title', 'Title')
    dialogue.query('Enter', 'Press any key to continue...')
    description = ''
    if object['meta']['shortDesc']:
        description += object['meta']['shortDesc']
        if object['meta']['description']:
            description += '\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n'
            
    if object['meta']['description']:
        description += object['meta']['description']
        if object['meta']['keywords']:
            description += '\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n'

    if object['meta']['keywords']:
        for keyword in object['meta']['keywords']:
            description += f'#{keyword} '
    pyperclip.copy(description)
    logger.info('The {} has been copied to your clipboard, paste it into the {} field', 'Description', 'Description')
    dialogue.query('Enter', 'Press any key to continue...')
    keywords = ", ".join(object['meta']['keywords'])
    pyperclip.copy(keywords)
    logger.info('The {} has been copied to your clipboard, paste it into the {} field', 'Keywords', 'Tags')
    dialogue.query('Enter', 'Press any key to continue...')
    logger.info('All set!')
    logger.info('Once the video has finished uploading you can delete the video file you copied to your computer, or keep it for whatever you may want to use it for.')

def cleanUp():
    logger.debug('Cleaning Up and Removing Previous Renders...')
    if os.path.exists(constants.RENDER_LOCATION):
        items = os.listdir(constants.RENDER_LOCATION)
        for item in items:
            path = os.path.join(constants.RENDER_LOCATION, item)
            if os.path.isfile(path):       
                try:
                    os.remove(path)
                    logger.debug('{} Removed', path)
                except:
                    logger.error('Could Not Delete {}', path)
            elif os.path.isdir(path):
                dir = os.listdir(constants.RENDER_LOCATION+'/'+item)
                for x in dir:
                    if os.path.isfile(constants.RENDER_LOCATION+'/'+item+'/'+x):       
                        try:
                            os.remove(constants.RENDER_LOCATION+'/'+item+'/'+x)
                            logger.debug('{} Removed', constants.RENDER_LOCATION+'/'+item+'/'+x)
                        except:
                            logger.error('Could Not Delete {}', constants.RENDER_LOCATION+'/'+item+'/'+x)
                try:
                    os.rmdir(constants.RENDER_LOCATION+'/'+item)
                    logger.debug('{} Removed', constants.RENDER_LOCATION+'/'+item)
                except:
                    logger.error('Could Not Delete {}', constants.RENDER_LOCATION+'/'+item)
    logger.debug('Finished')

def checkVersion():
    logger.info('Version: {}', constants.VERSION)
    logger.info('Checking for Updates...')
    
    url = 'https://api.github.com/repos/chrisjameschamp/TwitchTube/releases/latest'
    response = requests.get(url).json()
    if 'tag_name' in response:
        gitVersion = Version(response['tag_name'])
        curVersion = Version(constants.VERSION)

        if gitVersion > curVersion:
            logger.warning('There is a new version of TwitchTube available')
            logger.info('The Most recent version is {}', gitVersion)
            logger.info('Get the latest version by visiting https://github.com/chrisjameschamp/TwitchTube')
        else:
            logger.info('You are up to date')

    else:
        logger.error('Error Checking for Updates')

import json
import os
import re
import subprocess
import tkinter
import tqdm
import urllib.parse

from tkinter import filedialog
from util import constants, dialogue

tkinter.Tk().withdraw()

def ensureAppDataFolder():
    folder = constants.APPDATA_FOLDER
    #print('Ensuring App Data Folder Exists')
    if not os.path.exists(folder):
        print('App Data Folder Does Not Exist')
        print(f'Creating App Data Folder...')

        try:
            os.makedirs(folder)
            print(f'Created App Data Folder\n')
        except:
            print('Could not open the App Data Folder\n')
            closeTT()

    else:
        #print(f'App Data Folder Exists: {folder}')
        pass

def ensureFolder(folder):
    #print('Ensuring App Data Folder Exists')
    if not os.path.exists(folder):
        print('Folder "'+folder+'" Does Not Exist')
        print(f'Creating Folder "'+folder+'"...')

        try:
            os.makedirs(folder)
            print(f'Created Folder\n')
        except:
            print('Coud not create Folder\n')
            closeTT()

    else:
        #print(f'App Data Folder Exists: {folder}')
        pass

def saveFile(dest, object):
    print('Saving '+dest+'...')
    file = constants.APPDATA_FOLDER+'/'+dest+'.json'
    ensureAppDataFolder()

    #try:
    with open(file, 'w') as outfile:

        json.dump(object, outfile)
    print(dest.capitalize()+' saved to file\n')
    #except:
    #    print('Could not save the '+dest+' to file\n')

def getFile(dest):
    print('Checking existing '+dest+'...')
    file = constants.APPDATA_FOLDER+'/'+dest+'.json'
    ensureAppDataFolder()

    try:
        with open(file) as infile:
            data = json.load(infile)
        print('Loaded '+dest+'\n')
        return data
    except:
        print('No '+dest+' found\n')
        return None

def closeTT():
    print('Exiting TwitchTube...')
    exit();

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
        print('Success\n')
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

def setOptions(video, yt_class):
    title = ''
    shortDesc = ''
    description = ''
    keywords = []
    youtube_category = ''
    privacy = 'private'
    user_input = dialogue.query('Y/N', 'Do you wish to keep that title (Y/n)? ', default='Y', prePrint='The title of this video from Twitch is "'+video['title']+'"')
    if user_input.casefold().startswith('y'):
        title = video['title']
    else:
        user_input = dialogue.query('Required', 'What title would you like to give this video? ')
        title = user_input

    shortDesc = dialogue.query('Text', 'Enter a breif description for this specific video: ')

    if yt_class is not None:
        user_input = dialogue.query('Y/N', 'This will only be used on youtube (Y/n) ', default='Y', prePrint='Do you want to include a longer description below the breif description?')
        if user_input.casefold().startswith('y'):
            print('Checking existing saved description...')
            file = constants.APPDATA_FOLDER+'/desc.txt'
            if os.path.exists(file):
                user_input = dialogue.query('Options', 'You have a long description on file, would you like to use it, or view / edit it (USE/edit)? ', default='Use', options=['use', 'edit', 'view'], errorMsg='Please just answer with either use, edit, or view')
                if user_input.casefold().startswith('use'):
                    description = getDesc(file)
                else:
                    subprocess.call(['open', '-e', file])
                    user_input = dialogue.query('Y/N', 'Are you happy with the long desciprtion (Y/n)? ', default='Y')
                    user_input = dialogue.query('Y/N', 'Confirm that you saved the file (Y/n)? ', default='Y', prePrint='Make sure to save the file and close it before continueing')
                    description = getDesc(file)
            else:
                print('No saved description\n')
                if createFile(file):
                    subprocess.call(['open', '-e', file])
                    user_input = dialogue.query('Y/N', 'Are you happy with the long desciprtion (Y/n)? ', default='Y')
                    user_input = dialogue.query('Y/N', 'Confirm that you saved the file (Y/n)? ', default='Y', prePrint='Make sure to save the file and close it before continueing')
                    description = getDesc(file)
                else:
                    print('Warning: Could not create the description file\nProceeding as no long description will be included\n')

    user_input = dialogue.query('Text', 'Keywords: ', prePrint='Enter keywords for this video, seperate them by , otherwise your going to have a whole mess of issues')
    if user_input:
        keywords = list(map(str.strip, user_input.split(',')))

    if yt_class is not None:
        youtube_category = yt_class.getCategories()

    return {'title': title, 'shortDesc': shortDesc, 'description': description, 'keywords': keywords, 'yt_category': youtube_category, 'privacy': privacy}

def createFile(file):
    try:
        with open(file, 'w') as outfile:
            outfile.write('')
        print('Desc file created\n')
        return True
    except:
        return False

def getDesc(file):
    print('Getting saved description...')
    try:
        with open(file) as infile:
            data = infile.read()
        print('Loaded descrption\n')
        return data
    except:
        print('Could not get the saved description\n')
        return ''

def prefs():
    prefs = getFile(constants.PREFS_FILE)
    if prefs is not None:
        user_input = dialogue.query('Y/N', 'Would you like to edit your preferences before we begin (y/N)? ', default='N')
        if user_input.casefold().startswith('n'):
            return prefs
    else:
        prefs = {}

    prefs = settings('youtube', prefs)
    prefs = settings('facebook', prefs)

    saveFile(constants.PREFS_FILE, prefs)

    return prefs

def settings(channel, prefs):
    if channel in prefs:
        if prefs[channel]['enable']:
            user_input = dialogue.query('Y/N', 'Would you like to continue to upload to '+channel+' (Y/n)? ', default='Y', prePrint='Your current preference is to upload to '+channel+'.')
            if user_input.casefold().startswith('y'):
                prefs[channel]['enable'] = True
                if prefs[channel]['unique']:
                    user_input = dialogue.query('Y/N', 'Would you like to continue to upload a unique version to '+channel+' (Y/n)? ', default='Y', prePrint='Your current preference is to upload a unique version to '+channel+'.')
                    if user_input.casefold().startswith('y'):
                        prefs[channel]['enable'] = True
                    else:
                        prefs[channel]['enable'] = False
                else:
                    user_input = dialogue.query('Y/N', 'Would you like to continue to NOT upload a unique version to '+channel+' (Y/n)? ', default='Y', prePrint='Your current preference is to NOT upload a unique version to '+channel+'.')
                    if user_input.casefold().startswith('y'):
                        prefs[channel]['enable'] = False
                    else:
                        prefs[channel]['enable'] = True
            else:
                prefs[channel]['enable'] = False
                prefs[channel]['unique'] = False
        else:
            user_input = dialogue.query('Y/N', 'Would you like to continue to NOT upload to '+channel+' (Y/n)? ', default='Y', prePrint='Your current preference is to NOT upload to '+channel)
            if user_input.casefold().startswith('n'):
                prefs[channel]['enable'] = True
                if prefs[channel]['unique']:
                    user_input = dialogue.query('Y/N', 'Would you like to continue to upload a unique version to '+channel+' (Y/n)? ', default='Y', prePrint='Your current preference is to upload a unique version to '+channel)
                    if user_input.casefold().startswith('y'):
                        prefs[channel]['enable'] = True
                    else:
                        prefs[channel]['enable'] = False
                else:
                    user_input = dialogue.query('Y/N', 'Would you like to continue to NOT upload a unique version to '+channel+' (Y/n)? ', default='Y', prePrint='Your current preference is to NOT upload a unique version to '+channel)
                    if user_input.casefold().startswith('y'):
                        prefs[channel]['enable'] = False
                    else:
                        prefs[channel]['enable'] = True
            else:
                prefs[channel]['enable'] = False
                prefs[channel]['unique'] = False
    else:
        prefs[channel] = {'enable': False, 'unique': False}
        user_input = dialogue.query('Y/N', 'Would you like to upload to '+channel+' (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            prefs[channel]['enable'] = True
            user_input = dialogue.query('Y/N', 'Would you like to upload a unique, specific to '+channel+' version (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                prefs[channel]['unique'] = True
            else:
                prefs[channel]['unique'] = False
        else:
            prefs[channel]['enable'] = False
            prefs[channel]['unique'] = False

    if prefs[channel]['enable'] and prefs[channel]['unique']:
        print('Preferences set to upload a unique version to '+channel+'\n')
    elif prefs[channel]['enable']:
        print('Preferences set to upload to '+channel+'\n')
    else:
        print('Preferences set to not upload to '+channel+'\n')
    return prefs

def cleanUp():
    print('Cleaning Up and Removing Previous Renders...')
    items = os.listdir(constants.RENDER_LOCATION)
    for item in items:
        path = os.path.join(constants.RENDER_LOCATION, item)
        if os.path.isfile(path):       
            try:
                os.remove(path)
                print(path+' Removed')
            except:
                print('Warning: Could Not Delete '+path)
        elif os.path.isdir(path):
            dir = os.listdir(constants.RENDER_LOCATION+'/'+item)
            for x in dir:
                if os.path.isfile(constants.RENDER_LOCATION+'/'+item+'/'+x):       
                    try:
                        os.remove(constants.RENDER_LOCATION+'/'+item+'/'+x)
                        print(constants.RENDER_LOCATION+'/'+item+'/'+x+' Removed')
                    except:
                        print('Warning: Could Not Delete '+constants.RENDER_LOCATION+'/'+item+'/'+x)
            try:
                os.rmdir(constants.RENDER_LOCATION+'/'+item)
                print(constants.RENDER_LOCATION+'/'+item+' Removed')
            except:
                print('Warning: Could Not Delete '+constants.RENDER_LOCATION+'/'+item)
    print('Finished\n')
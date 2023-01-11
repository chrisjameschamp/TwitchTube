import re
import streamlink
import subprocess
import tqdm
import util

from datetime import datetime
from util import constants

dialogue = util.dialogue()

class twitchTube:
    def __init__(self):
        dialogue.p('intro');
        
        client_id = 0
        oauth = None
        channel = None
        channel_id = 0

        dialogue.p('intro');

        creds = util.getCredentials()
        print('')

        if 'client_id' in creds:
            client_id = creds['client_id']
        else:
            print('Enter the Client ID for you app.  If you do not have a Client ID visit https://dev.twitch.tv/docs/api')
            while True:
                user_input = input('Client ID: ')
                if user_input:
                    break
            client_id = user_input
            print('')

        if 'oauth' in creds:
            oauth = creds['oauth']
        else:
            print('Enter the Oauth code.  If you do not have an Oauth code visit https://twitchapps.com/tokengen/')
            while True:
                user_input = input('Oauth Code: Bearer ')
                if user_input:
                    break
            oauth = 'Bearer '+user_input
            print('')

        if 'channel' in creds:
            channel = creds['channel']
        else:
            print('Ok so we have a Client ID and an Authorization code to access data from Twtich')
            print('Enter the Channel Name you would like to download videos from')
            while True:
                user_input = input('Channel Name: ')
                if user_input:
                    break
            channel = user_input
            print('')

        user_info = util.testCredentials(channel, oauth, client_id)

        if 'error' in user_info or not user_info['data']:
            util.credentialsFailed(user_info, creds)
        elif creds:
            print('Success!')
            print('')
            print('On file the Twitch Channel you would like to download videos from is: '+creds['channel'])
            while True:
                user_input = input('Would you like to keep using that Channel (Y/n)?') or 'Y'
                if user_input.lower() in ('yes', 'no', 'y', 'n'):
                    break
                else:
                    print('Please just answer with either Yes or No')
            if user_input.casefold().startswith('n'):
                print('Enter the Channel Name you would like to download videos from')
                while True:
                    user_input = input('Channel Name: ')
                    if user_input:
                        break
                channel = user_input
                print('')

                user_info = util.testCredentials(channel, oauth, client_id)

                if 'error' in user_info or not user_info['data']:
                    util.credentialsFailed(user_info, creds)
                else:
                    print('Success!')
                    print('')
                    channel_id = user_info['data'][0]['id']
                    creds = {'client_id': client_id, 'oauth': oauth, 'channel': channel, 'channel_id': channel_id}
                    util.saveCredentials(creds)
            else:
                print('')
        else:
            print('Success!')
            print('')
            channel_id = user_info['data'][0]['id']
            creds = {'client_id': client_id, 'oauth': oauth, 'channel': channel, 'channel_id': channel_id}
            util.saveCredentials(creds)

        if channel_id == 0:
            channel_id = creds['channel_id']
        
        print('Getting recent highlights from Twitch for user: '+channel+'...')
        videos = util.getVideos(channel_id, oauth, client_id)

        if not videos['data']:
            print('There are no recent videos available for '+channel)
            print('')
            util.closeTT()

        print('Filering for just Highlights...')
        highlights = []

        for video in videos['data']:
            if video['type'] == 'highlight':
                dt = datetime.strptime(video['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                highlights.append({'title': video['title'], 'url': video['url'], 'duration': util.seconds(video['duration']), 'filename': video['user_login']+'_'+str(int(dt.timestamp()))})

        if not highlights:
            print('There are no recent highlights available for '+channel)
            print('')
            util.closeTT()

        count = len(highlights)
        print('')

        if count > 1:
            print('We have found '+str(count)+' highlights to choose from')
            print('Please choose the corresponding number to which video you would like to select')
            print('')
            for i, item in enumerate(highlights, 1):
                print(str(i)+') '+item['title'])
            print('')
            while True:
                    user_input = input('Video Number: ')
                    try:
                        value = int(user_input)
                        if 1 <= value <=5:
                            break
                        else:
                            print('You must choose a number between 1 and '+str(count))
                    except:
                        print('You must choose a number between 1 and '+str(count))

            video = highlights[value-1]
            print('')

            print('Awesome you selected '+str(value)+') '+video['title'])
            print('')

            print('Getting streams for video...')
            streams = streamlink.streams(video['url'])
            video['stream'] = streams['best'].url
            print('Success')
            print('')

            intro_file = "CJC_BUMPER_PR4444.mov"
            endcard_file = "End_Card_PR4444.mov"
            subscribe_file = "Subscribe_Overlay_PR4444.mov"

            intro_length = 7
            endcard_length = 30
            subscribe = False
            subscribe_start = 15

            while True:
                user_input = input('Would you like to inclde the CTA / Subscribe overlay (Y/n)?') or 'Y'
                if user_input.lower() in ('yes', 'no', 'y', 'n'):
                    break
                else:
                    print('Please just answer with either Yes or No')
            if user_input.casefold().startswith('y'):
                subscribe = True
                while True:
                    user_input = input('How many seconds into the video would you like the CTA / Subscribe video to play (Default: 15)?') or '15'
                    if user_input.isnumeric() and int(user_input) < video['duration']:
                        break
                    else:
                        print('Please enter a number less than the length of the video')
                subscribe_start = int(user_input)

            command = 'ffmpeg -y '
            #command += '-i '+video['stream']+' '
            command += '-i shorty.mp4 '
            command += '-i '+intro_file+' '
            command += '-i '+endcard_file+' '
            if subscribe:
                command += '-i '+subscribe_file+' '

            video['duration'] = 60

            voffset = str(intro_length)
            aoffset = str(intro_length*1000)
            afoffset = str(video['duration']-3)
            ecoffset = str(video['duration']+intro_length-1)
            eaoffset = str((video['duration']+intro_length-1)*1000)
            svoffset = str(subscribe_start)
            saoffset = str(subscribe_start*1000)
            output = constants.APPDATA_FOLDER+'/'+video['filename']+'.mp4'
            
            total = int(ecoffset) + endcard_length

            if subscribe:
                filters = [
                    # Start offset for main video
                    '[0:v] tpad=start_duration='+voffset+' [vid0]',
                    # Fade In and Out main audio
                    '[0:a] afade=t=in:st=0:d=3 [aud1]',
                    '[aud1] afade=t=out:st='+afoffset+':d=3 [aud2]',
                    # Start offset for main audio
                    '[aud2] adelay=delays='+aoffset+':all=1 [aud3]',
                    # Intro Overlay
                    '[vid0] [1:v] overlay=enable=gte(t\,0):eof_action=pass [vid1]',
                    # Start offset for subscribe video
                    '[3:v] setpts=PTS-STARTPTS+'+svoffset+'/TB [subscribe]',
                    # Start offset for subscribe audio
                    '[3:a] adelay=delays='+saoffset+':all=1 [subscribe_aud]',
                    # Subscribe Overlay
                    '[vid1] [subscribe]overlay=enable=gte(t\,0):eof_action=pass [vid2]',
                    # Start offset for endcard video
                    '[2:v] setpts=PTS-STARTPTS+'+ecoffset+'/TB [endcard]',
                    # Start offset for endcard audio
                    '[2:a] adelay=delays='+eaoffset+':all=1 [endcard_aud]',
                    # Endcard Overlay
                    '[vid2] [endcard] overlay=enable=gte(t\,0):eof_action=repeat [v]',
                    # Mis Audio
                    '[aud3] [1:a] [subscribe_aud] [endcard_aud] amix=inputs=4 [a]',
                ]
            else:
                filters = [
                    # Start offset for main video
                    '[0:v] tpad=start_duration='+voffset+' [vid0]',
                    # Fade In and Out main audio
                    '[0:a] afade=t=in:st=0:d=3 [aud1]',
                    '[aud1] afade=t=out:st='+afoffset+':d=3 [aud2]',
                    # Start offset for main audio
                    '[aud2] adelay=delays='+aoffset+':all=1 [aud3]',
                    # Intro Overlay
                    '[vid0] [1:v] overlay=enable=gte(t\,0):eof_action=pass [vid1]',
                    # Start offset for endcard video
                    '[2:v] setpts=PTS-STARTPTS+'+ecoffset+'/TB [endcard]',
                    # Start offset for endcard audio
                    '[2:a] adelay=delays='+eaoffset+':all=1 [endcard_aud]',
                    # Endcard Overlay
                    '[vid1] [endcard] overlay=enable=gte(t\,0):eof_action=repeat [v]',
                    # Mis Audio
                    '[aud3] [1:a] [endcard_aud] amix=inputs=3 [a]',
                ]

            filter = ' ; '.join(filters)
            command += '-filter_complex "'+filter+'" '
            command += '-map [v] -map [a] -crf 18 -c:v libx264 '
            command += '"'+output+'"'
            print('')
            
            print('Starting Transcode...')
            fps = 0
            frames = 0
            pbar = tqdm.tqdm(total=100, desc='Rendering', unit=' frames')

            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                if line.lstrip().startswith('Stream #'):
                    info = line.split(', ')
                    for item in info:
                        if item.endswith('fps'):
                            last_space_index = item.rindex(' ')
                            f = item[:last_space_index]
                            f = f.replace(' fps', '')
                            f = float(f)                            
                            if f > fps:
                                fps = f
                                total = fps * total
                                pbar.total = total
                if line.startswith('frame='):
                    p = re.split('(?<=frame=)(.*)(?=fps=)',line)
                    frame = int(p[1])
                    change = frame - frames
                    frames = frame
                    pbar.update(change)

            if frames < total:
                change = total - frames
                pbar.update(change)
            pbar.close()
            print('Success')
            print('')

            while True:
                user_input = input('Would you like watch the resulting video to check it (Y/n)?') or 'Y'
                if user_input.lower() in ('yes', 'no', 'y', 'n'):
                    break
                else:
                    print('Please just answer with either Yes or No')
            if user_input.casefold().startswith('y'):
                # Windows
                # subprocess.run(["start", "video.mp4"], shell=True)
                # MacOS / Linux
                subprocess.run(["open", output])
                print('')

                while True:
                    user_input = input('Are you satisfied with the results (Y/n)?') or 'Y'
                    if user_input.lower() in ('yes', 'no', 'y', 'n'):
                        break
                    else:
                        print('Please just answer with either Yes or No')
            print('')

            command = 'python upload_video.py --file="'+output+'" '
            command += '--title="'+video['title']+'" '
            command += '--description="Description" '
            command += '--keywords="surfing,Santa Cruz" '
            command += '--category="22" '
            command += '--privacyStatus="private" '

            print('Starting Upload...')
            b = 0
            total = 0
            pbar = tqdm.tqdm(total=1024, desc='Uploading', unit='B', unit_scale=True, unit_divisor=1024)

            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                print(line)
                if line.startswith('total>>'):
                    pbar.total = int(line.split('>>')[1])
                    total = int(line.split('>>')[1])
                elif line.startswith('abs>>'):
                    seek = int(line.split('>>')[1])
                    change = seek - b
                    b = seek
                    pbar.update(change)
                elif line.startswith('read>>'):
                    cur = int(line.split('>>')[1])
                    change = cur - b
                    b = cur
                    pbar.update(change)
            if b < total:
                change = total - b
                pbar.update(change)
            pbar.close()
            print('Success')
            print('')


if __name__ == '__main__':
    twitchTube()
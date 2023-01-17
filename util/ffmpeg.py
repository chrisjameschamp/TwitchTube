import math
import os
import platform
import re
import requests
import tqdm
import shutil
import subprocess
import zipfile

from util import constants, functions, dialogue

class ffmpeg:
    def __init__(self, path):
        self.realPath = path
        self.mpegPath = '"'+path+'/ffmpeg/ffmpeg"'
        self.probePath = '"'+path+'/ffmpeg/ffprobe"'

    def setOptions(self, channel='generic', options=None):
        if channel!='generic':
            print('Configuring video file for '+channel+'...\n')
        else:
            print('First we will configure the generic video file\nWe will configure the unique versions afterwards\n')

        highlight = None
        if options and 'highlight' in options and options['highlight']:
            user_input = dialogue.query('Y/N', 'Would you like to use the same highlight (Y/n)? ', default='Y', prePrint='The generic version uses a highlight at the beginning starting at '+functions.time(options['highlight']['start'])+' and ending at '+functions.time(options['highlight']['end']))
            if user_input.casefold().startswith('y'):
                highlight = options['highlight']
            else:
                user_input = dialogue.query('Y/N', 'Would you like to include a highlight at the start of the '+channel+' video (y/N)? ', default='N')
                if user_input.casefold().startswith('y'):
                    start = dialogue.query('Time', 'Enter the time into the video where you want the highlight to start (12m4s): ')
                    end = dialogue.query('Time', 'Enter the time into the video where you want the highlight to stop (1m15s): ')
                    highlight = {'start': start, 'end': end}
        else:
            user_input = dialogue.query('Y/N', 'Would you like to include a highlight at the start of the '+channel+' video (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                start = dialogue.query('Time', 'Enter the time into the video where you want the highlight to start (12m4s): ')
                end = dialogue.query('Time', 'Enter the time into the video where you want the highlight to stop (1m15s): ')
                highlight = {'start': start, 'end': end}

        trim = None
        if options and 'trim' in options and options['trim']:
            user_input = dialogue.query('Y/N', 'Would you like to trim the same amount (Y/n)? ', default='Y', prePrint='The generic version trims the length from '+functions.time(options['trim']['start'])+' to '+functions.time(options['trim']['end']))
            if user_input.casefold().startswith('y'):
                trim = options['trim']
            else:
                user_input = dialogue.query('Y/N', 'Would you like to change the in / out points of the '+channel+' video (y/N)? ', default='N')
                if user_input.casefold().startswith('y'):
                    start = dialogue.query('Time', 'Enter the time into the video where you want it to start (12m4s): ')
                    end = dialogue.query('Time', 'Enter the time into the video where you want it to end (1m15s): ')
                    trim = {'start': start, 'end': end}
        else:
            user_input = dialogue.query('Y/N', 'Would you like to change the in / out points of the '+channel+' video (y/N)? ', default='N')
            if user_input.casefold().startswith('y'):
                start = dialogue.query('Time', 'Enter the time into the video where you want it to start (12m4s): ')
                end = dialogue.query('Time', 'Enter the time into the video where you want it to end (1m15s): ')
                trim = {'start': start, 'end': end}
        
        introVid = None
        if options and 'intro' in options and options['intro']:
            user_input = dialogue.query('Y/N', 'Would you like to use the same one (Y/n)? ', default='Y', prePrint='The generic version uses an intro video at the beginning')
            if user_input.casefold().startswith('y'):
                introVid = options['intro']
            else:
                user_input = dialogue.query('Y/N', 'Would you like to include an intro video at the beginning of the '+channel+' video (Y/n)? ', default='Y')
                if user_input.casefold().startswith('y'):
                    introVid = self.getVid(channel, 'intro')
        else:
            user_input = dialogue.query('Y/N', 'Would you like to include an intro video at the beginning of the '+channel+' video (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                introVid = self.getVid(channel, 'intro')

        overlayVid = None
        if options and 'overlay' in options and options['overlay']:
            user_input = dialogue.query('Y/N', 'Would you like to use the same one (Y/n)? ', default='Y', prePrint='The generic version uses a CTA / Subscribe overlay')
            if user_input.casefold().startswith('y'):
                overlayVid = options['overlay']
            else:
                user_input = dialogue.query('Y/N', 'Would you like to include a CTA / Subscribe overlay in the '+channel+' video (Y/n)? ', default='Y')
                if user_input.casefold().startswith('y'):
                    overlayVid = self.getVid(channel, 'overlay')
        else:
            user_input = dialogue.query('Y/N', 'Would you like to include a CTA / Subscribe overlay in the '+channel+' video (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                overlayVid = self.getVid(channel, 'overlay')

        endVid = None
        if options and 'endcard' in options and options['endcard']:
            user_input = dialogue.query('Y/N', 'Would you like to use the same one (Y/n)? ', default='Y', prePrint='The generic version uses an Endcard')
            if user_input.casefold().startswith('y'):
                endVid = options['endcard']
            else:
                user_input = dialogue.query('Y/N', 'Would you like to include an endcard in the '+channel+' video (Y/n)? ', default='Y')
                if user_input.casefold().startswith('y'):
                    endVid = self.getVid(channel, 'end')
        else:
            user_input = dialogue.query('Y/N', 'Would you like to include an endcard in the '+channel+' video (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                endVid = self.getVid(channel, 'end')

        return {'intro': introVid, 'overlay': overlayVid, 'endcard': endVid, 'highlight': highlight, 'trim': trim}

    def getVid(self, channel, type):
        vid = functions.getFile(channel+'/'+type+'Vid')
        if vid:
            if type=='intro':
                user_input = dialogue.query('Y/N', 'Would you like to reuse this '+type+' file (Y/n)? ', default='Y', prePrint='There is an '+type+' video on file. "'+vid['file']+'" with a defined length of '+vid['length']+'s and an offset of '+vid['offset']+'s')
            elif type=='end':
                user_input = dialogue.query('Y/N', 'Would you like to reuse this '+type+' file (Y/n)? ', default='Y', prePrint='There is an '+type+' video on file. "'+vid['file']+'" with an offset of '+vid['offset']+'s')
            elif type=='overlay':
                user_input = dialogue.query('Y/N', 'Would you like to reuse this '+type+' file (Y/n)? ', default='Y', prePrint='There is an '+type+' video on file. "'+vid['file']+'"')
            else:
                return False

            if user_input.casefold().startswith('n'):
                print('Deleting existing '+channel+' '+type+' video...')
                try:
                    os.remove(constants.APPDATA_FOLDER+'/'+channel+'/vid/'+vid['file'])
                except:
                    print('Warning: Could not delete existing '+channel+' '+type+' video...')
                print('Deleting '+channel+' '+type+' video settings...')
                try:
                    os.remove(constants.APPDATA_FOLDER+'/'+channel+'/'+type+'Vid.json')
                except:
                    print('Warning: Could not delete '+channel+' '+type+' video settings...')
                vid = None
                print('')
            else:
                return vid

        print('Please select your video file...')
        file_path = functions.selectVideoFile()
        if file_path:
            print('Selected File: '+file_path+'\n')
            file_name = os.path.split(file_path)[1]
            if not functions.copy(file_path, constants.APPDATA_FOLDER+'/'+channel+'/vid/'+file_name):
                print('Warning: Selected file could not be copied\nProceeding as no '+type+' video will be included\n')
                return False
            else:
                if type=='intro':
                    vid = {'file': file_name, 'length': 0, 'offset': 0, 'folder': channel}
                    functions.saveFile(''+channel+'/'+type+'Vid', vid)
                    vid['length'] = dialogue.query('Numeric', 'What is the required length of the intro video in seconds? This essnetially would be the amount of seconds before an outro transition starts, if there is any. If left blank the intro video and main video will start at the same time (Default: 0) ', default='0')
                    vid['offset'] = dialogue.query('Numeric', 'What is the offset at the beginning of the intro video to accomdate transitions in seconds? This is only used if a highlight is played before the intro video (Default: 0) ', default=0)
                    functions.saveFile(''+channel+'/'+type+'Vid', vid)
                elif type=='end':
                    vid = {'file': file_name, 'offset': 0, 'folder': channel}
                    functions.saveFile(''+channel+'/'+type+'Vid', vid)
                    vid['offset'] = dialogue.query('Numeric', 'What is the offset at the beginning of the endcard video to accomdate transitions in seconds? This is only used if there is a transition to the endcard (Default: 0) ', default=0)
                    functions.saveFile(''+channel+'/'+type+'Vid', vid)
                elif type=='overlay':
                    vid = {'file': file_name, 'start': 15, 'folder': channel}
                    functions.saveFile(''+channel+'/'+type+'Vid', vid)
                    vid['start'] = dialogue.query('Numeric', 'How many seconds into the video would you like the overlay video to play (Default: 15) ', default='15')
                    functions.saveFile(''+channel+'/'+type+'Vid', vid)
                else:
                    return False
        else:
            print('Warning: No file selected\nProceeding as no '+type+' video will be included\n')
            return False

        return vid
            
    
    def render(self, object, type='generic'):
        print('Prepareing Transcode of '+type+' video...')
        command = self.mpegPath+' -y '
        command += '-i "'+object['video']['stream']+'" '
        
        if type=='generic':
            options = object['options']
        else:
            options = object[type]['options']

        if options['overlay']:
            command += '-i "'+constants.APPDATA_FOLDER+'/'+options['overlay']['folder']+'/vid/'+options['overlay']['file']+'" '

        if options['intro']:
            command += '-i "'+constants.APPDATA_FOLDER+'/'+options['intro']['folder']+'/vid/'+options['intro']['file']+'" '

        if options['endcard']:
            command += '-i "'+constants.APPDATA_FOLDER+'/'+options['endcard']['folder']+'/vid/'+options['endcard']['file']+'" '

        filters = []
        duration = 0
        offset = 0
        vinc = 0
        ainc = 0
        vin = 0
        ain = 0

        # Highlight
        if options['highlight'] and options['intro']:
            s = int(options['highlight']['start'])
            e = int(options['highlight']['end'])+int(options['intro']['offset'])
            d = int(options['highlight']['end'])-int(options['highlight']['start'])
            o = int(options['intro']['offset'])
            filters.append('['+str(vin)+':v] trim=start='+str(s)+':'+str(e)+',setpts=PTS-STARTPTS [highlight_vid]')
            filters.append('['+str(ain)+':a] atrim=start='+str(s)+':'+str(e)+',asetpts=PTS-STARTPTS,aresample=async=1 [ha]')
            filters.append('[ha] afade=t=out:st='+str(d)+':d='+str(o)+',aresample=async=1 [highlight_aud]')
            duration += d
            offset = duration
        elif options['highlight']:
            s = options['highlight']['start']
            e = int(options['highlight']['end'])
            d = int(options['highlight']['end'])-int(options['highlight']['start'])
            filters.append('['+str(vin)+':v] trim=start='+str(s)+':'+str(e)+',setpts=PTS-STARTPTS [highlight_vid]')
            filters.append('['+str(ain)+':a] atrim=start='+str(s)+':'+str(e)+',asetpts=PTS-STARTPTS,aresample=async=1 [ha]')
            filters.append('[ha] afade=t=out:st='+str(int(d-1))+':d=1,aresample=async=1 [highlight_aud]')
            duration += d
            offset = duration
        vin += 1
        ain += 1

        if options['highlight']:
            print('Sometimes when using the Highlight feature it will download the full video first, so the transcode may be unresponsive while it downloads the video.  Please be patient.')

        # Overlay
        if options['overlay']:
            s = duration+int(options['overlay']['start'])
            filters.append('['+str(vin)+':v] setpts=PTS-STARTPTS+'+str(s)+'/TB [overlay_vid]')
            filters.append('['+str(ain)+':a] adelay=delays='+str(s)+'s:all=1 [overlay_aud]')
            vin += 1
            ain += 1

        # Intro
        if options['intro']:
            s = max(duration-int(options['intro']['offset']), 0)
            filters.append('['+str(vin)+':v] setpts=PTS-STARTPTS+'+str(s)+'/TB [intro_vid]')
            filters.append('['+str(ain)+':a] adelay=delays='+str(s)+'s:all=1 [intro_aud]')
            duration += int(options['intro']['length'])-int(options['intro']['offset'])
            offset = duration
            vin += 1
            ain += 1

        # Endcard
        if options['endcard']:
            if options['trim']:
                if int(options['trim']['end']>int(object['video']['duration'])):
                    e = int(object['video']['duration'])
                else:
                    e = int(options['trim']['end'])
                s = max(duration+e-int(options['trim']['start'])-int(options['endcard']['offset']), 0)
            else:
                s = max(duration+int(object['video']['duration'])-int(options['endcard']['offset']), 0)
            filters.append('['+str(vin)+':v] setpts=PTS-STARTPTS+'+str(s)+'/TB [endcard_vid]')
            filters.append('['+str(ain)+':a] adelay=delays='+str(s)+'s:all=1 [endcard_aud]')
            try:
                probe = subprocess.run(self.probePath +' -v error -select_streams v:0 -show_entries stream=duration -of default=nokey=1:noprint_wrappers=1 "'+constants.APPDATA_FOLDER+'/'+options['endcard']['folder']+'/vid/'+options['endcard']['file']+'"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                endcardDuration = probe.stdout.decode('utf-8').strip()
                duration += int(math.ceil(float(endcardDuration)))
            except:
                print('Unable to parse the endcard for total duration')

        # Main
        if options['trim']:
            s = int(options['trim']['start'])
            if int(options['trim']['end']>int(object['video']['duration'])):
                e = int(object['video']['duration'])
            else:
                e = int(options['trim']['end'])
            filters.append('[0:v] trim=start='+str(s)+':'+str(e)+',setpts=PTS-STARTPTS [vid]')
            filters.append('[0:a] atrim=start='+str(s)+':'+str(e)+',asetpts=PTS-STARTPTS,aresample=async=1 [aud]')
            filters.append('[vid] tpad=start_duration='+str(offset)+' [vid'+str(vinc)+']')
            if options['highlight'] or options['intro']:
                filters.append('[aud] afade=t=in:st=0:d=3,aresample=async=1 [aud'+str(ainc)+']')
            else:
                filters.append('[aud] afade=t=in:st=0:d=0,aresample=async=1 [aud'+str(ainc)+']',)
            duration += e-s

        else:
            filters.append('[0:v] tpad=start_duration='+str(offset)+' [vid'+str(vinc)+']')
            if options['highlight'] or options['intro']:
                filters.append('[0:a] afade=t=in:st=0:d=3,aresample=async=1 [aud'+str(ainc)+']')
            else:
                filters.append('[0:a] afade=t=in:st=0:d=0,aresample=async=1 [aud'+str(ainc)+']',)

            duration += int(object['video']['duration'])

        vinc += 1
        ainc += 1

        if options['endcard']:
            if options['trim']:
                if int(options['trim']['end']>int(object['video']['duration'])):
                    e = int(object['video']['duration'])
                else:
                    e = int(options['trim']['end'])
                filters.append('[aud'+str(ainc-1)+'] afade=t=out:st='+str(int(e)-3)+':d=3 [aud'+str(ainc)+']')
            else:
                filters.append('[aud'+str(ainc-1)+'] afade=t=out:st='+str(int(object['video']['duration'])-3)+':d=3 [aud'+str(ainc)+']')
            ainc += 1
            
        filters.append('[aud'+str(ainc-1)+'] adelay=delays='+str(offset)+'s:all=1,aresample=async=1 [aud'+str(ainc)+']')

        # Combine Everything
        colorspace = ', colorspace=all=bt709:format=yuv444p10:iall=bt709'
        if options['highlight']:
            filters.append('[vid'+str(vinc-1)+'] [highlight_vid] overlay=enable=gte(t\,0):eof_action=pass'+colorspace+' [vid'+str(vinc)+']')
            colorspace = ''
            vinc += 1
        
        if options['intro']:
            filters.append('[vid'+str(vinc-1)+'] [intro_vid] overlay=enable=gte(t\,0):eof_action=pass'+colorspace+' [vid'+str(vinc)+']')
            colorspace = ''
            vinc += 1

        if options['overlay']:
            filters.append('[vid'+str(vinc-1)+'] [overlay_vid] overlay=enable=gte(t\,0):eof_action=pass'+colorspace+' [vid'+str(vinc)+']')
            colorspace = ''
            vinc += 1

        if options['endcard']:
            filters.append('[vid'+str(vinc-1)+'] [endcard_vid] overlay=enable=gte(t\,0):eof_action=repeat'+colorspace+' [vid'+str(vinc)+']')
            colorspace = ''
            vinc += 1

        # Audio
        mixer = '[aud'+str(ainc)+']'
        ainput = 1
        if options['highlight']:
            mixer += '[highlight_aud]'
            ainput += 1
        if options['intro']:
            mixer += '[intro_aud]'
            ainput += 1
        if options['endcard']:
            mixer += '[endcard_aud]'
            ainput += 1
        if options['overlay']:
            mixer += '[overlay_aud]'
            ainput += 1
        mixer += 'amix=inputs='+str(ainput)+':normalize=0 [a]'
        filters.append(mixer)

        filter = ' ; '.join(filters)
        command += '-filter_complex "'+filter+'" '
        command += '-map [vid'+str(vinc-1)+'] -map [a] -crf 18 -c:v libx264 -color_trc bt709 -color_primaries bt709 -colorspace bt709 '
        command += '"'+constants.RENDER_LOCATION+type+'/'+object['video']['filename']+'"'
        
        functions.ensureFolder(constants.RENDER_LOCATION+type+'/')

        #print(command)
        print('')

        print('Starting Transcode...')
        fps = 0
        frames = 0
        total=100
        pbar = tqdm.tqdm(total=total, desc='Rendering', unit=' frames')

        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            #print(line, end='')
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
                            total = fps * duration
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
        print('Success\n')
        return True

    def qc(self, object, type='generic'):
        while True:
            user_input = dialogue.query('Y/N', 'Would you like watch the resulting '+type+' video to check it (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                if platform.system() == 'Windows':
                    subprocess.run(['start', constants.RENDER_LOCATION+type+'/'+object['video']['filename']], shell=True)
                elif platform.system() == 'Darwin':
                    subprocess.run(["open", constants.RENDER_LOCATION+type+'/'+object['video']['filename']])
                elif platform.system() == 'Linux':
                    subprocess.run(["xdg-open", constants.RENDER_LOCATION+type+'/'+object['video']['filename']])
                else:
                    print('Opening Files for Preview is not supported on '+platform.system)

                user_input = dialogue.query('Y/N', 'Are you satisfied with the results (Y/n)? ', default='Y')
                if user_input.casefold().startswith('y'):
                    return True
                else:
                    user_input = dialogue.query('Y/N', 'Would you like to start over (Y/n)? ', default='Y')
                    if user_input.casefold().startswith('y'):
                        return False
                    else:
                        functions.closeTT()
            else:
                return True

    def check(self):
        found = False
        print('Locating FFmpeg...')
        while True:
            command = self.mpegPath+' -version'
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                if line.casefold().startswith('ffmpeg version'):
                    found = True
                    break
            command = '"'+self.realPath+'/ffmpeg/ffmpeg.exe" -version'
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                if line.casefold().startswith('ffmpeg version'):
                    self.mpegPath = '"'+self.realPath+'/ffmpeg/ffmpeg.exe"'
                    self.probePath = '"'+self.realPath+'/ffmpeg/ffprobe.exe"'
                    found = True
                    break
            command = '"'+constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg" -version'
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                if line.casefold().startswith('ffmpeg version'):
                    found = True
                    self.mpegPath = '"'+constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg"'
                    self.probePath = '"'+constants.APPDATA_FOLDER+'/ffmpeg/probe"'
                    break
            command = '"'+constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg.exe" -version'
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                if line.casefold().startswith('ffmpeg version'):
                    found = True
                    self.mpegPath = '"'+constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg.exe"'
                    self.probePath = '"'+constants.APPDATA_FOLDER+'/ffmpeg/probe.exe"'
                    break
            command = 'ffmpeg -version'
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in process.stdout:
                if line.casefold().startswith('ffmpeg version'):
                    found = True
                    self.mpegPath = 'ffmpeg'
                    break
            break
        if found:
            print('FFmpeg installed\n')
        else:
            print('FFmpeg is not installed\n')
            if platform.system() == 'Windows':
                zipfile = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
                folder = self.download(zipfile, 'FFmpeg')[0]
                print('Copying FFmpeg...')
                functions.copy(constants.APPDATA_FOLDER+'/ffmpeg/'+folder+'bin/ffmpeg.exe', constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg.exe')
                print('Copying FFprobe...')
                functions.copy(constants.APPDATA_FOLDER+'/ffmpeg/'+folder+'bin/ffprobe.exe', constants.APPDATA_FOLDER+'/ffmpeg/ffprobe.exe')
                try:
                    shutil.rmtree(constants.APPDATA_FOLDER+'/ffmpeg/'+folder)
                except:
                    print('Warning: Could not clean up '+constants.APPDATA_FOLDER+'/ffmpeg/'+folder+'\n')
                self.mpegPath = '"'+constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg.exe"'
                self.probePath = '"'+constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg.exe"'
                print('FFmpeg and FFprobe installed\n')
            elif platform.system() == 'Darwin':
                #FFmpeg
                zipfile = 'https://evermeet.cx/ffmpeg/ffmpeg-5.1.2.zip'
                self.download(zipfile, 'FFmpeg')
                #FFprobe
                zipfile = 'https://evermeet.cx/ffmpeg/ffprobe-5.1.2.zip'
                self.download(zipfile, 'FFprobe')
                self.mpegPath = '"'+constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg"'
                self.probePath = '"'+constants.APPDATA_FOLDER+'/ffmpeg/ffmpeg"'
                print('FFmpeg and FFprobe installed\n')
            else:
                print('Cannot automatically install FFmpeg on '+platform.system+'\nManually install FFmpeg and make sure it is accessable via command ffmpeg -version\nVisit https://ffmpeg.org/ for more information')
                functions.closeTT()

    def download(self, url, type):
        print('Downloading '+type+'...')
        dest = constants.APPDATA_FOLDER+'/ffmpeg/'
        functions.ensureFolder(dest)
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        files = None
        pbar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading')

        try:
            with open(dest+'tmp.zip', 'wb') as file:
                for data in response.iter_content(block_size):
                    pbar.update(len(data))
                    file.write(data)
            pbar.close()
            print('Success\n')
            response.close()
        except:
            pbar.close()
            print('Error downloading '+type+'\nPlease try again later\n')
            response.close()
            functions.closeTT()
        
        try:
            with zipfile.ZipFile(dest+'tmp.zip') as file:
                files = file.namelist()
                total_size = sum(f.file_size for f in file.infolist())
                pbar = tqdm.tqdm(total=total_size, desc='Extracting', unit='B', unit_scale=True)
                for f in file.infolist():
                    file.extract(f, path=dest)
                    pbar.update(f.file_size)
                pbar.close()
        except:
            print('Error extracting '+type+'\nPlease try again later\n')
            functions.closeTT()

        print('Success\n')

        print('Cleaning Up\n')
        try:
            os.remove(dest+'tmp.zip')
        except:
            print('Warning: Could not clean up temp.zip')

        return files


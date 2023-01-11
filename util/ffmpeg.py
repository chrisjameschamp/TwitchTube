import math
import os
import re
import tqdm
import subprocess
import util

from util import constants

class ffmpeg:
    def __init__(self):
        self.introVid = None
        self.overlayVid = None
        self.endVid = None
        self.highlight = None
        self.trim = None
        util.ensureFolder('tmp')
        self.renderLocation = constants.APPDATA_FOLDER+'/tmp/'

    def setOptions(self, video):
        user_input = util.query('Y/N', 'Would you like to include a highlight at the start of the video (y/N)? ', default='N')
        if user_input.casefold().startswith('y'):
            start = util.query('Time', 'Enter the time into the video where you want the highlight to start (12m4s): ')
            end = util.query('Time', 'Enter the time into the video where you want the highlight to stop (1m15s): ')
            self.highlight = {'start': start, 'end': end}

        user_input = util.query('Y/N', 'Would you like to change the in / out points of the video (y/N)? ', default='N')
        if user_input.casefold().startswith('y'):
            start = util.query('Time', 'Enter the time into the video where you want it to start (12m4s): ')
            end = util.query('Time', 'Enter the time into the video where you want it to end (1m15s): ')
            self.trim = {'start': start, 'end': end}
        
        user_input = util.query('Y/N', 'Would you like to include an intro video at the beginning (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            self.introVid = util.getFile('introVid')
            if self.introVid:
                user_input = util.query('Y/N', 'Would you like to reuse this intro file (Y/n)? ', default='Y', prePrint='There is an intro video on file. "'+self.introVid['file']+'" with a defined length of '+self.introVid['length']+'s and an offset of '+self.introVid['offset']+'s')
                if user_input.casefold().startswith('n'):
                    self.deleteIntroVid(self.introVid)
                    self.selectIntroVid()
            else:
                self.selectIntroVid()
        else:
            existing = util.getFile('introVid')
            if existing:
                self.deleteIntroVid(existing)

        user_input = util.query('Y/N', 'Would you like to include a CTA / Subscribe overlay (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            self.overlayVid = util.getFile('overlayVid')
            if self.overlayVid:
                user_input = util.query('Y/N', 'Would you like to reuse this overlay file (Y/n)? ', default='Y', prePrint='There is an overlay video on file. "'+self.overlayVid['file'])
                if user_input.casefold().startswith('n'):
                    self.deleteOverlayVid(self.overlayVid)
                    self.selectOverlayVid()
                else:
                    self.overlayVid['start'] = util.query('Numeric', 'How many seconds into the video would you like the overlay video to play (Default: 15) ', default='15')
                    util.saveFile('overlayVid', self.overlayVid)
            else:
                self.selectOverlayVid()
        else:
            existing = util.getFile('overlayVid')
            if existing:
                self.deleteOverlayVid(existing)

        user_input = util.query('Y/N', 'Would you like to include an endcard (Y/n)? ', default='Y')
        if user_input.casefold().startswith('y'):
            self.endVid = util.getFile('endVid')
            if self.endVid:
                user_input = util.query('Y/N', 'Would you like to reuse this endcard file (Y/n)? ', default='Y', prePrint='There is an endcard video on file. "'+self.endVid['file']+'" with an offset of '+self.endVid['offset']+'s')
                if user_input.casefold().startswith('n'):
                    self.deleteEndVid(self.endVid)
                    self.selectEndVid()
            else:
                self.selectEndVid()
        else:
            existing = util.getFile('endVid')
            if existing:
                self.deleteEndVid(existing)

        return {'intro': self.introVid, 'overlay': self.overlayVid, 'endcard': self.endVid, 'highlight': self.highlight, 'trim': self.trim}

    def selectIntroVid(self):
        print('Please select your video file...')
        file_path = util.selectVideoFile()
        if file_path:
            print('Selected File: '+file_path+'\n')
            file_name = os.path.split(file_path)[1]
            if not util.copy(file_path, constants.APPDATA_FOLDER+'/vid/'+file_name):
                print('Warning: Selected file could not be copied\nProceeding as no intro video will be included\n')
            else:
                self.introVid = {'file': file_name, 'length': 0, 'offset': 0}
                util.saveFile('introVid', self.introVid)
                self.introVid['length'] = util.query('Numeric', 'What is the required length of the intro video in seconds? This essnetially would be the amount of seconds before an outro transition starts, if there is any. If left blank the intro video and main video will start at the same time (Default: 0) ', default='0')
                self.introVid['offset'] = util.query('Numeric', 'What is the offset at the beginning of the intro video to accomdate transitions in seconds? This is only used if a highlight is played before the intro video (Default: 0) ', default=0)
                util.saveFile('introVid', self.introVid)
        else:
            print('Warning: No file selected\nProceeding as no intro video will be included\n')

    def selectOverlayVid(self):
        print('Please select your video file...')
        file_path = util.selectVideoFile()
        if file_path:
            print('Selected File: '+file_path+'\n')
            file_name = os.path.split(file_path)[1]
            if not util.copy(file_path, constants.APPDATA_FOLDER+'/vid/'+file_name):
                print('Warning: Selected file could not be copied\nProceeding as no overlay video will be included\n')
            else:
                self.overlayVid = {'file': file_name, 'start': 15}
                util.saveFile('overlayVid', self.overlayVid)
                self.introVid['start'] = util.query('Numeric', 'How many seconds into the video would you like the overlay video to play (Default: 15) ', default='15')
                util.saveFile('overlayVid', self.overlayVid)
        else:
            print('Warning: No file selected\nProceeding as no overlay video will be included\n')

    def selectEndVid(self):
        print('Please select your video file...')
        file_path = util.selectVideoFile()
        if file_path:
            print('Selected File: '+file_path+'\n')
            file_name = os.path.split(file_path)[1]
            if not util.copy(file_path, constants.APPDATA_FOLDER+'/vid/'+file_name):
                print('Warning: Selected file could not be copied\nProceeding as no endcard video will be included\n')
            else:
                self.endVid = {'file': file_name, 'offset': 0}
                util.saveFile('endVid', self.endVid)
                self.endVid['offset'] = util.query('Numeric', 'What is the offset at the beginning of the endcard video to accomdate transitions in seconds? This is only used if there is a transition to the endcard (Default: 0) ', default=0)
                util.saveFile('endVid', self.endVid)
        else:
            print('Warning: No file selected\nProceeding as no endcard video will be included\n')

    def deleteIntroVid(self, file):
        print('Deleting existing intro video...')
        try:
            os.remove(constants.APPDATA_FOLDER+'/vid/'+file['file'])
        except:
            print('Warning: Could not delete existing intro video...')
        print('Deleting intro video settings...')
        try:
            os.remove(constants.APPDATA_FOLDER+'/introVid.json')
        except:
            print('Warning: Could not delete intro video settings...')
        self.introVid = None
        print('')

    def deleteOverlayVid(self, file):
        print('Deleting existing overlay video...')
        try:
            os.remove(constants.APPDATA_FOLDER+'/vid/'+file['file'])
        except:
            print('Warning: Could not delete existing overlay video...')
        print('Deleting overlay video settings...')
        try:
            os.remove(constants.APPDATA_FOLDER+'/overlayVid.json')
        except:
            print('Warning: Could not delete overlay video settings...')
        self.overlayVid = None
        print('')

    def deleteEndVid(self, file):
        print('Deleting existing endcard video...')
        try:
            os.remove(constants.APPDATA_FOLDER+'/vid/'+file['file'])
        except:
            print('Warning: Could not delete existing endcard video...')
        print('Deleting endcard video settings...')
        try:
            os.remove(constants.APPDATA_FOLDER+'/endVid.json')
        except:
            print('Warning: Could not delete endcard video settings...')
        self.endVid = None
        print('')

    def verifyFile(self, location):
        print('Verifying existing rendered video...')
        if not os.path.exists(self.renderLocation+location):
            print('Existing video file missing, will need to render a new one\n')
            return False
        else:
            print('Existing video found, will proceed with the rendered file\n')
            return True
    
    def render(self, object):
        print('Prepareing Transcode...')
        command = 'ffmpeg -y '
        command += '-i "'+object['video']['stream']+'" '

        #######
        #command += '-i "shorty.mp4" '
        #object['video']['duration'] = 60
        #######

        if object['options']['overlay']:
            command += '-i "'+constants.APPDATA_FOLDER+'/vid/'+object['options']['overlay']['file']+'" '

        if object['options']['intro']:
            command += '-i "'+constants.APPDATA_FOLDER+'/vid/'+object['options']['intro']['file']+'" '

        if object['options']['endcard']:
            command += '-i "'+constants.APPDATA_FOLDER+'/vid/'+object['options']['endcard']['file']+'" '

        filters = []
        duration = 0
        offset = 0
        vinc = 0
        ainc = 0
        vin = 0
        ain = 0

        # Highlight
        if object['options']['highlight'] and object['options']['intro']:
            s = int(object['options']['highlight']['start'])
            e = int(object['options']['highlight']['end'])+int(object['options']['intro']['offset'])
            d = int(object['options']['highlight']['end'])-int(object['options']['highlight']['start'])
            o = int(object['options']['intro']['offset'])
            filters.append('['+str(vin)+':v] trim=start='+str(s)+':'+str(e)+',setpts=PTS-STARTPTS [highlight_vid]')
            filters.append('['+str(ain)+':a] atrim=start='+str(s)+':'+str(e)+',asetpts=PTS-STARTPTS,aresample=async=1 [ha]')
            filters.append('[ha] afade=t=out:st='+str(d)+':d='+str(o)+',aresample=async=1 [highlight_aud]')
            duration += d
            offset = duration
        elif object['options']['highlight']:
            s = object['options']['highlight']['start']
            e = int(object['options']['highlight']['end'])
            d = int(object['options']['highlight']['end'])-int(object['options']['highlight']['start'])
            filters.append('['+str(vin)+':v] trim=start='+str(s)+':'+str(e)+',setpts=PTS-STARTPTS [highlight_vid]')
            filters.append('['+str(ain)+':a] atrim=start='+str(s)+':'+str(e)+',asetpts=PTS-STARTPTS,aresample=async=1 [ha]')
            filters.append('[ha] afade=t=out:st='+str(int(d-1))+':d=1,aresample=async=1 [highlight_aud]')
            duration += d
            offset = duration
        vin += 1
        ain += 1

        if object['options']['highlight']:
            print('Sometimes when using the Highlight feature it will download the full video first, so the transcode may be unresponsive while it downloads the video.  Please be patient.')

        # Overlay
        if object['options']['overlay']:
            s = duration+int(object['options']['overlay']['start'])
            filters.append('['+str(vin)+':v] setpts=PTS-STARTPTS+'+str(s)+'/TB [overlay_vid]')
            filters.append('['+str(ain)+':a] adelay=delays='+str(s)+'s:all=1 [overlay_aud]')
            vin += 1
            ain += 1

        # Intro
        if object['options']['intro']:
            s = max(duration-int(object['options']['intro']['offset']), 0)
            filters.append('['+str(vin)+':v] setpts=PTS-STARTPTS+'+str(s)+'/TB [intro_vid]')
            filters.append('['+str(ain)+':a] adelay=delays='+str(s)+'s:all=1 [intro_aud]')
            duration += int(object['options']['intro']['length'])-int(object['options']['intro']['offset'])
            offset = duration
            vin += 1
            ain += 1

        # Endcard
        if object['options']['endcard']:
            if object['options']['trim']:
                if int(object['options']['trim']['end']>int(object['video']['duration'])):
                    e = int(object['video']['duration'])
                else:
                    e = int(object['options']['trim']['end'])
                s = max(duration+e-int(object['options']['trim']['start'])-int(object['options']['endcard']['offset']), 0)
            else:
                s = max(duration+int(object['video']['duration'])-int(object['options']['endcard']['offset']), 0)
            filters.append('['+str(vin)+':v] setpts=PTS-STARTPTS+'+str(s)+'/TB [endcard_vid]')
            filters.append('['+str(ain)+':a] adelay=delays='+str(s)+'s:all=1 [endcard_aud]')
            try:
                probe = subprocess.run('ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=nokey=1:noprint_wrappers=1 "'+constants.APPDATA_FOLDER+'/vid/'+object['options']['endcard']['file']+'"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                endcardDuration = probe.stdout.decode('utf-8').strip()
                duration += int(math.ceil(float(endcardDuration)))
            except:
                print('Unable to parse the endcard for total duration')

        # Main
        if object['options']['trim']:
            s = int(object['options']['trim']['start'])
            if int(object['options']['trim']['end']>int(object['video']['duration'])):
                e = int(object['video']['duration'])
            else:
                e = int(object['options']['trim']['end'])
            filters.append('[0:v] trim=start='+str(s)+':'+str(e)+',setpts=PTS-STARTPTS [vid]')
            filters.append('[0:a] atrim=start='+str(s)+':'+str(e)+',asetpts=PTS-STARTPTS,aresample=async=1 [aud]')
            filters.append('[vid] tpad=start_duration='+str(offset)+' [vid'+str(vinc)+']')
            if object['options']['highlight'] or object['options']['intro']:
                filters.append('[aud] afade=t=in:st=0:d=3,aresample=async=1 [aud'+str(ainc)+']')
            else:
                filters.append('[aud] afade=t=in:st=0:d=0,aresample=async=1 [aud'+str(ainc)+']',)
            duration += e-s

        else:
            filters.append('[0:v] tpad=start_duration='+str(offset)+' [vid'+str(vinc)+']')
            if object['options']['highlight'] or object['options']['intro']:
                filters.append('[0:a] afade=t=in:st=0:d=3,aresample=async=1 [aud'+str(ainc)+']')
            else:
                filters.append('[0:a] afade=t=in:st=0:d=0,aresample=async=1 [aud'+str(ainc)+']',)

            duration += int(object['video']['duration'])

        vinc += 1
        ainc += 1

        if object['options']['endcard']:
            if object['options']['trim']:
                if int(object['options']['trim']['end']>int(object['video']['duration'])):
                    e = int(object['video']['duration'])
                else:
                    e = int(object['options']['trim']['end'])
                filters.append('[aud'+str(ainc-1)+'] afade=t=out:st='+str(int(e)-3)+':d=3 [aud'+str(ainc)+']')
            else:
                filters.append('[aud'+str(ainc-1)+'] afade=t=out:st='+str(int(object['video']['duration'])-3)+':d=3 [aud'+str(ainc)+']')
            ainc += 1
            
        filters.append('[aud'+str(ainc-1)+'] adelay=delays='+str(offset)+'s:all=1,aresample=async=1 [aud'+str(ainc)+']')

        # Combine Everything
        if object['options']['highlight']:
            filters.append('[vid'+str(vinc-1)+'] [highlight_vid] overlay=enable=gte(t\,0):eof_action=pass [vid'+str(vinc)+']')
            vinc += 1
        
        if object['options']['intro']:
            filters.append('[vid'+str(vinc-1)+'] [intro_vid] overlay=enable=gte(t\,0):eof_action=pass [vid'+str(vinc)+']')
            vinc += 1

        if object['options']['overlay']:
            filters.append('[vid'+str(vinc-1)+'] [overlay_vid] overlay=enable=gte(t\,0):eof_action=pass [vid'+str(vinc)+']')
            vinc += 1

        if object['options']['endcard']:
            filters.append('[vid'+str(vinc-1)+'] [endcard_vid] overlay=enable=gte(t\,0):eof_action=repeat [vid'+str(vinc)+']')
            vinc += 1

        # Audio
        mixer = '[aud'+str(ainc)+']'
        ainput = 1
        if object['options']['highlight']:
            mixer += '[highlight_aud]'
            ainput += 1
        if object['options']['intro']:
            mixer += '[intro_aud]'
            ainput += 1
        if object['options']['endcard']:
            mixer += '[endcard_aud]'
            ainput += 1
        if object['options']['overlay']:
            mixer += '[overlay_aud]'
            ainput += 1
        mixer += 'amix=inputs='+str(ainput)+' [a]'
        filters.append(mixer)

        filter = ' ; '.join(filters)
        command += '-filter_complex "'+filter+'" '
        command += '-map [vid'+str(vinc-1)+'] -map [a] -crf 18 -c:v libx264 '
        command += '"'+self.renderLocation+object['video']['filename']+'"'
        
        util.ensureFolder(self.renderLocation)

        #print(command)
        print('')

        print('Starting Transcode...')
        fps = 0
        frames = 0
        pbar = tqdm.tqdm(total=100, desc='Rendering', unit=' frames')

        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            #print(line)
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

    def qc(self, object):
        while True:
            user_input = util.query('Y/N', 'Would you like watch the resulting video to check it (Y/n)? ', default='Y')
            if user_input.casefold().startswith('y'):
                # Windows
                # subprocess.run(["start", "video.mp4"], shell=True)
                # MacOS / Linux
                subprocess.run(["open", self.renderLocation+object['video']['filename']])

                user_input = util.query('Y/N', 'Are you satisfied with the results (Y/n)? ', default='Y')
                if user_input.casefold().startswith('y'):
                    return True
                else:
                    user_input = util.query('Y/N', 'Would you like to start over (Y/n)? ', default='Y')
                    if user_input.casefold().startswith('y'):
                        return False
                    else:
                        util.closeTT()
            else:
                return True
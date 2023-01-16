import subprocess

from util import constants, dialogue

print('Compiling TwitchTube\n')

command = f'pyinstaller build/TwitchTube.spec --distpath dist/TwitchTube-MacOS-{constants.VERSION}'

process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
for line in process.stdout:
    print(line, end='')
process.wait()
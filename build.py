import math
import subprocess
import util

from util import constants

print('Building TwitchTube\n')

curVersion = constants.VERSION
incVersion = round(constants.VERSION + 0.1, 1)
jmpVersion = float(math.floor(constants.VERSION) + 1)

print(f'The current version number is {curVersion}.  The next incremental version would be {incVersion}.  Or would you like to jump to to the next release version {jmpVersion}?')
user_input = util.query('Y/N', '(y/N)? ', default='N')


if user_input.casefold().startswith('y'):
    version = jmpVersion
else:
    version = incVersion

# Update Constants Version
with open('util/constants.py', 'r') as file:
    content = file.readlines()

for i, line in enumerate(content):
    if line.casefold().startswith('version'):
        content[i] = f'VERSION = {version}\n'

with open('util/constants.py', 'w') as file:
    file.writelines(content)

# Update Poetry Project Version
with open('pyproject.toml', 'r') as file:
    content = file.readlines()

for i, line in enumerate(content):
    if line.casefold().startswith('version'):
        content[i] = f'version = "{version}".0\n'

with open('pyproject.toml', 'w') as file:
    file.writelines(content)

# Git Update
user_input = util.query('Y/N', 'Would you like to commit changes to git (Y/n)? ', default='Y')
if user_input.casefold().startswith('y'):
    m = util.query('Required', 'Enter a description for this commit: ')

    # Add
    command = 'git add .'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        print(line, end='')

    command = f'git commit -m "{m}"'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        print(line, end='')

    command = 'git push origin main'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        print(line, end='')
import math
import subprocess

from util import constants

print('Building TwitchTube\n')

curVersion = constants.VERSION
incVersion = round(constants.VERSION + 0.1, 1)
jmpVersion = float(math.floor(constants.VERSION) + 1)

while True:
    print(f'The current version number is {curVersion}.  The next incremental version would be {incVersion}.  Or would you like to jump to to the next release version {jmpVersion}?')
    user_input = input('Y/N: ')

    if user_input.lower() in ('yes', 'no', 'y', 'n'):
        break
    else:
        print('Please just answer with either Yes or No')

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
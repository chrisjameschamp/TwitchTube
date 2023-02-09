import subprocess

from semantic_version import Version
from util import constants, dialogue

print('Building TwitchTube\n')

curVersion = Version(constants.VERSION)

nextPatchVersion = Version(constants.VERSION)
nextPatchVersion.patch += 1
nextMinorVersion = Version(constants.VERSION)
nextMinorVersion.minor += 1
nextMinorVersion.patch = 0
nextMajorVersion = Version(constants.VERSION)
nextMajorVersion.major += 1
nextMajorVersion.minor = 0
nextMajorVersion.patch = 0

print(f'The current version number is {curVersion}\n')
print(f'  1) Major version: {nextMajorVersion}')
print(f'  2) Minor version: {nextMinorVersion}')
print(f'  3) Patch version: {nextPatchVersion}')
while True:
    print('\nSelect the corresponding number next to the next desired version.')
    user_input = input('>>> ')
    try:
        value = int(user_input)
        if value >= 1 and value <= 3:
            if value==1:
                nextVersion = nextMajorVersion
            elif value==2:
                nextVersion = nextMinorVersion
            else:
                nextVersion = nextPatchVersion
            print(f'You have selected {nextVersion} as the next version.')
            print('Confirm (Y/N)?')
            if input('>>> ').lower() == 'y':
                break
        else:
            print(f'Invalid input, please enter a number between 1 and 3')
    except ValueError:
        print(f'Invalid input, please enter a number between 1 and 3')

print('Confirmed')
version = nextVersion

# Update Constants Version
with open('util/constants.py', 'r') as file:
    content = file.readlines()

for i, line in enumerate(content):
    if line.casefold().startswith('version'):
        content[i] = f"VERSION = '{version}'\n"

with open('util/constants.py', 'w') as file:
    file.writelines(content)

# Update Poetry Project Version
with open('pyproject.toml', 'r') as file:
    content = file.readlines()

for i, line in enumerate(content):
    if line.casefold().startswith('version'):
        content[i] = f'version = "{version}"\n'

with open('pyproject.toml', 'w') as file:
    file.writelines(content)

# Git Update
print('Would you like to commit changes to git (Y/n)?')
if input('>>> ').lower() == 'n':
    exit()

print('Required', 'Enter a description for this commit:')
m = input('>>> ')
m = f'V{version}: {m}'

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
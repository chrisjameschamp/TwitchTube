<h2 align="center">TwitchTube</h2>
<p align="center">Simple python application for downloading a highlight from Twitch, adding a intro bumper, and endcard, and uploading it to Youtube</p>
<div align="center">
  
  ![GitHub documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg?style=flat-square)
  ![GitHub repo size](https://img.shields.io/github/repo-size/chrisjameschamp/TwitchTube?style=flat-square)
  ![Github repo languages](https://img.shields.io/github/languages/count/chrisjameschamp/TwitchTube?style=flat-square)
  ![Github repo top lang](https://img.shields.io/github/languages/top/chrisjameschamp/TwitchTube?style=flat-square)
  ![GitHub license](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)
  ![GitHub last commit](https://img.shields.io/github/last-commit/chrisjameschamp/TwitchTube?style=flat-square)

</div>
<div align="center">
  <img width="800" alt="Header" src="https://user-images.githubusercontent.com/38870317/212498051-3848fc72-47ad-4eac-96b8-108d0925d954.png">
</div>

## Index

* [TwitchTube](#twitchtube)
* [Download](#download)
* [Overview](#overview)
  * [Example](#example) 
* [Usage](#usage)
  * [Installation](#installation)
  * [First Run](#first-run)
  * [Preferences](#preferences)
  * [Twitch](#twitch)

## Download

[Click here to download TwitchTube](https://github.com/chrisjameschamp/TwitchTube/releases)

Make sure to download the appropriate version based on your operating system.  Currently both MacOS and Windows are supported, Linux is also supported however for now it must be run via the source files.

## Overview

TwitchTube is simply a tool for downloading a Twitch Highlight or video, adding a quick highlight to the beginning, trimming the total video down to desired length, adding an intro video, adding a overlay or call to action video, and lastly add an endcard.  The resulting video is then rendered out and can either be saved to your computer, or uploaded to Youtube.

<p align="center">
  <img width="800" alt="timeline" src="https://user-images.githubusercontent.com/38870317/212783271-81905e91-0d1c-49fe-b64b-55f780f8a7df.png">
</p>

The graphic above demonstrates an example of how a timeline would look if all the options available in TwitchTube would work.
  
### Example
  
|Here is a highlight from Twitch:|Once this video has been run through TwitchTube with all available options, the result looks like this:|
|:---:|:---:|
|[![Original Vimeo Video](https://user-images.githubusercontent.com/38870317/212784097-2ba613d8-448a-4e9b-82c4-6b1ac3e74e64.png)](https://www.twitch.tv/videos/1703793089?filter=highlights&sort=time)|[![Resulting Youtube Video](https://user-images.githubusercontent.com/38870317/212784181-f4fb1295-e3e4-4b57-a3e8-29ad9a5b8685.png)](https://www.youtube.com/watch?v=R24PLLWPRTU&ab_channel=ChampDrivesCars)|

## Usage

### Installation


You can run TwitchTube two different ways.  You can either use one of the prebuilt versions listed under releases, or you can download the source files and run the `TwitchTube.py`.

The prebuilt releases have FFmpeg included in them and will work out of the box.

The source files do not include FFmpeg, if you already have FFmpeg on your machine and it is accessable via the `FFmpeg` command then it will use your installed version of FFmpeg.  If you do not have FFmpeg installed on your machine or it is accessable via a different path, then TwitchTube will automatically download FFmpeg on its own and store it in the AppData/Application Support folder.

**NOTE FOR LINUX USERS:** TwitchTube will not automatically install FFmpeg on Linux due to the number of variations of Linux Distros.  However if you manually install FFmpeg and it is accessable via the `FFmpeg` command then it will use your installed version of FFmpeg. Also `tk` is required to be installed if it is not already.

Whether you are running TwitchTube via a prebuilt release or with the source files, the rest of the usage documation remains the same.

### First Run

When running TwitchTube for the first time, it will create an App Data folder where it will store credentials, temporary files, and the video files for the Intro, Endcard, and Overlay.

The App Data folder is located on MacOS at `/Users/<username>/Library/Application Support/TwitchTube` on Windows at `'C:\Users\<username>\AppData\Local\ChrisJamesChamp\TwitchTube` and on Linux at `/home/<username>/.local/share/TwitchTube`

### Preferences

First thing that happens when you run TwitchTube is it will ask you if you would like to change your preferences.  Or on the first run, since no preferences will be saved, it will ask you what your preferences are.

Right now the only preferences are whether or not to upload the resulting video to Youtube.  Twitchtube will render out a "generic" version of the video that can be saved locally.  If you choose to not upload to Youtube then the generic file is all that will be created, and once it finishes rendering, can be saved locally.  If you choose to upload to Youtube you can choose whether you want the Youtube video to be unique or not, if it is unique then the settings will differ from that of the generic video allowing you to change the length of the video, which Intro to attach, or which endcard to use.  This might be usefull if you want to add an endcard for Youtube, but not for a version that you may upload to Vimeo or Facebook later.

### Twitch

Everytime TwitchTube runs it will attempt to verify if the Twitch credentials on file are valid.  If it's the first time running TwitchTube or the credentials are not valid, it will ask you for a Twitch Client ID, and an Oauth code.  Out of the box TwitchTube does not come with any of these credentials provided, you will need to create an app and authorize it manually.

To get a client id you first need to go to https://dev.twitch.tv/ and create a Twitch Application.  The application should have a redirect URL of `https://twitchapps.com/tokengen/` which will be needed to get the oauth code.  Once you have created your Twitch Application will be given a client id. For more information on how to do this, you can read the Twitch Dev docs https://dev.twitch.tv/docs/api.

Once you have the client id you need to get an oauth code, this is super easy.  Just go to https://twitchapps.com/tokengen/, enter your client id from the previous step, and hit connect.  This will give your oauth token.

Once you have the client id and oauth token, enter them into TwitchTube when prompted, and then enter a valid Twitch Channel in which you would like to grab videos from.  It will always confirm the channel you would like to download videos from.

To avoid returning too many videos at a time, TwitchTube will only get the most recent highlights from the selected channel.  However if the desired video is not listed, you can always choose Other (Always the last option) and manually enter a url to the Twitch video you are trying to use.  `IE: https://www.twitch.tv/videos/1703793089?filter=highlights&sort=time`

## 
<div align="center">
  <a href="https://paypal.me/Champeau?country.x=US&locale.x=en_US"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black"></a>
</div>

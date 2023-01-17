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
  * [Video Options](#video-options)
     * [Highlight](#highlight)
     * [Trim](#trim-video)
     * [Intro Video](#intro-video)
     * [Overlay CTA Video](#overlay-cta-video)
     * [Endcard Video](#endcard-video)
  * [Rendering](#rendering)
  * [Quality Control](#quality-control)
  * [Youtube](#youtube)
    * [Youtube Options](#youtube-options)
    * [Title](#title)
    * [Brief Description](#breif-description)
    * [Long Description](#long-description)
    * [Keywords](#keywords)
    * [Category](#category)
  * [Uploading](#uploading)
  * [Saving Vido](#saving-video)


## Download

[Click here to download TwitchTube](https://github.com/chrisjameschamp/TwitchTube/releases)

Make sure to download the appropriate version based on your operating system.

## Overview

**TwitchTube** is simply a tool for downloading a Twitch Highlight or video, adding a quick highlight to the beginning, trimming the total video down to desired length, adding an intro video, adding a overlay or call to action video, and lastly add an endcard.  The resulting video is then rendered out and can either be saved to your computer, or uploaded to Youtube.

<p align="center">
  <img width="800" alt="timeline" src="https://user-images.githubusercontent.com/38870317/212783271-81905e91-0d1c-49fe-b64b-55f780f8a7df.png">
</p>

The graphic above demonstrates an example of how a timeline would look if all the options available in **TwitchTube** would work.
  
### Example
  
|Here is a highlight from Twitch:|Once this video has been run through **TwitchTube** with all available options, the result looks like this:|
|:---:|:---:|
|[![Original Vimeo Video](https://user-images.githubusercontent.com/38870317/212784097-2ba613d8-448a-4e9b-82c4-6b1ac3e74e64.png)](https://www.twitch.tv/videos/1703793089?filter=highlights&sort=time)|[![Resulting Youtube Video](https://user-images.githubusercontent.com/38870317/212784181-f4fb1295-e3e4-4b57-a3e8-29ad9a5b8685.png)](https://www.youtube.com/watch?v=R24PLLWPRTU&ab_channel=ChampDrivesCars)|

## Usage

### Installation


You can run **TwitchTube** two different ways.  You can either use one of the prebuilt versions listed under releases, or you can download the source files and run the `TwitchTube.py`.

The prebuilt releases have FFmpeg included in them and will work out of the box.

The source files do not include FFmpeg, if you already have FFmpeg on your machine and it is accessable via the `FFmpeg` command then it will use your installed version of FFmpeg.  If you do not have FFmpeg installed on your machine or it is accessable via a different path, then **TwitchTube** will automatically download FFmpeg on its own and store it in the AppData/Application Support folder.

**NOTE FOR LINUX USERS:** **TwitchTube** will not automatically install FFmpeg on Linux due to the number of variations of Linux Distros.  However if you manually install FFmpeg and it is accessable via the `FFmpeg` command then it will use your installed version of FFmpeg. Also `tk` is required to be installed if it is not already.

Whether you are running **TwitchTube** via a prebuilt release or with the source files, the rest of the usage documation remains the same.

### First Run

When running **TwitchTube** for the first time, it will create an App Data folder where it will store credentials, temporary files, and the video files for the Intro, Endcard, and Overlay.

The App Data folder is located on MacOS at `/Users/<username>/Library/Application Support/TwitchTube` on Windows at `'C:\Users\<username>\AppData\Local\ChrisJamesChamp\TwitchTube` and on Linux at `/home/<username>/.local/share/TwitchTube`

### Preferences

First thing that happens when you run **TwitchTube** is it will ask you if you would like to change your preferences.  Or on the first run, since no preferences will be saved, it will ask you what your preferences are.

**TwitchTube** will render out a "generic" version of the video that can be saved locally.  If you choose to not upload to Youtube then the generic file is all that will be created, and once it finishes rendering, can be saved locally.  If you choose to upload to Youtube you can choose whether you want the Youtube video to be unique or not, if it is unique then the settings can differ from that of the generic video allowing you to change the length of the video, which Intro to attach, or which endcard to use.  This might be usefull if you want to add an endcard for Youtube, but not for a version that you may upload to Vimeo or Facebook later.

### Twitch

Everytime **TwitchTube** runs it will attempt to verify if the Twitch credentials on file are valid.  If it's the first time running **TwitchTube** or the credentials are not valid, it will ask you for a Twitch Client ID, and an Oauth code.  Out of the box **TwitchTube** does not come with any of these credentials provided, you will need to create an app and authorize it manually.

To get a client id you first need to go to https://dev.twitch.tv/ and create a Twitch Application.  The application should have a redirect URL of `https://twitchapps.com/tokengen/` which will be needed to get the oauth code.  Once you have created your Twitch Application will be given a client id. For more information on how to do this, you can read the Twitch Dev docs https://dev.twitch.tv/docs/api.

Once you have the client id you need to get an oauth code, this is super easy.  Just go to https://twitchapps.com/tokengen/, enter your client id from the previous step, and hit connect.  This will give your oauth token.

Once you have the client id and oauth token, enter them into **TwitchTube** when prompted, and then enter a valid Twitch Channel in which you would like to grab videos from.  It will always confirm the channel you would like to download videos from.

To avoid returning too many videos at a time, **TwitchTube** will only get the most recent highlights from the selected channel.  However if the desired video is not listed, you can always choose Other (Always the last option) and manually enter a url to the Twitch video you are trying to use.  `IE: https://www.twitch.tv/videos/1703793089?filter=highlights&sort=time`

### Video Options

#### Highlight

Prior to the video or the Intro video, you can add a highlight.  Think of this as a quick short snippet where the action is the greatest, maybe it leaves the audience with a cliff-hanger that makes them want to watch the entire video to see what happens.

**TwithTube** will first ask you if you would like to include a highlight.  By default the answer is `No` but simply type `Y` or `Yes` to add a highlight.

If adding a highlight, it will also ask you for the time into the video where you want the highlight to begin and the time into the video where you want the highlight to end.  For example: at `00:59:22` you want the highlight to start then you would enter `59m22s` and and you want the highlight to end at `01:05:13` then you would enter `1h5m13s`

#### Trim Video

If you want to change the in and/or out points of the video then you can trim it.  If you want to change just the in point, then when it asks for the new out point, enter a time greater than the length of the video and if you want to just change the out point, then when it asks for the new in point just set it as `0s`

Use the same syntax as the Highlight when entering times.

#### Intro Video

The Intro Video is the title card.  Think of the MGM graphic with the lion roaring.  The highlight would be the trailers beforehard and the Intro Video is the MGM Graphic, and then the primary Twitch video plays afterwards.

**TwitchTube** will save a copy of whatever video file you select so you will only have to choose it the first time if you would like to reuse it over and over again.

Most video formats are accepted and **TwitchTube** is designed to accept an alpha channel for transitions at the beginning and the end of the Intro Video.  It is recommended to use a straight alpha channel as opposed to premultiplied.

The resolution of the Intro video should match the Twitch Video you are downloading.

When selecting the Intro Video it will ask two things, the first one is the **length** of the Intro Video.  This is important as it needs to know the length in seconds before the out transition starts.  So if you have an Intro video that is 10 seconds long but the out transition starts at 8 seconds.  You would enter 8, always round down, if it starts at 8.5 seconds, still enter 8.  If there is no out transition, then enter the total length of the Intro Video rounding down, so if the total length is 5.8 seconds, enter 5.

The second thing it will ask you for is the **offset**.  This is the duration of the in transition.  If the transition is 3 seconds, then enter 3 seconds.  If it is 2.5 seconds then enter 3 seconds, round up for the offset.  This is only used if a highlight is used, the Introvideo will start at the beginning if no highlight video is chosen or if the offset is set to 0.

Your settings for the Intro Video will be saved for future use but can be changed if necessary.

#### Overlay CTA Video

The Overlay video or Call To Action (CTA) video is designed to be an overlay added somewhere in the middle of your video after the Intro Video and Highlight Clip (If they are being used) where the graphic can remind uses to like, follow, subscribe, etc.

This video is designed to have an alpha channel and for the content to already be placed on screen where it should appear.

Most video formats are accepted and **TwitchTube** is designed to accept an alpha channel .  It is recommended to use a straight alpha channel as opposed to premultiplied.

The resolution of the Overlay video should match the Twitch Video you are downloading.

The only option for the Overlay video is how many seconds into the video you would like for it to play.  This should simply be entered as number of seconds `5` or `120`.  Default is set to 15 seconds.

Your settings for the Overlay Video will be saved for future use but can be changed if necessary.

#### Endcard Video

The Endcard video will be played after the Twitch video finishes.

Most video formats are accepted and **TwitchTube** is designed to accept an alpha channel for transitions at the beginning of the Endcard Video.  It is recommended to use a straight alpha channel as opposed to premultiplied.

The resolution of the Endcard video should match the Twitch Video you are downloading.

The only option for the Endcard video is the **offset**. This is the duration of the in transition.  If the transition is 3 seconds, then enter 3 seconds.  If it is 2.5 seconds then enter 3 seconds, round up for the offset.  This is only used if a highlight is used, the Introvideo will start at the beginning if no highlight video is chosen or if the offset is set to 0.

Your settings for the Endcard Video will be saved for future use but can be changed if necessary.

### Rendering

Once the options are set the video will render. The video will be rendered at the resolution of the original Twitch Video and at the same frame-rate as well.  It will render out an `H.264` encoded video with a `.mp4` extension and in `BT.709` Colorspace.

### Quality Control

Once the video has finished rendering it will ask you if you would like to QC (Quality Check) the resulting video.  This is a good idea to make sure everything rendered out as intended.

Ff you answer `Y` to watch the resulting video, it will open the video with the default video viewing software on your system.

If you are happy with the results answer `Y`. **WARNING**: if you answer `N` TwitchTube will exit and the resulting video will be removed, you will have to start over.

### Youtube

If you have chosen to upload to Youtube in your preferences, then everytime **TwitchTube** runs it will try and verify if the Youtube credentials on file are valid. If it's the first time running **TwitchTube** or the credentials are not valid, it will ask you for a Youtube Client ID, and an Client Secret. Out of the box **TwitchTube** does not come with any of these credentials provided, you will need to create an app and authorize it manually.

You can follow the official youtube api in the documentation https://developers.google.com/youtube/registering_an_application for creating the project, and creating the credentials for the Youtube Client ID and Client Secret.

You will also need to creaete an API Key from the developers console as well. For more information on how to do this, you can read the Youtube developers docs: https://developers.google.com/youtube/v3/getting-started

When creating your credentials make sure to add the email associated with the youtube account in which you would like to upload to as a tester.

Once you have done all of that, **TwitchTube** will open a browser for you to sign into youtube and select the channel in which you would like to upload to.  Assuming you have done all the appropriate steps, you will be authorized and ready to go.

#### Youtube Options

When uploading to Youtube you will be given additional options.

#### Title

By default the title will be transfered from Twitch to Youtube, you can change the title at this point.

#### Breif Description

You can add a breif description about the video itself, usually a paragraph or less of text.

#### Long Description

The long description would be if you wanted to add links to social media, or have a part of the description that is uesed on multiple videos.  If you have a long description on file you can either edit it or by default it will simply use the long description on file.  If you choose to edit it the file it will open a txt file with the default text editor on your system.  Once you are satisfied make sure to save this file and then close it.  **TwitchTube** will confirm that you have saved the file just in case you forget.

The Long Description will be placed just after the breif description with bar or `▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬` seperating the two.

#### Keywords

You can add as many keywords as you would like, it will add these keywords to the video and also to the end of the description with hashtags.  Make sure to seperate the keywords with a commna.

#### Category

**TwitchTube** will list the available Categories to choose from.  Enter the corresponding number to the category you would like to choose.

### Uploading

Once all options are set the video will upload to Youtube.  Once complete **TwitchTube** will give you a link to the video and a Youtube Studio link as well so you can edit the resulting video.  The video will be set to private and you will have to manually switch it to public once you are ready.

### Saving Video

You can save a copy of both the generic and Youtube versions locally if you choose to.  **WARNING**: If you do not save a copy locally, it will be deleted next time **TwitchTube** runs.

**And Thats It!**

## 
<div align="center">
  <a href="https://paypal.me/Champeau?country.x=US&locale.x=en_US"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black"></a>
</div>

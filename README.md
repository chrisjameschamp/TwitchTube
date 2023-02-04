<h2 align="center">TwitchTube</h2>
<p align="center">Simple python application for downloading a highlight from Twitch, adding a intro bumper, and endcard, and uploading it to Youtube</p>
<div align="center">
  
  ![GitHub documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg?style=flat-square)
  ![GitHub repo size](https://img.shields.io/github/repo-size/chrisjameschamp/TwitchTube?style=flat-square)
  ![Github repo languages](https://img.shields.io/github/languages/count/chrisjameschamp/TwitchTube?style=flat-square)
  ![Github repo top lang](https://img.shields.io/github/languages/top/chrisjameschamp/TwitchTube?style=flat-square)
  ![GitHub license](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)
  ![GitHub last commit](https://img.shields.io/github/last-commit/chrisjameschamp/TwitchTube?style=flat-square)
  ![GitHub downloads](https://img.shields.io/github/downloads/chrisjameschamp/TwitchTube/total?style=flat-square)
  ![GitHub release](https://img.shields.io/github/v/release/chrisjameschamp/TwitchTube?style=flat-square&display_name=tag)
  

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
  * [Uploading](#uploading)
  * [Saving Video](#saving-video)


## Download

[Click here to download TwitchTube](https://github.com/chrisjameschamp/TwitchTube/releases)

Make sure to download the appropriate version based on your operating system.

## Overview

**TwitchTube** is a tool for editing and uploading Twitch highlights or videos, including adding a quick highlight, trimming, adding an intro, overlay or call-to-action video, and an endcard.

<p align="center">
  <img width="800" alt="timeline" src="https://user-images.githubusercontent.com/38870317/212783271-81905e91-0d1c-49fe-b64b-55f780f8a7df.png">
</p>

The graphic above demonstrates an example of how a timeline would look if all the options available in **TwitchTube** would work.
  
### Example

This is an example of a Twitch highlight before and after running it through **TwitchTube** with all options enabled. (You will need to click on the images to see the differences on Twitch and on Youtube)
  
|Before|After|
|:---:|:---:|
|[![Original Vimeo Video](https://user-images.githubusercontent.com/38870317/212784097-2ba613d8-448a-4e9b-82c4-6b1ac3e74e64.png)](https://www.twitch.tv/videos/1703793089?filter=highlights&sort=time)|[![Resulting Youtube Video](https://user-images.githubusercontent.com/38870317/212784181-f4fb1295-e3e4-4b57-a3e8-29ad9a5b8685.png)](https://www.youtube.com/watch?v=R24PLLWPRTU&ab_channel=ChampDrivesCars)|

## Usage

### Installation


You can run **TwitchTube** two different ways.  You can either use one of the prebuilt versions listed under releases, or you can download the source files and run the `TwitchTube.py`.

The prebuilt releases include FFmpeg and are ready to use.

The source files do not include FFmpeg, if you already have FFmpeg on your machine and it is accessable via the `FFmpeg` command then it will use your installed version of FFmpeg.  If you do not have FFmpeg installed on your machine or it is accessable via a different path, then **TwitchTube** will automatically download FFmpeg on its own and store it in the AppData/Application Support folder.

**NOTE FOR LINUX USERS:** **TwitchTube** will not automatically install FFmpeg on Linux due to the number of variations of Linux Distros.  However if you manually install FFmpeg and it is accessable via the `FFmpeg` command then it will use your installed version of FFmpeg. Also `tk` is required to be installed if it is not already.

Whether you are running **TwitchTube** via a prebuilt release or with the source files, the rest of the usage documentation remains the same.

### First Run

Upon the first launch, **TwitchTube** will create an App Data folder to store credentials, temporary files, and intro, endcard, and overlay video files.

The App Data folder is located on MacOS at `/Users/<username>/Library/Application Support/TwitchTube` on Windows at `'C:\Users\<username>\AppData\Local\ChrisJamesChamp\TwitchTube` and on Linux at `/home/<username>/.local/share/TwitchTube`

### Preferences

When you first launch **TwitchTube**, you will be prompted to change or set your preferences. On subsequent launches, you will be given the option to change your preferences.

**TwitchTube** can create a "generic" version of the video that can be saved locally. If you choose not to upload the video to YouTube, the generic file will be the only version created. However, if you choose to upload to YouTube, you can opt for a unique version of the video with different settings, such as a different length, intro, or endcard. This can be useful if you want to add an endcard for YouTube, but not for other platforms like Vimeo or Facebook.

### Twitch

Every time you run **TwitchTube**, it will verify that the Twitch credentials on file are valid. If it's the first time running the application or the credentials are invalid, you will be prompted to enter a Twitch Client ID and an OAuth token. **TwitchTube** does not come with these credentials, so you will need to create an app and authorize it manually.

To get a client ID, you first need to go to https://dev.twitch.tv/ and create a Twitch Application. The application should have a redirect URL of https://twitchapps.com/tokengen/, which is required to get the OAuth token. Once you have created your Twitch Application, you will be given a client ID. For more information on how to do this, you can read the Twitch Dev docs at https://dev.twitch.tv/docs/api.

To get an OAuth token, go to https://twitchapps.com/tokengen/ and enter your client ID from the previous step. This will give you your OAuth token.

Once you have the client ID and OAuth token, enter them into **TwitchTube** when prompted, and then enter a valid Twitch channel from which you would like to grab videos. The application will confirm the channel you selected.

To avoid returning too many videos at once, **TwitchTube** will only get the most recent highlights from the selected channel. However, if the desired video is not listed, you can always choose "Other" (which is always the last option) and manually enter the URL of the Twitch video you want to use. For example: https://www.twitch.tv/videos/1703793089?filter=highlights&sort=time.

### Video Options

#### Highlight

Before the video or the intro video, you can add a highlight. This is a quick snippet of the most action-packed part of the video that leaves the audience wanting more.

**TwitchTube** will ask you if you want to include a highlight. By default, the answer is "No," but you can type "Y" or "Yes" to add a highlight.

If you choose to add a highlight, you will be prompted to enter the start and end times of the highlight. For example, if you want the highlight to start at `00:59:22`, you would enter `59m22s` and if you want the highlight to end at `01:05:13`, you would enter `1h5m13s`.

#### Trim Video

If you want to change the in and/or out points of the video, you can trim it. If you want to change just the in point, enter a time greater than the length of the video when prompted for the new out point. If you want to change just the out point, enter `0s` when prompted for the new in point. Use the same syntax as the Highlight when entering times.

#### Intro Video

The Intro Video is a title card that appears at the beginning of the final video, similar to the MGM graphic with the lion roaring. **TwitchTube** will save a copy of the video file you select, so you only need to choose it once. Most video formats are accepted, and it is designed to accept an alpha channel for transitions at the beginning and end of the Intro Video. It is recommended to use a straight alpha channel, rather than premultiplied.

The resolution of the Intro Video should match the Twitch Video you are downloading. When selecting the Intro Video, **TwitchTube** will ask for two things: the length and offset of the Intro Video.

* The length is important as it needs to know the seconds before the out transition starts. So, if you have an Intro video that is 10 seconds long but the out transition starts at 8 seconds, you would enter 8. Always round down; if it starts at 8.5 seconds, still enter 8. If there is no out transition, then enter the total length of the Intro Video, rounding down. For example, if the total length is 5.8 seconds, enter 5.
* The offset is the duration of the in transition. If the transition is 3 seconds, then enter 3 seconds. If it is 2.5 seconds, then enter 3 seconds, rounded up. This is only used if a highlight is used. If no highlight video is chosen or if the offset is set to 0, the Intro video will start at the beginning.

Your settings for the Intro Video will be saved for future use, but they can be changed if necessary.

#### Overlay CTA Video

The Overlay video, or Call-to-Action (CTA) video, is designed to be an overlay added somewhere in the middle of your video, after the Intro Video and Highlight Clip (if they are being used). The overlay can remind users to like, follow, subscribe, etc.

This video is designed to have an alpha channel, and the content should already be placed on the screen where it should appear. Most video formats are accepted, and **TwitchTube** is designed to accept an alpha channel. It is recommended to use a straight alpha channel, rather than premultiplied.

The resolution of the Overlay video should match the Twitch Video you are downloading. The only option for the Overlay video is how many seconds into the video you would like it to play.
* This should be entered as a number of seconds. 
* For example, `5` or `120`.
* The default is set to 15 seconds.

Your settings for the Overlay Video will be saved for future use, but they can be changed if necessary.

#### Endcard Video

The Endcard video is played after the Twitch video finishes. Most video formats are accepted, and TwitchTube is designed to accept an alpha channel for transitions at the beginning of the Endcard Video. It is recommended to use a straight alpha channel, rather than premultiplied.

The resolution of the Endcard video should match the Twitch Video you are downloading. The only option for the Endcard video is the offset, which is the duration of the in transition.
* If the transition is 3 seconds, enter 3 seconds.
* If it is 2.5 seconds, enter 3 seconds, rounding up.
* This offset is only used if a highlight is used. If no highlight video is chosen or if the offset is set to 0, the Endcard video will start at the beginning.

Your settings for the Endcard Video will be saved for future use, but they can be changed if necessary.

### Rendering

Once the options are set, the video will begin rendering. The video will be rendered with the same resolution and frame rate as the original Twitch Video. It will be encoded with `H.264` and have a `.mp4` file extension, in the `BT.709` colorspace.

### Quality Control

Once the video has finished rendering, you will be prompted to Quality Check (QC) the resulting video. This is a good idea to ensure that everything rendered as intended.

If you choose to watch the resulting video, it will open in your system's default video viewing software. If you are satisfied with the results, you can confirm this. **WARNING:** If you choose not to QC the video, TwitchTube will exit and the resulting video will be deleted, requiring you to start over.

### Youtube

If you selected to upload to Youtube in your preferences, **TwitchTube** will verify if the Youtube credentials on file are valid every time it runs. If it's the first time running **TwitchTube** or the credentials are not valid, it will ask you for a Youtube Client ID and Client Secret. You will need to create an app and authorize it manually.

To create a project and credentials for the Youtube Client ID and Client Secret, follow the instructions on the official Youtube API documentation: https://developers.google.com/youtube/registering_an_application

You will also need to create an API Key from the developer's console. For more information on how to do this, refer to the Youtube Developers documentation: https://developers.google.com/youtube/v3/getting-started

When creating your credentials, make sure to add the email associated with the Youtube account you wish to upload to as a tester.

Once you have completed these steps, **TwitchTube** will open a browser for you to sign in to Youtube and select the channel you wish to upload to. If you have completed the appropriate steps, you will be authorized and ready to proceed.

#### Youtube Options
When uploading to Youtube, you'll have the option to set a title, brief and long description, keywords, and a category for your video.

* **Title:** By default, the title will be transferred from Twitch, but you can change it at this point.
* **Brief Description:** A short summary of the video, usually a paragraph or less.
* **Long Description:** A longer description that can include links to social media, or information that you want to include on multiple videos.
* **Keywords:** Add as many keywords as you'd like to help people find your video, they will be added to the video and to the end of the description with hashtags.
* **Category:** Select the appropriate category for your video from the list provided.

**Note:** Long Description can be edited by default and will open a txt file with the default text editor on your system. Make sure to save the file and close it, TwitchTube will confirm that you have saved the file just in case you forget. The Long Description will be placed just after the brief description with a bar or ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ separating the two.

### Uploading

After setting all the options, the video will be uploaded to Youtube. Once the upload is complete, **TwitchTube** will provide links to the video on Youtube and in Youtube Studio, where you can edit the video. The video will be set to private and you will have to manually make it public when you are ready.

### Saving Video

You can save local copies of both the generic and Youtube versions of the video. **WARNING**: If you don't save a copy locally, it will be deleted the next time **TwitchTube** runs.

**Thats It!**

## 
<div align="center">
  <a href="https://paypal.me/Champeau?country.x=US&locale.x=en_US"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black"></a>
</div>

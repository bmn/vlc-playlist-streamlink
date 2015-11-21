# vlc-playlist-livestreamer
VLC playlist extension to enable direct integration with Livestreamer

### Intro
[Livestreamer](http://docs.livestreamer.io/) is a command-line application that bypasses the "Flash-only!"-type restrictions that streaming sites such as Twitch and YouTube Live place on their streams. It acts as a middleman between the site, and the player application you *actually* want to use (VLC by default).

The downside of Livestreamer is that you have to do some CLI gymnastics every time you want to watch a stream, e.g. `livestreamer twitch.tv/peaches best`, and various GUIs have been developed to make this more user-friendly. [VLClive](https://github.com/sleighsoft/VLClive) is one example that adds a dialogue window to VLC.

VLC already has native support for video sites such as YouTube. Copy a [video URL](https://www.youtube.com/watch?v=oHg5SJYRHA0) or drag a link into VLC's playlist, and it'll happily stream that video. **vlc-playlist-livestreamer** is a Lua extension for VLC that attempts to provide this same behaviour for sites covered by Livestreamer.

### How it works
vlc-playlist-livestreamer depends on [livestreamersrv](https://github.com/athoik/livestreamersrv), a small HTTP server that runs in the background and acts as a go-between for Livestreamer (via its Python API) and the player. livestreamersrv URLs are in the format `http://127.0.0.1:88/URL` where `URL` is the actual stream URL.

* User adds (for example) `http://twitch.tv/galedog` to VLC's playlist and presses Play
* vlc-playlist-livestreamer silently changes the URL to `http://127.0.0.1:88/twitch.tv/galedog`
* VLC requests an HTTP stream from livestreamersrv
* livestreamersrv passes the request on to the Livestreamer API
* The API sends the video stream to livestreamersrv
* livestreamersrv passes the video on to VLC and it starts playing :)

### Installation
#### Install Python if necessary
Windows: https://www.python.org/downloads/ (ensure Python is added to PATH)

Cygwin: Install the packages *python* and *python-setuptools*

Mac: `brew install python` (or equivalent)

Linux: Install the package *python*

#### Install the Livestreamer API
`pip install -U livestreamer` (newer versions of Python)

`easy_install -U livestreamer` (older versions)

#### Install livestreamersrv
https://github.com/athoik/livestreamersrv

Cygwin: `cygrunsrv -I 'Livestreamer Service' -p /*livestreamersrv_directory*/livestreamersrv -a manualstart`

Linux: Move livestreamersrv to your services directory, and run any necessary command to enable the service (e.g. `update-rc.d livestreamersrv defaults` in *init.d*-based systems).

#### Install vlc-playlist-livestreamer
Copy vlc/livestreamer.lua to VLC's lua/playlist directory:
* Windows: *VLC_Program_Files_directory*\lua\playlist\
* Mac: /Applications/VLC.app/Contents/MacOS/share/lua/playlist/
* Linux: ~/.local/share/vlc/lua/playlist/

...

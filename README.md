# vlc-playlist-livestreamer
VLC playlist extension to enable direct integration with Livestreamer

### Overview
[Livestreamer](http://docs.livestreamer.io/) is a command-line application that bypasses the "Flash-only!"-type restrictions that streaming sites such as Twitch and YouTube Live place on their streams. It acts as a middleman between the site, and the player application you *actually* want to use (VLC by default).

The downside of Livestreamer is that you have to do some CLI gymnastics every time you want to watch a stream, e.g. `livestreamer twitch.tv/peaches best`, and various GUIs have been developed to make this more user-friendly. [VLClive](https://github.com/sleighsoft/VLClive) is one example that adds a dialogue window to VLC.

VLC already has native support for video sites such as YouTube. Copy a [video URL](https://www.youtube.com/watch?v=oHg5SJYRHA0) or drag a link into VLC's playlist, and it'll happily stream that video. **vlc-playlist-livestreamer** (VPL) is a Lua extension for VLC that attempts to provide this same behaviour for sites covered by Livestreamer.

### How it works
VPL uses a modified version of [livestreamersrv](https://github.com/athoik/livestreamersrv), a small HTTP server that runs in the background and acts as a go-between for Livestreamer (via its Python API) and the player. livestreamersrv URLs are in the format `http://127.0.0.1:10088/URL` where `URL` is the actual stream URL.

* User adds (for example) `http://twitch.tv/carcinogensda` to VLC's playlist and presses Play
* VPL silently changes the URL to `http://127.0.0.1:10088/twitch.tv/carcinogensda`
* VLC requests an HTTP stream from livestreamersrv
* livestreamersrv passes the request on to the Livestreamer API
* The API sends the video stream to livestreamersrv
* livestreamersrv passes the video on to VLC and it starts playing :)

### Automated Installation
**Windows**: [Cygwin](https://www.cygwin.com/) is recommended for Windows installations. Manual installation steps for Windows without Cygwin are below.

**Cygwin**: Run `install-cygwin.sh` from the terminal. Ensure beforehand that the files are in a location you're happy to leave them. Some steps will ask for Windows administrator privileges.

**Mac**: Automated installer not yet available.

**Linux**: Automated installer not yet available.

### Manual Installation
#### Install Python 2.x/3.x if necessary
**Windows**: https://www.python.org/downloads/ (ensure Python is added to PATH)

**Cygwin**: Install the packages `python` and `python-setuptools`

**Mac**: `brew install python` (or equivalent)

**Linux**: Install the package `python`

#### Install the Livestreamer API & dependencies
`pip install -U livestreamer six` (newer versions of Python)

`easy_install -U livestreamer six` (older versions)

#### Have livestreamersrv run in the background
**Windows**: Windows background server support is very experimental right now...

`schtasks /Create /RU *Windows_username* /RP *Windows_password* /SC ONSTART /TN "Livestreamer Service" /TR "*this_directory*\livestreamersrv\livestreamersrv.bat"` and restart the system.

or https://support.microsoft.com/en-gb/kb/137890

**Cygwin**: `cygrunsrv -I 'Livestreamer Service' -p /*this_directory*/livestreamersrv/livestreamersrv`

**Linux**: Move livestreamersrv/livestreamersrv to your services directory, and run any necessary command to enable the service (e.g. `update-rc.d livestreamersrv defaults` in *init.d*-based systems). Then start the service (`/etc/init.d/livestreamersrv start`) or restart the system.

#### Install vlc-playlist-livestreamer
Copy vlc/livestreamer.lua to VLC's lua/playlist directory:
* **Windows**: *VLC_Program_Files_directory*\lua\playlist\
* **Mac**: /Applications/VLC.app/Contents/MacOS/share/lua/playlist/
* **Linux**: ~/.local/share/vlc/lua/playlist/

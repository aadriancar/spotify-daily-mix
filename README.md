# Daily Mix

Daily Mix is a Python-based tool and custom playlist generator designed to reclaim the "Daily Drive" experience after [its removal from Spotify in March 2026](https://www.distractify.com/p/what-happened-to-daily-drive-spotify). While the original lacked customization, Daily Mix introduces "recipes," which are user-defined layouts (e.g. `PSPSSSP`) that let you dictate exactly how you want your podcasts and music to play out.

*You must have Python downloaded and a Spotify Premium membership to use Daily Mix.*
> **Why Spotify Premium?** Ever since [February 2026](https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security), Spotify's Development Mode (what is needed to run Daily Mix) is only restricted to those who have a Spotify Premium account.

## Setup
In order for Daily Mix to work, a few steps need to be made.
1. Go to https://developer.spotify.com/dashboard and log into your Spotify account.
2. Click the **Create app** button.
3. Fill out the following blanks:
    - **App name:** `Daily Mix`
    - **App description:** `Custom playlist generator`
    - **Redirect URIs:** `http://127.0.0.1:8888/callback`
    - **Which API/SDKs are you planning to use?:** Select *Web API*.
4. Click the **Save** button.
5. Copy down your **Client ID** and **Client secret**. You will need this for later.

## Installation
Daily Mix can be installed through 3 different options.
### Option A: Remote Installation (Requires Git)
```
cd path/to/folder
python -m venv .venv
source .venv/bin/activate

pip install git+https://github.com/aadriancar/spotify-daily-mix.git
```
### Option B: Local Installation (Requires Git)
```
git clone https://github.com/aadriancar/spotify-daily-mix.git

cd spotify-daily-mix
python -m venv .venv
source .venv/bin/activate

pip install .
```
### Option C: Manual Download (Does not require Git)
1. Download ZIP from GitHub
2. Extract ZIP to desired folder
3. Open terminal, navigate to folder (`cd path/to/folder`)
4. Create a virtual environment and install package
```
python -m venv .venv
source .venv/bin/activate

pip install .
```

## Usage
Then, use the function `dmsetup` to setup Daily Mix, using your **Client ID** and **Client secret** from earlier.
```
dmsetup
```
Finally, run the program using `dailymix`.
```
dailymix
```

> With Daily Mix, the user has the option to pull their song choices from an existing playlist that they own. While I would love to allow the user to pull songs from *any* public playlist, Spotify removed the ability to do so in February 2026 (documentation can be found [here](https://developer.spotify.com/documentation/web-api/references/changes/february-2026)). Thus, the easiest workaround for this problem is to clone the playlist of your choice by clicking the three dots found in the playlist's menu, clicking *Add to other playlist*, then *New playlist*. Now, the user will be able to use that playlist for their Daily Mix.

### Automation & Updating Playlists
Daily Mix currently does not natively support automatic updates to the playlists. For now, each playlist can be manually updated through the menu of `dailymix`, and doing so will update all podcasts to their latest episodes, along with a new random selection of songs (if chosen from an existing playlist). If more than one podcast is assigned to the same spot in the layout, updating the playlist will take the latest episode out of the chosen podcasts.

Since Daily Mix is a Python script, it can be setup to run automatically if setup locally. Windows, Mac, and Linux all have their own tools to be able to do so. The user is encouraged to look more into this if they would like.

## Improvements
Any feedback or notes for improvement is welcome! This project is open-source after all :)

## Social Network
- **LinkedIn:** https://www.linkedin.com/in/adrian-carnate/
- **GitHub:** https://github.com/aadriancar/
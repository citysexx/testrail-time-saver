# About 
This is a mini-life simplifier for QA specialists.

## Motivation
I got pissed off by the fact that as soon as the new build comes out, you gotta manually set your tests to retest. 
In big commercial projects this can take 1-2 hours just clicking. This is not my cup of tea so I made this script that automatizes monotous work for me and you.

While I was thinking about it, I came to a conclusion that this repo must contain not only "move all to retest" feature, so I made this script easily scalable to all additional actions that you usually consider monotonous and time-consuming.

## Features
1. Set all tests in the selected project and test plan to `RETEST`

## Support
This script works on Linux. For Windows, manual tweaks will be needed.

## Dependencies
- `python3` (3.9 or higher)
- you may need `python3-venv` package for linux. I say you MAY because some distros like Red Hat do not need this dependency. Please follow your distribution guides to install this package.
Tested on Ubuntu and Arch Linux.
Arch: `pacman -S python3-venv`
Ubuntu: `apt install python3-venv` 

## Usage
- clone this repository `git clone https://github.com/citysexx/testrail-time-saver.git`
- `cd testrail-time-saver/`
- `chmod +x start.sh`
- launch `start.sh` without sudo privileges, enter your credentials and good to go!
**Note**: The creds are being saved locally at your folder and do not go anywhere. You can reuse the script without re-entering creds again OR you may rewrite them

## Contact me and help contribute please
https://t.me/gordmitrii

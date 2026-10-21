# Python script to autoplay bird audio tracks from Macaulay Library and Xeno-Canto

Imagine that you are preparing for a birding trip to a beautiful broadleaf forest (one of my favorite habitats). You would really like to become familiar with a list of vocalizations but do not have enough time to dedicate to listening. Aha! Now you can try to passively learn them anytime your laptop is open!

This is a reasonably lightweight Python utility that allows you to autoplay recordings from Macaulay Library and Xeno-Canto, since I have not been able to find an existing utility that does this. I have been able to run this alongside relatively heavy image-analysis code.

This utility was largely written by me, with implementation of the Lua script carried out using Gemini through Yale's Clarity Portal. The specific implementation details are clearly commented in the `.py` file. Due diligence has been carried out to ensure that this assistance does only what is desired. In general, the code is deliberately commented for readability, with birders with limited coding familiarity in mind. If there are concerns, do reach out! I will likely not update this code further, but encourage anyone interested to do so.


## How it works
This script does not scrape websites or attempt to automate a browser. It simply utilizes your clipboard and the fact that media links have a known form. After setup, it works as follows:

1. Open an ML/XC species or search-results page in your browser. Ensure that it displays as a grid or list; the gallery display will not work.
2. Copy the page contents:
   - Press `Ctrl+A` to select all
   - Press `Ctrl+C` to copy
3. Run `bird_stream.py` or click the conveniently set-up icon (instructions below).
4. The script searches your clipboard for
   - `ML...`: Macaulay Library recording IDs
   - `XC...`: Xeno-Canto recording IDs
5. Recordings are added to an mpv playlist and played sequentially

While mpv is open, you can press **`b`** or left-click the player window to open the current recording’s catalogue page in your default browser. Existing mpv keys allow you to switch between recordings.

## Requirements
Before using the script, install:
- [Python 3](https://www.python.org/downloads/)
- [mpv](https://mpv.io/)
  - This script was developed with [shinchiro’s Windows builds of mpv](https://github.com/shinchiro/mpv-winbuild-cmake/releases).
- The Python package `pyperclip`, which allows the script to read clipboard contents

## Setup
1. Download the files from this repository (or clone the repo)
2. Locate the mpv installation and copy the path. Open `bird_stream.py` and update MPV_EXE_PATH.
3. You can now run the `bird_stream.py` from either your chosen python IDE(I like Pycharm and Spyder) or from the terminal using `py "C:\path\to\bird_stream.py"`. If that does not work I would recommend trying `python "C:\path\to\bird_stream.py"`. NOTE: ensure that you replace these dummy paths with the actual path to `bird_stream.py`.

### Setting up a Desktop Shortcut (and Taskbar if you want it)
1. Locate the downloaded files and copy their paths. Open the `run_bird_stream.bat` file and update the path to the python file path and save it. 
2. Right click on an empty area of your desktop. Choose New --> Shortcut. Paste or browse to obtain the path to your .bat file and click Next. Give the shortcut a name (it can be absolutely anything). Click Finish and it should be on your Desktop
3. You can (optionally) change the icon to this shortcut by right clicking on it and picking change icon. There are free sites that will allow you to convert any png to an icon and you again just need the path to your desired icon (or pick from the boring standard options) and click OK
4. If you wish to have this pinned to your Taskbar, right click on the icon again and go through the full list of options until you stumble on "Pin to Taskbar".
5. Now its super easy. Simply execute the steps from the How it Works section above. 

## Troubleshooting
Reiterating some of the issues you may run into:
1. Ensure the paths are updated in a) the MPV path in the .py file, b) the .py file path in the .bat file, c) the .bat file in the optional icon setup 
2. The .bat file uses `py "C:\path\to\bird_stream.py"`. If that does not work I would recommend trying `python "C:\path\to\bird_stream.py"`
3. Clipboard is empty: You need to copy the page before starting the script or launching it by clicking the icon
4. No ML/XC streams: If you copy the site while it is in Gallery display instead of Grid or List display, no catalogue numbers are copied. The clipboard will therefore contain no accessible streams.
5. If you are using an operating system other than Windows, you may need to do some additional Googling and make updates for the script to run smoothly



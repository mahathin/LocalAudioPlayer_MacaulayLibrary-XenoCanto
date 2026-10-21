# Python script to autoplay bird audio tracks from Macaulay Library and XenoCanto

If you are a birder, you have likely wished you could listen to species specific bird calls while working. After a bunch of trial-and-error, here is a no application utility that allows you to do sequentially autoplay tracks from Macaulay Library and Xeno-Canto. 

This script avoids dealing with web scrapers or API rate limits and instead uses the following workflow: copy the contents of any species or search page from your web browser (Ctrl+A -> Ctrl+C), and then run the script. It extracts the catalog numbers in your search using the markers of "XC..." and "ML..." and plays them using an MPV.

The prerequisites for this are to have Python and an MPV player (and install some python packages). I use shinchiro mpv and the script is designed around it, and you may need to modify it based off . And additionally I use a python package, pyperclip to read off the clipboard you copy the page onto. 

Once you have the bird_stream.py script on your laptop, you will need to change the path to the mpv. Once you do this you should be able to run this locally on your python IDE(my choice is to use Pycharm/Spyder). 
In principle you can run this from your terminal, I personally find it a nuisance to manually enter the path since we need the clipboard. An alternative is to set up a desktop/taskbar short cut using run_bird_stream.bat file. Here you will need to open this file on notepad and edit the path to the python file and save it. 


Note: I use the Python Launcher in the bat file via the call "py "C:(yourpath)\bird_stream.py"" if this throws errors after replacing the path, try "python "C:(yourpath)\bird_stream.py"".


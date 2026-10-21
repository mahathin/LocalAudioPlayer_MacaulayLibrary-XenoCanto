#!/usr/bin/env python3

# import necessary packages
import os
import re
import subprocess
import sys
import tempfile

try:
    import pyperclip
except ImportError:
    print("Error: Please install pyperclip(using say pip) to use the clipboard")
    sys.exit(1)

# Sample path to mpv on windows (the form of this path will change for other os) - UPDATE THIS WITH YOUR PATH!!!
MPV_EXE_PATH = r"C:\Program Files\MPV Player\mpv.exe" 

# Function definitions:

# Function 1:
"""
    Extract supported catalogue IDs from the clipboard text and convert them to stream entries.
    
    Parameters
    data : this is a string, and specifically is text from the clipboard to search for catalogue ID's.

    Returns
    list[tuple[str, str]] :
        A list of (stream_url, title) pairs. For example:

            [
                (
                    "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/12345",
                    "ML12345",
                ),
                (
                    "https://www.xeno-canto.org/67890/download",
                    "XC67890",
                ),
            ]

    Notes:
    Despite the following not being issues for the use case I designed this code for the following are true: 
    - Matching is case-insensitive, so "ml12345" and "ML12345" both work
    - Spaces between the prefix and number are allowed, e.g. "ML 12345".
    - dict.fromkeys(...) removes duplicate IDs while preserving their first-seen order in the input text.
"""
def process_input(data):
    streams = []

    # Find Macaulay Library/Xeno Canto IDs:
    #
    # \b  = defines a word boundary, may prevent a match inside a larger word and may need to modified for expanded use cases
    # ML/XC  = literal "ML" or "XC"
    # \s*  = zero or more spaces, allowing "ML123" or "ML 123"
    # \d{4,10} = an ID of 4 through 10 digits and for XC \d{3,8} for 3 through 8 digits
    # Parentheses make re.findall return just the numeric part
    ml_matches = re.findall(r"\bML\s*(\d{4,10})\b", data, re.IGNORECASE)
    xc_matches = re.findall(r"\bXC\s*(\d{3,8})\b", data, re.IGNORECASE)

    # Create Macaulay Library/Xeno-canto stream entries:
    # dict.fromkeys(...) is a convenient ordered de-duplication technique: this skips duplicate IDs but maintains first occurrence based order
    for asset_id in dict.fromkeys(ml_matches):
        stream_url = (
            f"https://cdn.download.ams.birds.cornell.edu/api/v1/asset/{asset_id}"
        )
        title = f"ML{asset_id}"

        # The title is included in the M3U8 playlist and is used for to generate titles in the mpv's media-title property and I use it again to generate catalogue page URLs using Lua script to act almost like a hyperlink
        streams.append((stream_url, title))
      
    for xeno_canto_id in dict.fromkeys(xc_matches):
        stream_url = f"https://www.xeno-canto.org/{xeno_canto_id}/download"
        title = f"XC{xeno_canto_id}"
        streams.append((stream_url, title))

    return streams

# Function 2:
"""
    Create a temporary extended-M3U playlist for mpv:

    Parameters
    streams: list[tuple[str, str]] that are returned by process_input(), each containing a stream URL and catalogue number as a display title

    Returns
    A string that is the path to the the temporary .m3u8 file

    The file is created with delete=False because mpv needs to access it after python closes the file. It is deleted later in play_queue()
"""

def write_playlist(streams):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".m3u8", delete=False, encoding="utf-8") as playlist_file:
        # Required header for an extended M3U playlist
        playlist_file.write("#EXTM3U\n")

        for stream_url, title in streams:
            # #EXTINF provides metadata for the next media URL and -1 means that the recording duration is unknown
            playlist_file.write(f"#EXTINF:-1,{title}\n")
            playlist_file.write(f"{stream_url}\n")

        return playlist_file.name

# Function 3:
"""
    Write the embedded mpv Lua helper to a temporary .lua file

    Returns
    A str that is the path to the temporary Lua script

    mpv is given this file using --script=..., enabling the key and mouse bindings defined in LUA_SCRIPT_CONTENT below

    This section of the code to implement LUA was generated using Gemini of Yale's Clarity Portal
"""
def write_lua_script():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".lua", delete=False, encoding="utf-8") as lua_file:
        lua_file.write(LUA_SCRIPT_CONTENT)
        return lua_file.name

# Function 4:
"""
    Cleanup temporary files to ensure they do not accumulate
"""
def remove_file_if_present(path):
    if os.path.exists(path):
        os.remove(path)

# Function 5:
"""
    Launch mpv and play the supplied stream entries as a playlist. This calls the temporary files cleanup command after mpv closes, including when mpv cannot be launched successfully

    Again some attempted metadata display and Lua integration was generated using Gemini of Yale's Clarity Portal
"""
def play_queue(streams):
    if not streams:
        print("\n[!] No valid XC or ML catalogue numbers found")
        return

    playlist_path = None
    lua_path = None
    try:
        # Create the files mpv needs before starting it
        playlist_path = write_playlist(streams)
        lua_path = write_lua_script()

        # mpv command-line arguments
        mpv_args = [
            MPV_EXE_PATH,

            # Load the helper Lua script that opens catalogue pages
            f"--script={lua_path}",

            # Keep a visible mpv window even for audio-only streams
            "--force-window=yes",

            # Skip ordinary media metadata tags display (only cause I haven't successfully got it to work so far)
            "--display-tags=",

            # Set the window title to the playlist title, such as ML12345
            "--title=${media-title}",

            # Display the same title as mpv's on-screen message
            "--osd-msg1=${media-title}",

            # Presentation settings for the compact player window
            "--osd-font-size=36",
            "--osd-align-x=center",
            "--osd-align-y=center",
            "--geometry=450x180",

            # The playlist must come last because it is the media input
            playlist_path,
        ]

        # check=False means a non-zero mpv exit status will not raise an error. Allows us to simply close mpv normally.
        subprocess.run(mpv_args, check=False)

    except FileNotFoundError:
        # Usually means MPV_EXE_PATH is incorrect or mpv is not installed
        print(f"\n[!] Error: mpv executable not found at:\n    {MPV_EXE_PATH}")

    finally:
        # Delete files even if mpv fails to launch or the user closes it
        if playlist_path:
            remove_file_if_present(playlist_path)

        if lua_path:
            remove_file_if_present(lua_path)


# mpv Lua helper - Reiterating previous comments, this block of the code was implemented using Gemini of Yale's Clarity Portal
# syntax in this block changes to that of Lua. This can be confusing but for someone trying to read the code, "--" is used to comment
# For someone attempting to edit this would recommend looking up Lua syntax. I would consider it quite accessible to a python user. 

"""
This is used to bind the media link to the mpv player allowing the user to either left click or click "b" to open the media link in their default browser. 
This serves as way of accessing the metadata quickly. 
"""

LUA_SCRIPT_CONTENT = r"""
Open the catalogue page for the recording currently playing in mpv
local function open_catalogue_page()
    -- The Python-generated M3U8 playlist sets this to values such as ML123456 or XC654321
    local title = mp.get_property("media-title")

    -- If there is no title, there is no reliable ID from which to build a URL
    if not title then
        return
    end

    -- Determine which catalogue the current track belongs to
    local ml_id = title:match("ML(%d+)")
    local xc_id = title:match("XC(%d+)")

    local url = nil

    if ml_id then
        -- Macaulay Library catalogue page
        url = "https://macaulaylibrary.org/asset/" .. ml_id

    elseif xc_id then
        -- Xeno-Canto catalogue page
        url = "https://xeno-canto.org/" .. xc_id
    end

    -- If the title did not contain a supported ID, do nothing
    if not url then
        return
    end

    -- Show a short message in the mpv window so the user knows what happened
    mp.osd_message("Opening: " .. url, 2)

    -- Open the URL through the standard Windows shell and therefore default browser. The empty string after "start" supplies a window-title argument, ensuring that a URL is treated as the target
    mp.commandv("run", "cmd", "/c", "start", "", url)
end

-- Bind "b"  and left clicks in the mpv window to opening the current recording's catalogue page.
mp.add_key_binding("b", "open_webpage", open_catalogue_page)
mp.add_key_binding("MBTN_LEFT", "open_webpage_click", open_catalogue_page)
"""

# Finally, the program entry point
if __name__ == "__main__":
    # Retrieve the current clipboard contents as text.
    clipboard_data = pyperclip.paste()

    # Avoid running searches or starting mpv when there is nothing useful to process. strip() treats whitespace-only clipboard content as empty.
    if not clipboard_data.strip():
        print("Clipboard is empty. Copy text containing ML or XC numbers first.")
        sys.exit(1)

    # Build the list of recording streams and open them in mpv.
    queue = process_input(clipboard_data)
    play_queue(queue)

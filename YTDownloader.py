# version is 2.0

# TEST
# video = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
# playlist = 'https://www.youtube.com/playlist?list=PLojpqoibx6qLXV4sQilgDG78ic8Linwgk'

# ! create code to update HTML accordingly (if mp3/mp4 files are deleted)

# import modules
from pytube import YouTube, Playlist
import subprocess
import sys
import os
import re
from datetime import timedelta



print('''
YouTube Downloader v2.1
created by Ian Zhang and Connor Carpenter

will download .mp4 from a YouTube link
can optionally download .mp3 and .ogg (.mp4 will be downloaded regardless)

input a playlist link to download every video in the playlist
selecting to download .mp3 and/or .ogg will download that file type for the whole playlist

[!] will overwrite identical filenames


''')



PATH = os.getcwd()  + '\YouTubeDownloads'

# get link of the video
link = input("Enter YouTube link:\n\n")
while True:
    if re.search('^.*((watch\?)|(\/v\/)|(-wt)|(\?feature=youtube_gdata_player)|(watch%)|(\/e(mbed)?\/)).*$',link):
        linkType = 'watch'
        break
    elif re.search('list\?list=',link):
        linkType = 'playlist'
        break
    else:
        print('[!] inputted link not recognized as a video or playlist, please re-enter link')
        link = input("Enter YouTube link:\n\n")

#download other filetypes?
print('\n\ninput other filetypes to be downloaded')
additional_download = input('ex:"mp3 ogg"\n\n').lower().replace('.','').split()

# output folder
print(f'\n\nOutput will be in folder: {PATH}\n')
while True:
    n = input('Would you like to proceed? (y/n)\n')
    if n.lower() == 'y':
        break
    elif n.lower() == 'n':
        raise Exception('Program terminated.')
    else:
        print(f"Error. \"{n}\" not recognized\n")



# download videos
def download(link, i=0):
    # create object
    uservid = YouTube(link).streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    title = uservid.title
    newTitle = uservid.title

    try:
        length = YouTube(link).length
    except TypeError:
        length = 'Error'

    #replace illegal characters
    print("\nRemoving illegal characters...\n")
    for i in [" ","\\","/",":","*","?","\"","<",">","|"]:
        newTitle = newTitle.replace(i,"")

    # download vid
    uservid.download(output_path = PATH, filename = f'{newTitle}.mp4')

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError: 
        base_path = os.path.abspath(".")
    converter = base_path + "\\ffmpeg.exe"
    #print(x) #debug

    # convert to other filetypes
    # -vn prevents downloading visual data, -y overwrites files
    if "mp3" in additional_download:
        subprocess.run(f"{converter} -i {PATH}\{newTitle}.mp4 -y {PATH}\{newTitle}.mp3")
    if "ogg" in additional_download:
        subprocess.run(f"{converter} -i {PATH}\{newTitle}.mp4 -vn -y {PATH}\{newTitle}.ogg")

    videos.append([title, newTitle, length, link])



# download video or playlist
videos = []
if linkType == 'watch':  
    download(link)
elif linkType == 'playlist':  
    for i in range(len(Playlist(link))):
        download(Playlist(link)[i], i)



#HTML code
start = '''
    <!DOCTYPE html>
<html>
<head>
    <title>YouTube Downloads</title> 
    <style>
        table {
            border:1px solid #b3adad;
            border-collapse:collapse;
            padding:5px;
        }
        table th {
            border:1px solid #b3adad;
            padding:5px;
            background: #f0f0f0;
            color: #313030;
        }
        table td {
            border:1px solid #b3adad;
            text-align:center;
            padding:5px;
            background: #ffffff;
            color: #313030;
        }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>Video Title</th>
                <th>Video Length</th>
                <th>YouTube Link</th>
                <th>Local mp4</th>
                <th>Local mp3</th>
                <th>Local ogg</th>
            </tr>
        </thead>
        <tbody>'''

body = ''
for title, newTitle, length, link in videos:
    #garunteed
    ytLink = f'<a href={link}> {link}</a>'
    length = str(timedelta(seconds=int(length)))
    local_mp4 = f'<a href=\{PATH}\{newTitle}.mp4> {newTitle}.mp4</a>'

    #check for mp3
    if os.path.isfile(f"{PATH}\{newTitle}.mp3"):
        local_mp3 = f'<a href=\{PATH}\{newTitle}.mp3> {newTitle}.mp3</a>'
    else:
        local_mp3 = '<p>no .mp3</p>'

    #check for ogg
    if os.path.isfile(f"{PATH}\{newTitle}.ogg"):
        local_ogg = f'<a href=\{PATH}\{newTitle}.ogg> {newTitle}.ogg</a>'
    else:
        local_ogg = '<p>no .ogg</p>'

    body += f'''
            <tr>
                <td>{title}</td>
                <td>{length}</td>
                <td>{ytLink}</td>
                <td>{local_mp4}</td>
                <td>{local_mp3}</td>
                <td>{local_ogg}</td>
            <tr>
    '''

end = '''
        </tbody>
    </table>
</body>
</html>'''

#if file already exists, append
#otherwise write new file
if os.path.isfile(fr'{PATH}\YouTube Video.html'):
    print('\nappending HTML file...\n')
    final = ''
    with open(fr'{PATH}\YouTube Video.html','r') as file:
        for line in file.readlines():
            if re.search('\<\/tbody\>',line):
                final += body
            final += line
        #print(final)
else:
    print('\ncreating HTML file...\n')
    final = start + body + end

# write html file
with open(f'{PATH}\YouTube Video.html','w') as file:
    file.write(final)


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


PATH = os.getcwd()  + '\YouTubeDownloads'

# get link of the video
link = input("Enter YouTube link: \n\n")
linkType = ''
while True:
    if re.search('^.*((watch\?)|(\/v\/)|(-wt)|(\?feature=youtube_gdata_player)|(watch%)|(\/e(mbed)?\/)).*$',link):
        linkType = 'watch'
        break
    elif re.search('list\?list=',link):
        linkType = 'playlist'
        break
    else:
        print('[!] inputted link not recognized as a video or playlist, please re-enter link\n\n')
        link = input("Enter YouTube link: \n\n")

# output folder
print(f'\nOutput will be in folder: {PATH}\n\n')
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
    x = base_path + "\\ffmpeg.exe"
    #print(x) #debug

    # convert to mp3
    subprocess.run(f"{x} -i {PATH}\{newTitle}.mp4 {PATH}\{newTitle}.mp3")

    videos.append([title, newTitle, length, link])

videos = []



# download video or playlist
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
    <title>HTML Table Generator</title> 
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
                <th>Local Video</th>
                <th>Local Audio</th>
            </tr>
        </thead>
        <tbody>'''

body = ''
for title, newTitle, length, link in videos:
    ytLink = f'<a href={link}> {link}</a>'
    length = str(timedelta(seconds=int(length)))
    localVideo = f'<a href=\{PATH}\{newTitle}.mp4> {newTitle}.mp4</a>'
    localAudio = f'<a href=\{PATH}\{newTitle}.mp3> {newTitle}.mp3</a>'

    body += f'''
            <tr>
                <td>{title}</td>
                <td>{length}</td>
                <td>{ytLink}</td>
                <td>{localVideo}</td>
                <td>{localAudio}</td>
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


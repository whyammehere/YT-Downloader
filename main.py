from pytube import *

vid = YouTube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

vid_title = vid.title
print(vid_title)
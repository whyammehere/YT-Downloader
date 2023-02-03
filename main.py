# import modules
from pytube import YouTube 
import subprocess
  
# get link of the video
link = input("Input video link: \n\n")
  
# download video
uservid = YouTube(link).streams.filter().first().download(output_path = "videos/", filename = 'user_vid.mp4')

# convert to audio file
subprocess.run("ffmpeg -i videos/user_vid.mp4 videos/user_audio.mp3")


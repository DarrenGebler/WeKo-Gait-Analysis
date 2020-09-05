import os

# Path to Unnormalised Videos
path = "./Videos/Unnormalised/"

# Flips videos to build initial data sets
for filename in os.listdir(path):
    directory = path+filename
    filebase = ".".join(filename.split(".")[:-1])
    os.system(f"ffmpeg -i {directory} -vf hflip -c:a copy Videos/Flipped/{filebase}_flipped.mp4")
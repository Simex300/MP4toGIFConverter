import os
import sys
import cv2
import shutil
import math
import glob
from PIL import Image

def createDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def mp4ToJpgs(path):
    video = cv2.VideoCapture(path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    reading, image = video.read()
    frameCount = 0
    while reading:
        cv2.imwrite(f"temp/frame_{frameCount:04d}.jpg", image)
        reading, image = video.read()
        frameCount += 1
    return math.floor((1/fps) * 1000)

def JpgsToGif(jpgsDirPath, toPath, filename, fps):
    images = glob.glob(f"{jpgsDirPath}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    frame_one = frames[0]
    createDir('output')
    frame_one.save(f"output/{filename}.gif", format="GIF", append_images=frames, save_all=True, duration=fps, loop=0)

if __name__ == "__main__":
    fromPath = ""
    toPath = ""
    try:
        fromPath = sys.argv[1]
    except IndexError:
        print("No path were given")
        exit()

    try:
        toPath = sys.argv[2]
    except IndexError:
        toPath = "output"

    filename = []
    if fromPath.find('\\'):
        filename = fromPath.split('\\')
    else:
        filename = fromPath.split('/')

    filename = filename[-1]
    filename, extension = tuple(filename.split("."))
    if filename.find(")") > -1:
        filename = filename[filename.index(")") + 1:]

    createDir('temp')
    frame = mp4ToJpgs(fromPath)
    JpgsToGif('temp', toPath, filename, frame)
    shutil.rmtree('temp')
    pass
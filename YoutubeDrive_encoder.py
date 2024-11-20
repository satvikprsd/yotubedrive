import binascii
import numpy as np
from PIL import Image
import cv2
import os

width,height = 1080,1920
box_size_x,box_size_y=8,8
max_limit = width*height//(box_size_x*box_size_y)

with open("pfp.png","rb") as file:
    hexdata = str(binascii.hexlify(file.read()))[2:-1]

extention = "png"

def getsubstrings(string, n=max_limit):
    length = len(string)
    if length <= n:
        return [string]
    substrings = [string[i:i+n] for i in range(0, length - n + 1, n)]
    if length % n != 0:
        substrings.append(string[-(length % n):])
    return substrings

rgb_values = [
    (255, 0, 0),         # Red
    (0, 255, 0),         # Green
    (0, 0, 255),         # Blue
    (255, 255, 0),       # Yellow
    (0, 255, 255),       # Cyan
    (255, 0, 255),       # Magenta
    (128, 0, 0),         # Dark Red
    (0, 128, 0),         # Dark Green
    (0, 0, 128),         # Dark Blue
    (128, 128, 0),       # Olive
    (128, 0, 128),       # Purple
    (0, 128, 128),       # Teal
    (192, 192, 192),     # Light Gray
    (255, 165, 0),       # Orange
    (255, 105, 180),     # Hot Pink
    (255, 255, 255)      # White
]

hex = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,'8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

hexdata = getsubstrings(hexdata)
length = len(hexdata)
print(length)
for i in range(length):
    string = hexdata[i]
    x, y = 0, 0
    data = np.zeros((width, height, 3), dtype=np.uint8)
    
    for j in string:
        color = list(rgb_values[hex[j]])
        
        for xi in range(box_size_x):
            for yj in range(box_size_y):
                data[x+xi][y+yj] = color    

        y += box_size_y
        if y > height - box_size_y: 
            y = 0
            x += box_size_x
    img = Image.fromarray(data)
    img.save(f'frames/frame{i}.png')

image_folder = 'frames'
video_name = 'video.avi'
fps = 30

images = [f"frame{i}.png" for i in range(length)]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()

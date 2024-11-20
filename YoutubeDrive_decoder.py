import cv2
import os
import numpy as np
import binascii
import time

start = time.time()
width,height = 1080,1920
box_size_x,box_size_y = 8,8
video_path = 'video.avi'
output_folder = 'frames_out'
os.makedirs(output_folder, exist_ok=True)

video = cv2.VideoCapture(video_path)
fps = video.get(cv2.CAP_PROP_FPS)
print(fps)
frame_duration = 1.0 / fps  # Duration of each frame in seconds
time_between_frames = 0.033   # Interval to capture frames (1 second)
elapsed_time = 0.0
frame_count = 0

while True:
    success, frame = video.read()
    if not success:
        break

    if elapsed_time >= time_between_frames * frame_count:
        frame_name = os.path.join(output_folder, f"frame{frame_count}.png")
        cv2.imwrite(frame_name, frame)
        frame_count += 1

    elapsed_time += frame_duration

video.release()
cv2.destroyAllWindows()

hex = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
hexstring = ""
output_indices = []
print(frame_count)
print(time.time() - start)
bgr_values = [
(0, 0, 255),         # Red
(0, 255, 0),         # Green
(255, 0, 0),         # Blue
(0, 255, 255),       # Yellow
(255, 255, 0),       # Cyan
(255, 0, 255),       # Magenta
(0, 0, 128),         # Dark Red
(0, 128, 0),         # Dark Green
(128, 0, 0),         # Dark Blue
(0, 128, 128),       # Olive
(128, 0, 128),       # Purple
(128, 128, 0),       # Teal
(192, 192, 192),     # Light Gray
(0, 165, 255),       # Orange
(180, 105, 255),     # Hot Pink
(255, 255, 255)      # White
]

bgr_values_np = np.array(bgr_values)
def closest_color_index(color):
    diff = bgr_values_np - color
    dist = np.sqrt((diff ** 2).sum(axis=1))
    return np.argmin(dist)
output_indices = []
hexstring_list = []

for i in range(frame_count):
    image = cv2.imread(f'frames_out/frame{i}.png')
    for x in range(0, width, box_size_x):
        row_indices = []
        for y in range(0, height, box_size_y):
            block = image[x:x+box_size_x, y:y+box_size_y]
            avg_color = block.mean(axis=(0, 1))
            if np.allclose(avg_color, [0, 0, 0], atol=10):
                break

            index = closest_color_index(avg_color)
            row_indices.append(index)
            hexstring_list.append(f"{index:x}")
        output_indices.append(row_indices)
        if np.allclose(avg_color, [0, 0, 0], atol=10):
            break
hexstring = ''.join(hexstring_list)
if len(hexstring)%2!=0:
    hexstring='0'+hexstring

with open("o.png", "wb") as file:
    file.write(binascii.unhexlify(hexstring))
print(time.time() - start)
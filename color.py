import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import pyttsx3
import threading

# Reading a CSV file with pandas and assigning names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Initialize the pyttsx3 text-to-speech engine
engine = pyttsx3.init()

# Function to calculate the minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to speak the color name
def speak_color_name(color_name):
    engine.say(color_name)
    engine.runAndWait()

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    frame = param[0]  # Get 'frame' from the list
    if event == cv2.EVENT_LBUTTONDBLCLK:
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        color_name = getColorName(r, g, b)

        # Display the color name and voice on the screen using Pillow
        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_frame)
        font = ImageFont.load_default()

        tag_text = f'Detected Color: {color_name}'
        voice_text = f'Voice: {color_name}'

        draw.rectangle([(0, 0), (500, 90)], fill=(255, 255, 255))
        draw.text((10, 30), tag_text, font=font, fill=(0, 0, 0))
        draw.text((10, 60), voice_text, font=font, fill=(0, 0, 0))

        frame = np.array(pil_frame)
        cv2.imshow('image', frame)

        # Start a new thread to speak the color name
        threading.Thread(target=speak_color_name, args=(color_name,)).start()

        print(tag_text)
        print(voice_text)

# Video capture from the default camera
cap = cv2.VideoCapture(0)

cv2.namedWindow('image')
frame_holder = [None]  # List to hold the frame

cv2.setMouseCallback('image', draw_function, frame_holder)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_holder[0] = frame.copy()  # Store a copy of the frame in the list
    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


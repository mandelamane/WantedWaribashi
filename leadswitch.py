import os
import time

import cv2
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from playsound import playsound

from line_notify_bot import LINENotifyBot


def make_wanted():
    pic = cv2.imread("img/taked.png")[:, :, ::-1]
    frame = cv2.imread("img/frame.png")[:, :, ::-1]

    pic = cv2.resize(pic, (540, 405))
    frame[170:575, 50:590] = pic

    cv2.imwrite("img/wanted.png", frame[:, :, ::-1])


def start_camera():
    camera = cv2.VideoCapture(0)

    print("taking picture")

    playsound("voice/camera.mp3")

    print("shutter")
    (
        ret,
        frame,
    ) = camera.read()
    time.sleep(1)

    cv2.imwrite("img/taked.png", frame[::-1, :, :])

    camera.release()
    print("finished")


def send_message(bot, message, image=None):
    bot.send(
        message=message,
        image=image,
    )


bot = LINENotifyBot(access_token=os.environ["LINE_TOKEN"])


GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

flag = False
while True:
    if GPIO.input(14) == 1:
        print("------")
        flag = False
    else:
        if not flag:
            print("sound on")
            start_camera()
            playsound("voice/hiroyuki.mp3")
            make_wanted()
            send_message(bot, message="WANTED", image="img/wanted.png")
            flag = True
        else:
            print("not sound")

    time.sleep(0.5)

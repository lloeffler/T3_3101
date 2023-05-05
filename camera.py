#!/usr/bin/python3
import datetime
import traceback
from threading import Thread, Event
from time import sleep

import cv2 as cv

event = Event()
camera = cv.VideoCapture(0)
run = True
paused = False
img_name = ''
paused_menu = 'save: saves current image\nresume: resumes image stream\nexit: quits programm\n>'


def show(event):
    try:
        while run:

            if not paused:
                _, frame = camera.read()
                if frame is not None:
                    img_name = datetime.datetime.now().isoformat()
                    cv.imshow('camera', frame)

            if paused:
                user_input = input(paused_menu)
                while user_input != 'exit' and user_input != 'resume':
                    user_input = input(paused_menu)

                if user_input == 'save':
                    cv.imwrite('{}.png'.format(img_name), frame)

                if user_input == 'resume':
                    paused = False

                if user_input == 'exit':
                    run = False
    except Exception as exception:
        print(str(exception), traceback.format_exc())


def react():
    try:
        while run:
            if not paused:
                key = input('press enter to pause.')
                paused = True
                sleep(0.5)
    except Exception as exception:
        print(str(exception), traceback.format_exc())

show_image_thread = Thread(
    group=None, target=show, daemon=True, args=(event))
react_thread = Thread(
    group=None, target=react, daemon=True)

show_image_thread.start()
react_thread.start()

show_image_thread.join()
react_thread.join()
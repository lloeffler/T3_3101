#!/usr/bin/python3

import datetime
import traceback
from threading import Thread
from time import sleep

import cv2 as cv


class Application:
    """
    Application to show what the camera sees, take a picture and pause the videostreamlike showed images.
    """

    def __init__(self):
        self.camera = cv.VideoCapture(0)
        self.run = True
        self.paused = False
        self.img_name = ''
        self.paused_menu = '{}\nsave: saves current image\nresume: resumes image stream\nexit: quits programm\n>'

    def main(self):
        """
        The main function, that executes the programm.
        """

        def show():
            """
            Threaded function to show streamlike images from the camera and handle pause menu with userinput.
            """
            try:
                while self.run:

                    # Videostreamlike image output.
                    if not self.paused:
                        _, frame = self.camera.read()
                        if frame is not None and _ is not None:
                            img_name = datetime.datetime.now().__str__()
                            cv.imshow('camera', frame)
                            # Needed show image.
                            cv.waitKey(1)
                        else:
                            print('no image')

                    # Pause menue
                    if self.paused:
                        # Read user input.
                        user_input = input(self.paused_menu.format(img_name))
                        while user_input != 'exit' and user_input != 'resume':
                            user_input = input(self.paused_menu.format(img_name))

                        # Save image, if user input was save.
                        if user_input == 'save':
                            cv.imwrite('{}.png'.format(img_name), frame)

                        # Resume execution.
                        if user_input == 'resume':
                            self.paused = False

                        # Stops execution and lead tu application exit.
                        if user_input == 'exit':
                            self.run = False
                            cv.destroyAllWindows()
            except Exception as exception:
                print(str(exception), traceback.format_exc())

        def pause():
            """
            Pauses stream like execution and let show thread run into pause menue.
            """
            try:
                while self.run:
                    if not self.paused:
                        input('press enter to pause.')
                        self.paused = True
                        sleep(0.5)
            except Exception as exception:
                print(str(exception), traceback.format_exc())

        # Generate threads.
        show_image_thread = Thread(
            group=None, target=show, daemon=True)
        pause_thread = Thread(
            group=None, target=pause, daemon=True)

        if self.camera.isOpened():
            # Start threads.
            show_image_thread.start()
            pause_thread.start()

            # Join threads.
            show_image_thread.join()
            pause_thread.join()
        else:
            print('could not open camera')


if __name__ == '__main__':
    try:
        application = Application()
        application.main()
    except Exception as exception:
        print(str(exception), traceback.format_exc())

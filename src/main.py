from datetime import datetime, timedelta
from pathlib import Path
import pygetwindow as gw
import os
import pyautogui
import time

from src.detector import detect_objects
from src.send_mail import EmailThread

PICTURES_FOLDER = '\\Pictures\\'
PNG = '_.png'
IMG_SUBNAME = 'a_'
SECONDS_TIME = 6000  # 10 minutes
WINDOW_TITLE = 'Imou'


def take_screenshot(secs):
    now = datetime.now().strftime("%H_%M_%S")
    time.sleep(secs)
    Path(os.getcwd() + PICTURES_FOLDER).mkdir(parents=True, exist_ok=True)

    p = pyautogui.screenshot()
    p = p.crop((230, 80, 1900, 920))
    p.save(os.getcwd() + PICTURES_FOLDER + IMG_SUBNAME + str(now) + PNG)

    return os.getcwd() + PICTURES_FOLDER + IMG_SUBNAME + str(now) + PNG


if __name__ == "__main__":
    verbose = False
    seconds = 1
    number_of_screenshots = 3
    print("Started script: " + datetime.now().strftime("%H:%M:%S"))
    end_time = datetime.now() + timedelta(seconds=number_of_screenshots)
    print("Script will end at: " + end_time.strftime("%H:%M:%S"))

    if verbose:
        z1 = gw.getAllTitles()
        print(z1)

    this = gw.getWindowsWithTitle(WINDOW_TITLE)[0]
    this.maximize()

    for a in range(number_of_screenshots):

        path = take_screenshot(seconds)
        processed_path = detect_objects(path)

        if processed_path != 'no_objects':

            def thread_function(processed_path_image):
                email_sender = EmailThread(processed_path_image)
                email_sender.start()
                print('Detected objects, sending mail')

            thread_function(processed_path)

    this.minimize()

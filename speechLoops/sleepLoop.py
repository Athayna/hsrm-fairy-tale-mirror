import multiprocessing
from speechLoops.speechLoop import SpeechLoop
import pandas as panda
import cv2
import time
from datetime import datetime
from numpy import sum

class SleepLoop(SpeechLoop):
    """This is the sleep loop. It is the first loop that is called when the program starts."""

    def __init__(self, handler) -> None:
        super().__init__(handler)

    def play(self) -> None:
        """This method is called when the loop is started. It is used to start the speech recognition and to set the next loop."""
        if not self.handler.sleeping:
            self.handler.sleeping = True
            self.handler.imagePlayer.setImage("gesicht-schlafen")

        motionEvent = multiprocessing.Event()

        motionProcess = multiprocessing.Process(target=detectMotion, args=[motionEvent])
        motionProcess.start()

        while 1:
            self.handler.result = self.listen(showPictures=False)

            print('sleepy sleepy')

            if any(x in self.handler.result for x in ("spiegel", "spieglein")) or motionEvent.is_set():
                self.handler.result = ""
                self.handler.sleeping = False
                if motionProcess.is_alive():
                    motionProcess.terminate()
                self.handler.setSpeechLoop(self.handler.getSpeechLoop("welcomeLoop"))
                return
        
def detectMotion(event):
    initialState = None
    # motionTrackList = [None, None]
    motionTime = []
    # dataFrame = panda.DataFrame(columns = ["Initial", "Final"])

    # starting the webCam to capturethe video using cv2 module
    video = cv2.VideoCapture(1)

    timeSinceSleep = time.time()
    countTime = time.time()
    initialDifference = 0
    # using infinite loop to capture the frames from the video
    while 1:
        # reading each image or frame from the video using read function
        check, cur_frame = video.read()
        timeSinceSleep = time.time() - timeSinceSleep

        # from color images creating a gray frame
        if(check == False):
            continue
        gray_image = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)

        # to find the changes creating a gaussian blur from the gray scale image
        gray_frame = cv2.GaussianBlur(gray_image, (21, 21), 0)

        # for the first iteration checking the condition
        # assign greyframe to initial state if it is none
        timeDiff = time.time() - countTime
        print(f'TimeDiff: {timeDiff}')
        if (initialState is None) or (timeDiff > 10):
            initialState = gray_frame
            countTime = time.time()
            initialDifference = 0
            continue

        # calculation of difference between static or initial and gray frame
        differ_frame = cv2.absdiff(initialState, gray_frame)

        # the change between static or initial background and current gray frame are highlighted
        thresh_frame1, thresh_frame2 = cv2.threshold(differ_frame, 30, 255, cv2.THRESH_BINARY)
        thresh_frame2 = cv2.dilate(thresh_frame2, None, iterations=2)

        # detect if something has changed
        h, w = thresh_frame2.shape
        err = sum(differ_frame)
        mse = err / (float(h * w))
        print(f'Mse is: {mse}. InitialDifference is {initialDifference}')
        if initialDifference == 0:
            initialDifference = mse
            print('if')
            continue
        else:
            diff = abs(initialDifference - mse)
            print(f'Else | Diff is: {diff}')
            if (timeSinceSleep > 10) and (diff > 5 and diff < 20):
                initialDifference = mse
                event.set()
                video.release()
                return
        time.sleep(1)

    # releasing the video
    video.release()
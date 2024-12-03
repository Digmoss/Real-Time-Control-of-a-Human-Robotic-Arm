#! /usr/bin/python3
import cv2
import board
import busio
from picamera2 import Picamera2
from adafruit_servokit import ServoKit
from cvzone.HandTrackingModule import HandDetector

thumb_close = 0
thumb_open = 180
index_close = 0
index_open = 180
middle_close = 0
middle_open = 180
ring_close = 180
ring_open = 0
pinky_close = 180
pinky_open = 0

i2c = busio.I2C(board.SCL, board.SDA)
kit = ServoKit(address=0X40, i2c=i2c, frequency=50, channels=16)
detector = HandDetector(maxHands=1, detectionCon=0.8)
piCam=Picamera2()
piCam.preview_configuration.main.size=(1280, 720)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

def makemove(values):
    if values[0] == 1:
        kit.servo[0].angle = thumb_open
    else:
        kit.servo[0].angle = thumb_close
    if values[1] == 1:
        kit.servo[1].angle = index_open
    else:
        kit.servo[1].angle = index_close
    if values[2] == 1:
        kit.servo[2].angle = middle_open
    else:
        kit.servo[2].angle = middle_close
    if values[3] == 1:
        kit.servo[3].angle = ring_open
    else:
        kit.servo[3].angle = ring_close
    if values[4] == 1:
        kit.servo[4].angle = pinky_open
    else:
        kit.servo[4].angle = pinky_close


while True:
    img = piCam.capture_array()
    img= cv2.flip(img, 1)
    hand = detector.findHands(img, draw=False)
    if hand:
        lmList = hand[0]
        if lmList:
            fingers = detector.fingersUp(lmList)
            if fingers:
                makemove(fingers)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
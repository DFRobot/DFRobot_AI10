# -*- coding: utf-8 -*
'''!
  @file continuous_recognition.py
  @brief This example demonstrates how to use the continuous recognition function of the AI-10 module.
  @copyright	Copyright (c) 2025 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license The MIT License (MIT)
  @author [jiali](zhixinliu@dfrobot.com)
  @version V1.0
  @date 2025-7-13
  @url https://github.com/DFRobot/DFRobot_AI10
'''
from __future__ import print_function
import sys
import os
sys.path.append("../")
import time
import RPi.GPIO as GPIO
from DFRobot_AI10 import *

recognize = DFRobot_AI10_UART(115200)


def setup():
  while (recognize.begin() == False):
    print("Sensor initialize failed!!")
    time.sleep(1)

  print("Sensor initialize success!!")
  
  #Enable face frame
  if recognize.enable_face_frame():
    print("Face frame enabled!")

def loop():
  #Continuous recognition result
  recDat = struct_recognition_data()

  '''! When a human face is detected,  the system automatically starts the recognition process.
  After the person moves away for x seconds, the recognition stops and the module continues with low-power face detection.
  the range is 3-20s. 
  '''
  print("=================================")
  print("Recognize...")
  
  recDat = recognize.start_continuous_face_recognition(5)#5s timeout

  #Print the recognition result
  if recDat.result == 0:
    print("recognition success")
    if recDat.type == recognize.TYPE_QR:
      print("Recognition type: QR code")
      print("QR code data: ", recDat.QR_date)
    else:
      if recDat.type == recognize.TYPE_FACE:
        print("Recognition type: Face")
      else:
        print("Recognition type: Plam")
      print("User ID: ", recDat.uid) 
      print("User name: ",recDat.user_name)  
      print("Admin Permission: ","Normal" if recDat.admin == recognize.NORMAL else "Admin")

  else:
    print("Recognition failed!")
    print("Error code: ", recDat.result)
    if recDat.result == 13:
      print("Recognition timed out!")
    elif recDat.result == 4:
      print("Camera error!")
    elif recDat.result == 12:
      print("Live check failed!")
    else:
      print()
  print("=================================")

  time.sleep(0.1)

if __name__ == "__main__":
  setup()
  while True:
    loop()

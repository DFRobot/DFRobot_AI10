# -*- coding: utf-8 -*
'''!
  @file single_registered_user.py
  @brief This example demonstrates how to enroll a single registered user.
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
import termios
import tty
from DFRobot_AI10 import *

recognize = DFRobot_AI10_UART(115200)

def enroll_once():
  print("Start to enroll a user...")
  
  #User enroll result anc information
  udata = struct_user_info()

  #admin permission is required to register a user. NORMAL：average person ，ADMIN: administrator
  #userName registered user name, the length is 32 bytes at most
  #timeout is the time to wait for the recognition result, the range is 3-20 seconds

  udata =recognize.enroll_user(recognize.NORMAL,"User1",5)

  #Check if the registration is successful, if successful, print the user information
  if(udata.result == recognize.Success):
    print("Enroll user success!")
    print("User ID: ",udata.uid)
    print("User name: ",udata.user_name)
    print("Admin permission: ","Normal" if udata.admin == recognize.NORMAL else "Admin")
    print("User enrolled type: ","Face" if udata.type == recognize.TYPE_FACE else "Palm")
  elif(udata.result == recognize.FailedFaceEnrolled):
    print("Failed to enroll user, user already enrolled!")
  else:
    print("Enroll user failed!")


def getch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(fd)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch


def setup():
  while (recognize.begin() == False):
    print("Sensor initialize failed!")
    time.sleep(1)
  
  print("Sensor initialize success!")

def loop():
  enroll_once()
  print("Press Enter to continue enrolling, press any other key to exit.···")
  key = getch()
  if key != '\r' and key != '\n':
    sys.exit()


if __name__ == "__main__":
  setup()
  while True:
    loop()

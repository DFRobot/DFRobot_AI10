# -*- coding: utf-8 -*
'''!
  @file operate_user_data.py
  @brief operate user data
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
    print("Sensor initialize failed!")
    time.sleep(1)
  
  print("Sensor initialize success!")
  
  print("AI10 An example of AT command control")
  print("-----------------------------")
  print("Available commands:")
  print("AT+GETUSERS       # Get all user information")
  print("AT+DELUSER=ID     # Delete the specified user (e.g. AT+DELUSER=0x1001)")
  print("AT+DELALLUSERS    # Delete all users")
  print("-----------------------------")
  

def loop():
  user_input = input(">> ").strip().upper()
  all_data = struct_All_User_ID()
  if user_input == "AT+GETUSERS":

    print("Get all user information")
    # Get all user information
    all_data = recognize.get_all_user_ids()
    if all_data.result == 0x00:
      print("Get all user ID success!")
      print("User number:",all_data.user_num)
      print("User ID :")
      for i in range(0,all_data.user_num):
        print(all_data.uids[i],end = ' ')
      print("")
    print("OK")
  elif user_input.startswith("AT+DELUSER="):
    user_id = int(user_input.split("=")[1])
    # Delete the user with the specified ID
    if recognize.delete_user(user_id):
      print("successfully deleted!")
    print("OK")
    
  elif user_input == "AT+DELALLUSERS":
    # Delete all users
    if recognize.delete_all_user():
      print("successfully deleted!")
    print("OK")

  else:
    print("The command is incorrect!")

  time.sleep(0.1)

if __name__ == "__main__":
  setup()
  while True:
    loop()

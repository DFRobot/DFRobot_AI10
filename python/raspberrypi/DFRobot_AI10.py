# -*- coding: utf-8 -*
'''!
  @file DFRobot_AI10.py
  @brief DFRobot_AI10 Class infrastructure, implementation of underlying methods
  @copyright	Copyright (c) 2025 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license The MIT License (MIT)
  @author [jiali](zhixinliu@dfrobot.com)
  @version V1.0
  @date 2025-7-13
  @url https://github.com/DFRobot/DFRobot_AI10
'''
import serial
import time

class struct_enroll_result_data:
  def __init__(self):
    self.result = 0
    self.uid = 0
    self.type = 0

    self.nid = 0
    self.face_data = [0x0000]*8
    '''!
    face_data[0]state
    face_data[1]left
    face_data[3]right
    face_data[4]bottom
    face_data[5]yaw
    face_data[6]pitch
    face_data[7]roll
    '''
class struct_recv_pack:
  def __init__(self):
    self.result = 0
    self.mid = 0
    self.data_len = 0
    self.data = [0x00] * 256
    self.nid = 0
    self.face_data = [0x0000]*8

class struct_All_User_ID:
  def __init__(self):
    self.user_num = 0
    self.uids = [0x0000] * 100
    self.result = 0

class struct_user_info:
  def __init__(self):
    self.uid = 0
    self.user_name = ""
    self.admin = 0
    self.type = 0
    self.result = 0

class struct_recognition_data:
  def __init__(self):
    self.result = 0
    self.type = 0
    self.uid = 0
    self.user_name = ""
    self.admin = 0
    self.QR_date = ""
    self.nid = 0
    self.face_data = [0x0000]*8

TIME_OUT                     =   0x64
CMD_TIME_OUT                 =   0x03
SYNCWORD_H                   =   0xEF
SYNCWORD_L                   =   0xAA
MID_RELAY                    =   0x00
MID_NOTE                     =   0x01

RESET                        =   0x10
ENROLL_SINGLE                =   0x1D
MID_GET_ALL_USERID           =   0x24
GET_USER_INFO                =   0x22
DEL_USER                     =   0x20
DEL_ALL_USER                 =   0x21
SET_FACE__LOCATION_DISPLAY   =   0xB5
VERIFY                       =   0x12
MID_SCAN_QR_CODE             =   0x70

FACE_DIRECTION_UP            =   0x10
FACE_DIRECTION_DOWN          =   0x08
FACE_DIRECTION_LEFT          =   0x04
FACE_DIRECTION_RIGHT         =   0x02
FACE_DIRECTION_MIDDLE        =   0x01
FACE_DIRECTION_UNDEFINE      =   0x00

class DFRobot_AI10(object):
  ## Continuous recognition status
  __continue_verify = 0x00
  ## Type error
  TYPE_NULL = 0x00
  ## Face type
  TYPE_FACE = 0x01
  ## Palm type
  TYPE_PALM = 0x02
  ## QR code type
  TYPE_QR   = 0x03

  ## Normal user
  NORMAL = 0x00
  ## Admin user
  ADMIN = 0x01

  Success = 0x00
  FailedFaceEnrolled  = 0x0A

  def __init__(self, baud):
    self.ser = serial.Serial('/dev/ttyAMA0', baudrate = baud,bytesize=8,parity="N",stopbits = 1 ,timeout=0.5)
    if self.ser.isOpen == False:
        self.ser.open()

  def begin(self):
    '''!
      @brief begin 
    '''
    time.sleep(0.05)
    return self.drv_reset() 

  def start_continuous_face_recognition(self,timeout):
    '''!
      @brief Start continuous face recognition
      @param timeout: Timeout time (3-20s)
      @return recognize the result
      @n      result        Instruction execution result
      @retval  0x00:        Recognition success
      @retval  default:     Recognition failure
      @n      type:         Recognition types
      @retval  TYPE_NULL:   Undefine
      @retval  TYPE_FACE:   Face recognition
      @retval  TYPE_PALM:   Palm recognition
      @retval  TYPE_QR:     QR code recognition
      @n      uid:          user ID
      @n      user_name     Recognition user name 
      @n      admin:        Recognition user permissions
      @retval  NORMAL:      Normal user
      @retval  ADMIN:       Admin user
      @n      QR_date:      The QR code data
    '''

    data_buf = [0x00]*20
    self.__continue_verify = 0x01

    data_buf[0] = VERIFY & 0xFF
    data_buf[1] = (0x02 >> 8) & 0xFF
    data_buf[2] = (0x02 >> 0) & 0xFF
    data_buf[3] = self.__continue_verify & 0xFF
    data_buf[4] = timeout & 0xFF

    self.send_package(data_buf,5)
    recv_pack = struct_recv_pack()
    recv_pack = self.recv_package(timeout)

    return self.recognition_data_analysis(recv_pack)

  def get_recognition_result(self,timeout):
    '''!
      @brief Recognize once at a time
      @param timeout: Timeout time (3-20s)
      @return recognize the result
      @n      result        Instruction execution result
      @retval  0x00:        Recognition success
      @retval  default:     Recognition failure
      @n      type:         Recognition types
      @retval  TYPE_NULL:   Undefine
      @retval  TYPE_FACE:   Face recognition
      @retval  TYPE_PALM:   Palm recognition
      @retval  TYPE_QR:     QR code recognition
      @n      uid:          user ID
      @n      user_name     Recognition user name 
      @n      admin:        Recognition user permissions
      @retval  NORMAL:      Normal user
      @retval  ADMIN:       Admin user
      @n      QR_date:      The QR code data
    '''
    data_buf = [0x00]*20
    self.__continue_verify = 0x00

    data_buf[0] = VERIFY & 0xFF
    data_buf[1] = (0x02 >> 8) & 0xFF
    data_buf[2] = (0x02 >> 0) & 0xFF
    data_buf[3] = self.__continue_verify & 0xFF
    data_buf[4] = timeout & 0xFF

    self.send_package(data_buf,5)
    recv_pack = struct_recv_pack()
    recv_pack = self.recv_package(timeout)#timeout

    return self.recognition_data_analysis(recv_pack)

  def recognition_data_analysis(self,recv_pack):
    '''!
      @brief Recognition data analysis
      @param recv_pack: The received package
      @return recognize the result
    '''
    recognition_data = struct_recognition_data()

    recognition_data.result = recv_pack.result
    recognition_data.nid = recv_pack.nid

    for i in range(0,8):
      recognition_data.face_data[i] = recv_pack.face_data[i]

    if recv_pack.result == 0x00:
      if recv_pack.mid == MID_SCAN_QR_CODE:
        recognition_data.type = self.TYPE_QR
        recognition_data.QR_date = recv_pack.data[0:recv_pack.data_len].decode('ascii').strip('\0')
      elif recv_pack.mid == VERIFY:
        recognition_data.uid = (recv_pack.data[0] << 8) | recv_pack.data[1]
        if recognition_data.uid <= 1000:
          recognition_data.type = self.TYPE_FACE
        else:
          recognition_data.type = self.TYPE_PALM
        recognition_data.user_name = recv_pack.data[2:34].decode('ascii').strip('\0')
        recognition_data.admin = recv_pack.data[34]
      else:
        recognition_data.type = self.TYPE_NULL
    else:
      recognition_data.type = self.TYPE_NULL

    return recognition_data

  def enable_face_frame(self):
    '''!
      @brief Enable face frame
      @return enable the face frame result
      @retval      True  enable the face frame success
      @retval      False  enable the face frame failure
    '''
    data_buf = [0x00]*20
    
    data_buf[0] = SET_FACE__LOCATION_DISPLAY
    data_buf[1] = (0x01 >> 8) & 0xFF
    data_buf[2] = (0x01 >> 0) & 0xFF
    data_buf[3] = 0x01

    self.send_package(data_buf,4)
    recv_pack = struct_recv_pack()
    recv_pack = self.recv_package()

    if recv_pack.result == 0x00:
      return True
    else:
      return False

  def get_all_user_ids(self):
    '''!
      @brief Get all user ID
      @return Get the result
      @n      result      Instruction execution result
      @retval  0x00:       Get all user ID success
      @retval  default:    Get all user ID failure
      @n      user_num:   The number of users
      @n      uids:       The user ID list
    '''
    self.drv_reset()
    all_data = struct_All_User_ID()
    data_buf = [0x00]*20

    data_buf[0] = MID_GET_ALL_USERID & 0xFF
    data_buf[1] = (0x01 >> 8) & 0xFF
    data_buf[2] = (0x01 >> 0) & 0xFF
    data_buf[3] = 0x00

    recv_pack = struct_recv_pack()
    self.send_package(data_buf,4)
    recv_pack = self.recv_package()

    all_data.result = recv_pack.result

    if recv_pack.result == 0x00:
      all_data.user_num = recv_pack.data[0]
      for i in range(0,all_data.user_num):
        all_data.uids[i] = recv_pack.data[1+i*2]<<8 | recv_pack.data[2+i*2]
    else:
      all_data.user_num = 0
    
    return all_data


  def get_user_info(self,uid):
    '''!
      @brief Get user information
      @param uid: The user ID
      @return Get the result
      @n      result      Instruction execution result
      @retval  0x00:       Get user information success
      @retval  default:    Get user information failure
      @n      uid:        user ID
      @n      user_name   user name 
      @n      admin:      User enrollment permissions
      @retval  NORMAL:     Normal user
      @retval  ADMIN:      Admin user
      @n      type:       User enrollment type
      @retval  TYPE_NULL:  Undefine
      @retval  TYPE_FACE:  Face enrollment
      @retval  TYPE_PALM:  Palm enrollment
    '''
    self.drv_reset()
    data_buf = [0x00]*20

    data_buf[0] = GET_USER_INFO & 0xFF
    data_buf[1] = (0x02 >> 8) & 0xFF
    data_buf[2] = (0x02 >> 0) & 0xFF
    data_buf[3] = (uid >> 8) & 0xFF
    data_buf[4] = (uid >> 0) & 0xFF

    self.send_package(data_buf,5)
    recv_pack = struct_recv_pack()
    recv_pack = self.recv_package()

    user_info = struct_user_info()
    if(recv_pack.result == 0x00):
      
      user_info.uid = recv_pack.data[0]<<8 | recv_pack.data[1]
      user_info.user_name = recv_pack.data[2:34].decode('ascii').strip('\0')
      user_info.admin = recv_pack.data[34]
      if uid > 1000:
        user_info.type = self.TYPE_PALM
      else:
        user_info.type = self.TYPE_FACE
    else:
      user_info.uid = 0
      user_info.user_name = ""
    return user_info

  def delete_user(self,uid):
    '''!
      @brief Delete user
      @param uid: The user ID
      @return delete the user result
      @retval  True: delete the user success
      @retval  False: delete the user failure
    '''
    self.drv_reset()
    data_buf = [0x00]*20

    data_buf[0] = DEL_USER & 0xFF
    data_buf[1] = (0x02 >> 8) & 0xFF
    data_buf[2] = (0x02 >> 0) & 0xFF
    data_buf[3] = (uid >> 8) & 0xFF
    data_buf[4] = (uid >> 0) & 0xFF

    self.send_package(data_buf,5)
    recv_pack = struct_recv_pack()
    recv_pack = self.recv_package()

    if(recv_pack.result == 0x00):
      return True
    else:
      return False

  def delete_all_user(self):
    '''!
      @brief Delete all user
      @return delete all user result
      @retval  True: delete the user success
      @retval  False: delete the user failure
    '''
    self.drv_reset()
    data_buf = [0x00]*20

    data_buf[0] = DEL_ALL_USER & 0xFF
    data_buf[1] = (0x00 >> 8) & 0xFF
    data_buf[2] = (0x00 >> 0) & 0xFF

    self.send_package(data_buf,3)
    recv_pack = struct_recv_pack()
    recv_pack = self.recv_package()

    if(recv_pack.result == 0x00):
      return True
    else:
      return False

  def enroll_user(self,admin,user_name,timeout):
    '''!
      @brief Enroll user
      @param admin: The user is an administrator or not
      @retval NORMAL:     Normal user
      @retval ADMIN:      Admin user
      @param user_name: The user name
      @param timeout: Timeout time, measured in seconds(3-20s)
      @return enroll the user result
      @n      result      Instruction execution result
      @retval  0x00:       Enroll user success
      @retval  default:    Enroll user failure
      @n      uid:        user ID
      @n      user_name   user name 
      @n      admin:      User enrollment permissions
      @retval  NORMAL:     Normal user
      @retval  ADMIN:      Admin user
      @n      type:       User enrollment type
      @retval  TYPE_NULL:  Undefine
      @retval  TYPE_FACE:  Face enrollment
      @retval  TYPE_PALM:  Palm enrollment
      @n      result      Instruction execution result
      @retval  Success:       Enroll user success
      @retval  FailedFaceEnrolled:  Failed to enroll user due to face recognition failure
      @retval  default:    Enroll user failure
    '''
    enroll_data = struct_enroll_result_data()
    enroll_data = self.signed_account(ENROLL_SINGLE,admin,user_name,FACE_DIRECTION_UNDEFINE,timeout)

    user_info = struct_user_info()
    if(enroll_data.result == self.Success):
      user_info.uid = enroll_data.uid
      user_info.user_name = user_name[0:20]
      user_info.admin = admin
      user_info.type = enroll_data.type
      user_info.result = self.Success
    elif(enroll_data.result == self.FailedFaceEnrolled):
      user_info.uid = 0
      user_info.result = self.FailedFaceEnrolled
    else:
      user_info.uid = 0
      user_info.result = enroll_data.result


    return user_info

  def signed_account(self, cmd, admin,user_name,face_dir,timeout):
    '''!
      @brief Signed account
      @param cmd: The command
      @param admin: The user is an administrator or not
      @param user_name: The user name
      @param face_dir: The face direction
      @param timeout: Timeout time, measured in seconds
      @return enroll the user result
    '''
    self.drv_reset()
    data_buf = [0x00]*50
    data_indux = 0

    data_buf[data_indux] = cmd & 0xFF
    data_indux += 1
    pack_size = 35
    data_buf[data_indux] = pack_size >> 8 & 0xFF
    data_indux += 1
    data_buf[data_indux] = (pack_size) & 0xFF
    data_indux += 1
    data_buf[data_indux] = admin & 0xFF
    data_indux += 1
    for i in range(0,32):
      if i < len(user_name):
        data_buf[data_indux] = ord(user_name[i])
      else:
        data_buf[data_indux] = 0x00
      data_indux +=1
    data_buf[data_indux] = face_dir & 0xFF
    data_indux += 1
    data_buf[data_indux] = timeout & 0xFF
    data_indux += 1

    self.send_package(data_buf,data_indux)

    recv_pack = struct_recv_pack()
    recv_pack = self.recv_package(timeout)

    enroll_data =  struct_enroll_result_data()
    enroll_data.result = recv_pack.result
    if recv_pack.result == 0x00:
      enroll_data.uid = recv_pack.data[0]<<8 | recv_pack.data[1]

      if(recv_pack.face_data[0] == 128):
        enroll_data.type = self.TYPE_PALM
      else:
        enroll_data.type = self.TYPE_FACE

      enroll_data.nid = recv_pack.nid
      for i in range(0,8):
        enroll_data.face_data[i] = recv_pack.face_data[i]

    else:
      enroll_data.uid = 0
      enroll_data.type = self.TYPE_NULL
      
    return enroll_data

  def drv_reset(self):
    data_buf = [0x00]*10

    data_buf[0] = RESET & 0xFF
    data_buf[1] = (0x00 >> 8) & 0xFF
    data_buf[2] = (0x00 >> 0) & 0xFF

    self.send_package(data_buf,3)
    recv_pack = struct_recv_pack()
    recv_pack = self.recv_package()

    if recv_pack.mid == RESET:
      return True
    else:
      return False

  def xor_check_sum(self,data,len):
    parityCheck = 0x00
    for i in range(0,len):
        parityCheck ^= data[i]
    return parityCheck
  
  def xor_check(self,data,length):
    parityCheck = 0
    if(len(data)) < length + 1:
      return False

    for i in range(0,length):
      parityCheck ^= data[i]
    if(parityCheck == data[length]):
      return True
    else:
      return False

  def recv_package(self,timeout = CMD_TIME_OUT):

    recv_pack = struct_recv_pack()
    recv_len = 0x00

    now_time = time.time()
    while((time.time() - now_time) < timeout + 0.5):
      data_buffer = [0x00] * 256
      data_buffer = self.read_reg(0,2)

      if (data_buffer[0] == SYNCWORD_H and data_buffer[1] == SYNCWORD_L) and len(data_buffer)  == 2:
        data_buffer = self.read_reg(0,3)
        msg_id = data_buffer[0]
        recv_len = (data_buffer[1]<<8) | data_buffer[2]
        recv_pack.data_len = recv_len - 2
        data_buffer += bytearray(self.read_reg(0,recv_len + 1))
        if(self.xor_check(data_buffer,recv_len + 3) == True):
          if(msg_id == MID_RELAY):
            if(len(data_buffer) >= 5):
              recv_pack.mid  = data_buffer[3]
              recv_pack.result     = data_buffer[4]
              recv_pack.data    = data_buffer[5:len(data_buffer)]
            else:
              recv_pack.result = 0x05
            return recv_pack

          elif(msg_id == MID_NOTE):
            if(recv_len == 0x11):
              recv_pack.nid = data_buffer[3]
              for i in range(0,8):
                recv_pack.face_data[i] = (data_buffer[4 + i * 2]) | (data_buffer[5+i * 2]<<8)

          else:
            recv_pack.result = 0x05
            return recv_pack
        else:
          continue
      else:
        continue
    recv_pack.result = 0x0D
    return recv_pack

  def send_package(self, data,len):
    syncword_data = [SYNCWORD_H,SYNCWORD_L]
    parityCheck = [0x00]*2
    parityCheck[0] = self.xor_check_sum(data,len)

    self.wrirte_reg(0,syncword_data,2)
    self.wrirte_reg(0,data,len)
    self.wrirte_reg(0,parityCheck,1)

class DFRobot_AI10_UART(DFRobot_AI10):
  def __init__(self, baud):
    #self.__baud = baud
    super(DFRobot_AI10_UART, self).__init__(baud)

  def wrirte_reg(self, reg ,data,length):
    send = bytes(data[:length])
    self.ser.flushInput()
    try:
      self.ser.write(send)
      return
    except:
      print("please check connect or mode!")
    return
  
  def read_reg(self, reg, len):
    recv = [0x00]*len
    timenow = time.time()
    while ((time.time() - timenow)  <= 0.1):
      count = self.ser.inWaiting()
      if count != 0:
        recv = self.ser.read(len)
        return recv
    return recv
/*!
 * @file DFRobot_AI10.cpp
 * @brief The implementation of the DFRobot_AI10 and DFRobot_AI10_UART class
 * @copyright	Copyright (c) 2025 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license The MIT License (MIT)
 * @author [jiali](zhixinliu@dfrobot.com)
 * @version V1.0
 * @date 2025-07-15
 * @url https://github.com/DFRobot/DFRobot_AI10
 */
#include "DFRobot_AI10.h"

DFRobot_AI10::DFRobot_AI10(){}
DFRobot_AI10::~DFRobot_AI10(){}

sUserData_t DFRobot_AI10::enrollUser(uint8_t admin, const char* userName, uint8_t timeout)
{
  sUserData_t uData;
  if(userName == NULL){
    uData.UID = 0;
    return uData;
  }
  sEnrollResultData_t enrollResultData = signedAccount(ENROLL_SINGLE,admin,userName,FACE_DIRECTION_UNDEFINE,timeout);
  if(enrollResultData.result == eSuccess){
    uData.UID = enrollResultData.UID;
    strncpy(uData.userName, userName, 20);
    uData.userName[20] = '\0';
    uData.admin = admin;
    if(uData.UID > 1000){
      uData.type = ePalm;
    }else{
      uData.type = eFace;
    }
    uData.result = eSuccess;
  }else if(enrollResultData.result == eFailedFaceEnrolled){
    uData.UID = 0;
    uData.result = eFailedFaceEnrolled;
  }else{
    uData.UID = 0;
    uData.result = enrollResultData.result;
  }
  return uData;
}

sEnrollResultData_t DFRobot_AI10::signedAccount(uint8_t CMD, uint8_t admin, const char* userName, uint8_t faceDir, uint8_t timeout)
{
  drvReset();
  sEnrollData_t enrollData;
  sEnrollResultData_t enrollResultData;

  uint8_t dataIndex = 0;
  uint8_t data[50];

  enrollData.admin = admin;
  strncpy((char*)enrollData.userName, userName, 20);
  enrollData.faceDir = faceDir;
  enrollData.timeout = timeout;
  data[dataIndex++] = CMD;
  uint16_t date_size= sizeof(enrollData);
  data[dataIndex++] = (date_size >> 8) & 0xFF;
  data[dataIndex++] = (date_size >> 0) & 0xFF;
  memcpy(data+dataIndex, &enrollData, date_size);
  dataIndex += date_size;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack = recvPackage(timeout);

    if(rPack.replyData.result == eSuccess){
      enrollResultData.UID = (rPack.replyData.data[0] << 8) | rPack.replyData.data[1];
      enrollResultData.result = rPack.replyData.result;
      memcpy(&enrollResultData.noteData, &rPack.noteData, sizeof(sNoteData_t));

      if(enrollResultData.noteData.state == 0x80){
        enrollResultData.type = ePalm;
      }else if(enrollResultData.noteData.state == 0x00){
        enrollResultData.type = eFace;
      }
    }else{
      enrollResultData.result = rPack.replyData.result;
    }

    return enrollResultData;
}

sAllUserID_t DFRobot_AI10::getAllUserIDs(void)
{
  drvReset();
  uint8_t data[20];
  uint16_t dataIndex = 0;
  uint8_t i = 0;

  sAllUserID_t uDatas;

  data[dataIndex++] = MID_GET_ALL_USERID;
  data[dataIndex++] = (0x01 >> 8) & 0xFF;
  data[dataIndex++] = (0x01 >> 0) & 0xFF;
  data[dataIndex++] = 0x00;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack = recvPackage();

  uDatas.result = rPack.replyData.result;
  if(rPack.replyData.result == eSuccess){
    uDatas.userNum = rPack.replyData.data[0];
    for(i = 0; i < uDatas.userNum; i++){
      uDatas.UIDS[i] = (rPack.replyData.data[1 + i*2] << 8) | rPack.replyData.data[2 + i*2];
    }
  }else{
    uDatas.userNum = 0x00;
  }
  return uDatas;
}

bool DFRobot_AI10::deleteAllUser(void)
{
  drvReset();
  uint8_t data[20];
  uint16_t dataIndex = 0;

  data[dataIndex++] = DEL_ALL_USER;
  data[dataIndex++] = (0x00 >> 8) & 0xFF;
  data[dataIndex++] = (0x00 >> 0) & 0xFF;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack= recvPackage();

  if(rPack.replyData.result == eSuccess){
    return true;
  }else{
    return false;
  }
}

sUserData_t DFRobot_AI10::getUserInfo(uint16_t UID)
{
  drvReset();
  uint8_t data[20];
  uint16_t dataIndex = 0;
    
  data[dataIndex++] = GET_USER_INFO;
  data[dataIndex++] = (0x02 >> 8) & 0xFF;
  data[dataIndex++] = (0x02 >> 0) & 0xFF;
  data[dataIndex++] = (UID >> 8) & 0xFF;
  data[dataIndex++] = (UID >> 0) & 0xFF;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack= recvPackage();
  sUserData_t uData;
  if(rPack.replyData.result == eSuccess){
    uData.UID = (rPack.replyData.data[0] << 8) | rPack.replyData.data[1];
    memcpy((uint8_t*)uData.userName, &rPack.replyData.data[2], 32);
    uData.admin = rPack.replyData.data[34];
  }else{
    uData.UID = 0x00;
  }

  return uData;
}

bool DFRobot_AI10::deleteUser(uint16_t UID)
{
  drvReset();
  uint8_t data[20];
  uint16_t dataIndex = 0;

  data[dataIndex++] = DEL_USER;
  data[dataIndex++] = (0x02 >> 8) & 0xFF;
  data[dataIndex++] = (0x02 >> 0) & 0xFF;
  data[dataIndex++] = (UID >> 8) & 0xFF;
  data[dataIndex++] = (UID >> 0) & 0xFF;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack= recvPackage();

  if(rPack.replyData.result == eSuccess){
    return true;
  }else{
    return false;
  }
}

sRecognitionData_t DFRobot_AI10::getRecognitionResult(uint8_t timeout)
{
  uint8_t data[20];
  uint16_t dataIndex = 0;
  continueVerify = 0x00;

  data[dataIndex++] = VERIFY;
  data[dataIndex++] = (0x02 >> 8) & 0xFF;
  data[dataIndex++] = (0x02 >> 0) & 0xFF;
  data[dataIndex++] = continueVerify;
  data[dataIndex++] = timeout;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack= recvPackage(timeout);

  return recognitionDataAnalysis(rPack);
}

sRecognitionData_t DFRobot_AI10::startContinuousFaceRecognition(uint8_t timeout)
{
  uint8_t data[256];
  uint16_t dataIndex = 0;
  continueVerify = 0x01;

  data[dataIndex++] = VERIFY;
  data[dataIndex++] = (0x02 >> 8) & 0xFF;
  data[dataIndex++] = (0x02 >> 0) & 0xFF;
  data[dataIndex++] = continueVerify;
  data[dataIndex++] = timeout;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack= recvPackage(timeout);

  return recognitionDataAnalysis(rPack);
}

sRecognitionData_t DFRobot_AI10::recognitionDataAnalysis(sRecvPack_t rPack)
{
  sRecognitionData_t recData;

  recData.result = rPack.replyData.result;
  memcpy(&recData.noteData, &rPack.noteData, sizeof(sNoteData_t));
  if(rPack.replyData.result == eSuccess){
    if(rPack.replyData.mid == MID_SCAN_QR_CODE){
      recData.type = eQR;
      memcpy(recData.QRDdata, rPack.replyData.data, 256);
    }else if(rPack.replyData.mid == VERIFY){
      recData.userData.UID = (rPack.replyData.data[0] << 8) | rPack.replyData.data[1];
      if(recData.userData.UID <= 1000){
        recData.type = eFace;
      }
      else{
        recData.type = ePalm;
      }
      memcpy((uint8_t*)recData.userData.userName, &rPack.replyData.data[2], 32);
      recData.userData.admin = rPack.replyData.data[34];
    }else{
      recData.type = eNull;
    }

  }else{
    recData.type = eNull;
  }
  return recData;
}

bool DFRobot_AI10::enableFaceFrame(void)
{
  uint8_t data[20];
  uint16_t dataIndex = 0;
  
  data[dataIndex++] = SET_FACE__LOCATION_DISPLAY;
  data[dataIndex++] = (0x01 >> 8) & 0xFF;
  data[dataIndex++] = (0x01 >> 0) & 0xFF;
  data[dataIndex++] = 0x01;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack= recvPackage();

  if(rPack.replyData.result == eSuccess){
    return true;
  }else{
    return false;
  }
}

void DFRobot_AI10::sendPackage(uint8_t *data, uint8_t len)
{
  uint8_t SyncWord_data[2] = {SyncWord_H,SyncWord_L};
  uint8_t ParityCheck = XORCheckSum(data, len);

  writeReg(0,SyncWord_data, 2);
  writeReg(0,data, len);
  writeReg(0,&ParityCheck, 1);
}

sRecvPack_t DFRobot_AI10::recvPackage(uint8_t timeout)
{
  sRecvPack_t recvData;
  memset(&recvData, 0, sizeof(recvData));
  uint8_t data[256];
  uint16_t timeOut = timeout*1000;

  uint16_t recvLen = 0;
  uint32_t nowtime = millis();

  while(millis() - nowtime < timeOut + 500){
    recvLen = readReg(0,data, 2);

    if(recvLen > 0 && ((data[0] == SyncWord_H) && (data[1] == SyncWord_L))){
        recvLen = readReg(0,data, 3);
        uint8_t msg_id = data[0];
        recvLen = (data[1]<<8) | data[2];
        recvLen = readReg(0,&data[3], recvLen + 1) + 3;
        if(XORCheck(data, recvLen)){
          if(msg_id == MID_RELAY){
            memcpy(&recvData.replyData,&data[3],recvLen-1-3);
            return recvData;
          }else if(msg_id == MID_NOTE){
            memcpy(&recvData.noteData,&data[3],recvLen-1-3);
          }else{
            recvData.replyData.result = eFailedUnknow;
            return recvData;
          }
        }else{
          continue;
        }
      }else{
        continue;
      }
  }
  recvData.replyData.result = eFailedTimeout;
  return recvData;
}

uint8_t DFRobot_AI10::XORCheckSum(uint8_t *dat, uint8_t len)
{
  uint8_t ParityCheck = 0;
  for(uint8_t i = 0; i < len ;i++){
    ParityCheck ^= dat[i];
  }
  return ParityCheck;
}
bool DFRobot_AI10::drvReset(void)
{
  uint8_t data[10];
  uint16_t dataIndex = 0;

  data[dataIndex++] = RESET;
  data[dataIndex++] = (0x00 >> 8) & 0xFF;
  data[dataIndex++] = (0x00 >> 0) & 0xFF;

  sendPackage(data, dataIndex);
  sRecvPack_t rPack= recvPackage();
  if(rPack.replyData.mid == RESET){
    return true;
  }
  else{
    return false;
  }
}

bool DFRobot_AI10::XORCheck(uint8_t *data, uint8_t len)
{
  uint8_t ParityCheck = 0;
  for(uint8_t i = 0; i < len - 1;i++){
    ParityCheck ^= data[i];
  }
  if (ParityCheck == data[len - 1]){
    return true;
  }else{
    return false;
  }
}

#if defined(ARDUINO_AVR_UNO) || defined(ESP8266)
DFRobot_AI10_UART::DFRobot_AI10_UART(SoftwareSerial* sSerial,uint32_t Baud)
{
  this->_serial = sSerial;
  this->_baud = Baud;
}
#else
DFRobot_AI10_UART::DFRobot_AI10_UART(HardwareSerial* hSerial,uint32_t Baud,uint8_t rxpin ,uint8_t txpin )
{
  this->_serial = hSerial;
  this->_baud = Baud;
  this->_rxpin = rxpin;
  this->_txpin = txpin;
}
#endif

bool DFRobot_AI10_UART::begin(void)
{
  #ifdef ESP32
    _serial->begin(this->_baud, SERIAL_8N1, _txpin, _rxpin);
  #elif defined(ARDUINO_AVR_UNO) || defined(ESP8266)
    _serial->begin(this->_baud);
    delay(50);
  #else
    _serial->begin(this->_baud);
  #endif
  return drvReset();
}

void DFRobot_AI10_UART::writeReg(uint8_t reg,uint8_t *data, uint8_t len)
{
  _serial->write(data, len);
  len = reg;
}

int16_t DFRobot_AI10_UART::readReg(uint8_t reg,uint8_t *data, uint8_t len)
{
  uint16_t i = 0;
  uint32_t nowtime = millis();
  while(millis() - nowtime < TIME_OUT){
    while(_serial->available() > 0){
      if(i == len) return len;
      data[i++] = _serial->read();
    }
  }
  len = reg;
  return i;
}

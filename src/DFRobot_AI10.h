/*!
 * @file DFRobot_AI10.h
 * @brief Define the basic structure of the DFRobot_AI10 class, the implementation of the basic methods
 * @copyright	Copyright (c) 2025 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license The MIT License (MIT)
 * @author [jiali](zhixinliu@dfrobot.com)
 * @version V1.0
 * @date 2025-07-15
 * @url https://github.com/DFRobot/DFRobot_AI10
 */
#ifndef __DFROBOT_AI10_H__
#define __DFROBOT_AI10_H__

#include <Arduino.h>
#if defined(ARDUINO_AVR_UNO) || defined(ESP8266)
#include "SoftwareSerial.h"
#else
#include "HardwareSerial.h"
#endif

/**
 * @struct sEnrollData_t
 * @brief Structure to hold enrollment data for user registration
 */
typedef struct {
  uint8_t admin; 
  uint8_t userName[32];
  uint8_t faceDir; 
  uint8_t timeout;
}sEnrollData_t;

/**
 * @struct sNoteData_t
 * @brief  receive note data
 */
typedef struct {
  uint8_t nid; 
  int16_t state;
  int16_t left;
  int16_t top;
  int16_t Right;
  int16_t bottom;
  int16_t yaw;
  int16_t pitch;
  int16_t roll;
}sNoteData_t;

/**
 * @struct sEnrollResultData_t
 * @brief The result of user enrollment
 */
typedef struct {
  uint8_t result; 
  uint16_t UID;
  uint8_t type;
  sNoteData_t noteData;
}sEnrollResultData_t;

/**
 * @struct sReplyData_t
 * @brief Receive reply data
 */
typedef struct {
  uint8_t mid; 
  uint8_t result; 
  uint8_t data[256];
}sReplyData_t;

/**
 * @struct sRecvPack_t
 * @brief received package data
 */
typedef struct {
  sReplyData_t replyData;
  sNoteData_t noteData;
}sRecvPack_t;

/**
 * @struct sAllUserID_t
 * @brief All user and all ID
 */
typedef struct {
  uint8_t result; 
  uint8_t userNum;
  uint16_t UIDS[100];
}sAllUserID_t;

/**
 * @struct sUserData_t
 * @brief User data
*/
typedef struct {
  uint16_t UID;
  char userName[32]; 
  uint8_t admin;
  uint8_t type;
  uint8_t result;
}sUserData_t;

/**
 * @struct sRecognitionData_t
 * @brief Recognition data
*/
typedef struct {
  uint8_t result;
  sUserData_t userData;
  sNoteData_t noteData;
  char QRDdata[256];
  uint8_t type;
}sRecognitionData_t;

/**
 * @enum eResult_t
 * @brief Result codes 
*/
typedef enum{
  eSuccess = 0,
  eRejected = 1,
  eAborted = 2,
  eFailedCamera = 4,
  eFailedUnknow = 5,
  eFailedInvalidParam = 6,
  eFailedNoMemory = 7,
  eFailedUnknowUser = 8,
  eFailedMaxUser = 9,
  eFailedFaceEnrolled = 10,
  eFailedLiveCheck = 12,
  eFailedTimeout = 13,
  eFailedDetectQR = 26,
}eResult_t;

/**
 * @enum eType_t
 * @brief Type parameters
*/
typedef enum{
  eNull = 0,
  eFace,
  ePalm,
  eQR,
}eType_t;

/**
 * @enum eAdmin_t
 * @brief Admin parameters
*/
typedef enum{
  eNormal, /**< Normal permission */
  eAdmin, /**< Admin permission */
}eAdmin_t;

class DFRobot_AI10{
public:

#define TIME_OUT                        0x64             ///< time out
#define CMD_TIME_OUT                    0x03             ///< command time out
#define SyncWord_H                      0xEF
#define SyncWord_L                      0xAA
#define MID_RELAY                       0x00
#define MID_NOTE                        0x01

#define RESET                           0x10
#define ENROLL_SINGLE                   0x1D
#define MID_GET_ALL_USERID              0x24
#define GET_USER_INFO                   0x22
#define DEL_USER                        0x20
#define DEL_ALL_USER                    0x21
#define SET_FACE__LOCATION_DISPLAY      0xB5
#define VERIFY                          0x12
#define MID_SCAN_QR_CODE                0x70

#define FACE_DIRECTION_UP               0x10
#define FACE_DIRECTION_DOWN             0x08
#define FACE_DIRECTION_LEFT             0x04
#define FACE_DIRECTION_RIGHT            0x02
#define FACE_DIRECTION_MIDDLE           0x01
#define FACE_DIRECTION_UNDEFINE         0x00

  DFRobot_AI10();
  ~DFRobot_AI10();

  /**
   * @fn enrollUser
   * @brief Enroll a user with face or palm information
   * @param admin  
   * @n     eNormal     Normal permission
   * @n     eAdmin:     Admin permission
   * @param userName  Enroll user name
   * @param timeout  timeout
   * @return sUserData_t
   * @n      UID                    The user ID
   * @n      userName               The user name
   * @n      admin                  The user's authority
   * @n      type                   The type of enrollment
   * @n         eNull                   Null
   * @n         eFace                   Face
   * @n         ePalm                   Palm
   * @n      result                 Registration result
   * @n         eSuccess                Success
   * @n         eFailedFaceEnrolled     Failed to enroll, the face has been enrolled
   * @n         eFailedInvalidParam     Invalid parameter
   * @n         eFailedMaxUser          Maximum number of users reached
   * @n         eFailedCamera           Failed to capture the face
   * @n         eFailedTimeout          Time out
  */
  sUserData_t enrollUser(uint8_t admin,const char* userName, uint8_t timeout);

  /**
   * @fn signedAccount
   * @brief get the information of all users
   * @return sUserData_t
   * @n       result                 Get the result
   * @n           0                      Success
   * @n           default                Failed
   * @n       userNum                The Number of users
   * @n       UIDS                   All user ids
  */
  sAllUserID_t getAllUserIDs(void);

  /**
   * @fn enableFaceFrame
   * @brief Open the face frame
   * @return true or false
  */
  bool enableFaceFrame(void);

  /**
   * @fn getRecognitionResult
   * @brief Get the recognition result
   * @param timeout 
   * @return sRecognitionData_t
   * @n       result                  he result of recognition
   * @n       userData                The user information
   * @n       noteData                The note information
   * @n       QRDdata                 The QR code information
   * @n       type                    The type of recognition
   * @n           eNull                   Null
   * @n           eFace                   Face
   * @n           ePalm                   Palm
   * @n           eQR                     QR code
  */
  sRecognitionData_t getRecognitionResult(uint8_t timeout);

  /**
   * @fn startContinuousFaceRecognition
   * @brief Start continuous face recognition
   * @param timeout 
   * @return sRecognitionData_t
   * @n       result                  The result of recognition
   * @n       userData                The user information
   * @n       noteData                The note information
   * @n       QRDdata                 The QR code information
   * @n       type                    The type of recognition
   * @n           eNull                   Null
   * @n           eFace                   Face
   * @n           ePalm                   Palm
   * @n           eQR                     QR code
  */
  sRecognitionData_t startContinuousFaceRecognition(uint8_t timeout);

  /** 
   * @fn deleteUser
   * @brief Delete a user by UID
   * @param UID 
   * @return true or false
  */
  bool deleteUser(uint16_t UID);

  /**
   * @fn deleteAllUser
   * @brief Delete all users
   * @return true or false
  */
  bool deleteAllUser(void);


protected:
  uint8_t XORCheckSum(uint8_t *data, uint8_t len);
  bool XORCheck(uint8_t *data, uint8_t len);
  sEnrollResultData_t signedAccount(uint8_t CMD, uint8_t admin,const char* userName, uint8_t faceDir, uint8_t timeout);
  sUserData_t getUserInfo(uint16_t UID);
  void sendPackage(uint8_t *data, uint8_t len);
  sRecvPack_t recvPackage(uint8_t timeout = CMD_TIME_OUT);
  sRecognitionData_t recognitionDataAnalysis(sRecvPack_t rPack);
  bool drvReset(void);

private:
  virtual void writeReg(uint8_t reg,uint8_t *data, uint8_t len) = 0;
  virtual int16_t readReg(uint8_t reg,uint8_t *data, uint8_t len) = 0;
  uint8_t continueVerify = 0;
};

class DFRobot_AI10_UART: public DFRobot_AI10{
public:
  #if defined(ARDUINO_AVR_UNO) || defined(ESP8266)
  DFRobot_AI10_UART(SoftwareSerial *sSerial, uint32_t Baud);
  #else
  DFRobot_AI10_UART(HardwareSerial* hSerial,uint32_t Baud,uint8_t rxpin = 0,uint8_t txpin = 0);
  #endif
  bool begin(void);

protected:

  virtual void writeReg(uint8_t reg,uint8_t *data, uint8_t len);
  virtual int16_t readReg(uint8_t reg,uint8_t *data, uint8_t len);

private:
#if defined(ARDUINO_AVR_UNO) || defined(ESP8266)
  SoftwareSerial *_serial;
#else
  HardwareSerial *_serial;
#endif
  uint32_t _baud;
  uint8_t _rxpin = 0;
  uint8_t _txpin = 0;
};

#endif
# DFRobot_AI10
- [中文版](./README_CN.md)

This is a high-precision AI visual recognition module, featuring dual 2-megapixel cameras in combination with advanced deep learning algorithms. It is capable of accurately identifying both moving and static targets. Compared with traditional visual sensors, its anti-interference ability has been significantly enhanced and it is not affected by factors such as changes in environmental light, temperature fluctuations or complex backgrounds. Whether it is a fast-moving human body, a static human face or subtle palm vein features, the module can achieve rapid and stable detection and recognition.

![正反面](resources/images/FacePlamQR.jpg) 


## Product Link()

    SKU：SEN0677

## Table of Contents

* [Summary](#Summary)
* [Installation](#Installation)
* [Methods](#Methods)
* [Compatibility](#Compatibility)
* [History](#History)
* [Credits](#Credits)

## Summary

Provides an Arduino library that has the following features:
  Recognize human faces or palm prints
  Obtain the QR code information

## Installation
There are two methods for using this library:<br>
1. Open Arduino IDE, search for "DFRobot_AI10" on the status bar in Tools ->Manager Libraries and install the library.<br>
2. Download the library file before use, paste it into \Arduino\libraries directory, then open the examples folder and run the demo in the folder.<br>

## Methods

```C++
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
  recognitionData_t getRecognitionResult(uint8_t timeout);

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
  recognitionData_t startContinuousFaceRecognition(uint8_t timeout);

  /** 
   * @fn deleteUser
   * @brief Delete a user by UID
   * @param UID 
   * @return bool
   * @n       true     Success
   * @n       false    Failed
  */
  bool deleteUser(uint16_t UID);

  /**
   * @fn deleteAllUser
   * @brief Delete all users
   * @return bool
   * @n       true     Success
   * @n       false    Failed
  */
  bool deleteAllUser(void);
```

## Compatibility

MCU                | Work Well    |   Work Wrong    | Untested    | Remarks
------------------ | :----------: | :-------------: | :---------: | :----:
Arduino Uno        |      √       |                 |             |
Arduino MEGA2560   |      √       |                 |             |
Arduino Leonardo   |      √       |                 |             |
FireBeetle-ESP8266 |      √       |                 |             |
FireBeetle-ESP32   |      √       |                 |             |
FireBeetle-M0      |      √       |                 |             |
Micro:bit          |             | nonsupport uart |             |

## History
- 2025/07/18 - Version 1.0.0 released.

## Credits

Written by jiali(zhixinliu@dfrobot.com), 2025. (Welcome to our [website](https://www.dfrobot.com/))
# DFRobot_C4001
- [English Version](./README.md)

这是一款高精度AI视觉识别模组，采用双200万像素摄像头配合先进的深度学习算法，具有动静目标均可精准识别的特点。相比传统视觉传感器，其抗干扰能力显著提升，不受环境光照变化、温度波动或复杂背景等因素影响。无论是快速移动的人体、静态人脸还是细微的掌静脉特征，模组都能实现快速、稳定的检测识别。
以智能楼宇门禁系统为例，传统方案在逆光、暗光或人员密集场景下容易出现识别失败。而本AI视觉模组凭借强大的环境适应能力，可在各种复杂光照条件下准确识别人脸、掌纹等生物特征，同时支持多人同时检测。其毫秒级响应速度确保通行效率，内置的3D活体检测功能有效防范照片、视频等欺骗手段，为智能安防系统提供更可靠的身份认证解决方案。该模组还能实时统计人员进出数据，助力楼宇实现智能化管理和资源优化配置。

![效果图](../../resources/images/FacePlamQR.jpg)

## 产品链接()

    SKU：SEN0677

## 目录

* [概述](#概述)
* [库安装](#库安装)
* [方法](#方法)
* [兼容性](#兼容性)
* [历史](#历史)
* [创作者](#创作者)

## 概述

提供一个python库给模块，此库具有以下功能：
  识别 人脸或掌纹
  获取 二维码信息

## 库安装
1. 下载库至树莓派，要使用这个库，首先要将库下载到Raspberry Pi，命令下载方法如下:

```
sudo git clone https:
```

1. 打开并运行例程，要执行一个例程demo_x.py，请在命令行中输入python demo_x.py。例如，要执行 continuous_recognition.py例程，你需要输入:

```
python  continuous_recognition.py
或 
python2 continuous_recognition.py
或 
python3 continuous_recognition.py
```

## 方法

```python
 def begin(self):
  '''!
    @brief begin 
  '''

  def start_continuous_face_recognition(self,timeout):
    '''!
      @brief 开始连续人脸识别
      @param timeout: 超时时间 (3-20s)
      @return 识别结果
      @n      result        指令执行结果
      @retval  0x00:        识别成功
      @retval  default:     识别失败
      @n      type:         识别类型
      @retval  TYPE_NULL:   未定义
      @retval  TYPE_FACE:   人脸识别
      @retval  TYPE_PALM:   掌纹识别
      @retval  TYPE_QR:     二维码识别
      @n      uid:          用户ID
      @n      user_name     识别用户名称 
      @n      admin:        识别用户权限
      @retval  NORMAL:      普通用户
      @retval  ADMIN:       管理员用户
      @n      QR_date:      二维码数据
    '''

  def get_recognition_result(self,timeout):
    '''!
      @brief 启动识别一次
      @param timeout: 超时时间 (3-20s)
      @return 识别结果
      @n      result        指令执行结果
      @retval  0x00:        识别成功
      @retval  default:     识别失败
      @n      type:         识别类型
      @retval  TYPE_NULL:   未定义
      @retval  TYPE_FACE:   人脸识别
      @retval  TYPE_PALM:   掌纹识别
      @retval  TYPE_QR:     二维码识别
      @n      uid:          用户ID
      @n      user_name     识别用户名称 
      @n      admin:        识别用户权限
      @retval  NORMAL:      普通用户
      @retval  ADMIN:       管理员用户
      @n      QR_date:      二维码数据
    '''

  def enable_face_frame(self):
    '''!
      @brief 使能人脸框
      @return 使能人脸框结果
      @retval      True  使能人脸框成功
      @retval      False 使能人脸框失败
    '''
    
  def get_all_user_ids(self):
    '''!
      @brief 得到所有用户ID
      @return 得到结果
      @n      result       指令执行结果
      @retval  0x00:       得到所有用户ID成功
      @retval  default:    得到所有用户ID失败
      @n      user_num:    用户数量
      @n      uids:        用户ID列表
    '''



  def delete_user(self,uid):
    '''!
      @brief 删除指定用户
      @param uid: 用户ID
      @return 删除用户结果
      @retval  True:  删除用户成功
      @retval  False: 删除用户失败
    '''

  def delete_all_user(self):
    '''!
      @brief 删除所有用户
      @return 删除所有用户结果
      @retval  True:  删除所有用户成功
      @retval  False: 删除所有用户失败
    '''


      def enroll_user(self,admin,user_name,timeout):
    '''!
      @brief 登记用户
      @param admin: 这用户是否为管理员
      @retval NORMAL:     普通用户
      @retval ADMIN:      管理员用户
      @param user_name: 用户名
      @param timeout:     超时时间，单位为秒(3-20s)
      @return   登记用户结果
      @n      uid:                    用户ID
      @n      user_name               用户名 
      @n      admin:                  用户权限
      @retval  NORMAL:                普通用户
      @retval  ADMIN:                 管理员用户
      @n      type:                   用户登记类型
      @retval  TYPE_NULL:             未定义
      @retval  TYPE_FACE:             人脸登记
      @retval  TYPE_PALM:             掌纹登记
      @n      result                  指令执行结果
      @retval  Success:               登记成功
      @retval  FailedFaceEnrolled:    人脸已被登记
      @retval  default:               登记失败
    '''
```

## 兼容性

* RaspberryPi Version

| Board        | 正常运行  | 运行失败   | 未测试    | 备注
| ------------ | :-------: | :--------: | :------: | :-----: |
| RaspberryPi2 |           |            |    √     |         |
| RaspberryPi3 |           |            |    √     |         |
| RaspberryPi4 |     √     |            |          |         |

* Python版本

| Python  | 正常运行  | 运行失败   | 未测试    | 备注
| ------- | :-------: | :--------: | :------: | :-----: |
| Python2 |     √     |            |          |         |
| Python3 |     √     |            |          |         |


## 历史

- 2025/07/18 - V1.0.0 版本

## 创作者

Written by zhixinliu(zhixinliu@dfrobot.com), 2021. (Welcome to our [website](https://www.dfrobot.com/))
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 17:31:55 2021

@author: 李立宗  lilizong@gmail.com
微信公众号：计算机视觉之光（微信号cvlight）
计算机视觉40例——从入门到深度学习（python+OpenCV）（待定名称）
李立宗 著     电子工业出版社
"""


import numpy as np
import cv2
import dlib

def critical_detecting():
    # Step 1：载入模型（加载预测器）
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Step 2：摄像头初始化
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # dlib初始化
    detector = dlib.get_frontal_face_detector()

    # Step 4：获取每一张脸的关键点（实现检测），针对每一帧进行处理
    while True:
        # 捕获一帧
        ret, img = cap.read()
        # 没有捕获到帧，直接退出
        if ret is None:
            break
        # 可以将当前帧处理为灰度，方便后续计算
        # gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #  参数gray：当前的视频帧（或者图像），参数1：上采样人脸（将人脸放大）
        faces = detector(img, 1)
        # 针对捕获到的多个人脸进行逐个处理
        for face in faces:
            # 获取关键点
            shape = predictor(img, face)
            # 将关键点转换为坐标(x,y)的形式
            landmarks = np.matrix([[p.x, p.y] for p in shape.parts()])
            # Step 5：绘制每一张脸的关键点（绘制shape中的每个点）
            for idx, point in enumerate(landmarks):
                # 当前关键的坐标
                pos = (point[0, 0], point[0, 1])
                # 针对当前关键点，绘制一个实心圆
                cv2.circle(img, pos, 2, color=(0, 255, 0), thickness=-1)
                # 字体
                font = cv2.FONT_HERSHEY_SIMPLEX
                # 利用cv2.putText输出1-68,索引序号加1，显示时从1开始。
                cv2.putText(img, str(idx + 1), pos, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        # 显示当前帧，及捕获到的各个人脸框
        cv2.imshow("face", img)
        # 捕获按键
        key = cv2.waitKey(1)
        # 如果按下Ecs键，则退出（Esc的ASCII码为27）
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == 'main':
    critical_detecting()

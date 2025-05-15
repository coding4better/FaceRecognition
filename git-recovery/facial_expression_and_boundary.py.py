# 该文件实现了人脸表情识别和面部轮廓绘制的功能。
# 通过计算嘴部的宽高比和嘴与脸颊的宽度比判断表情，
# 并使用凸包和直线绘制面部各部分的轮廓。

# -*- coding: utf-8 -*-
from scipy.spatial import distance as dist
import numpy as np
import dlib
import cv2

def boundary_drawing():
    # 模型初始化
    shape_predictor= "shape_predictor_68_face_landmarks.dat" #dace_landmark
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)


    # ======================= 绘制边框自定义函数 ===================================
    # 自定义函数drawLine，将指定的点连接起来
    def drawLine(start,end):
        # 获取点集
        pts = shape[start:end]
        # 遍历点集，将各个点用直线连接起来
        for l in range(1, len(pts)):
            ptA = tuple(pts[l - 1])
            ptB = tuple(pts[l])
            cv2.line(img, ptA, ptB, (0, 255, 0), 2)
    # 自定义函数，将指定的点构成一个凸包、绘制其轮廓
    def drawConvexHull(start,end):
        # 注意，凸包用来绘制眼睛、嘴
        # 眼睛、嘴也可以用drawLine通过直线绘制
        # 但是，使用凸包绘制轮廓，更方便进行颜色填充等设置
        # 获取某个特定五官的点集
        Facial = shape[start:end]
        # 针对该五官构造凸包
        mouthHull = cv2.convexHull(Facial)
        # 把凸包轮廓绘制出来
        cv2.drawContours(img, [mouthHull], -1, (0, 255, 0), 2)


    # ============================= 表情识别自定义函数 =============================
    # 自定义函数，计算嘴的宽高比
    # Mouth Aspect Ratio,嘴宽高比。参数也可以直接使用landmarks，确定好关键点位置即可
    def MAR(mouth):
        A = dist.euclidean(mouth[3], mouth[9])   #欧氏距离，直接计算y轴差值也可以
        B = dist.euclidean(mouth[2], mouth[10])
        C = dist.euclidean(mouth[4], mouth[8])
        avg = (A+B+C)/3
        D = dist.euclidean(mouth[0], mouth[6])
        mar=avg/D
        return mar
    # 自定义函数，计算嘴宽度、脸颊宽度的比值
    # Mouth Jaw Ratio,嘴宽度/脸颊宽度（嘴/下巴)
    def MJR(shape):
        #嘴宽度，欧氏距离，也可以直接计算x轴差值
        mouthWidht = dist.euclidean(shape[48], shape[54])
        #下巴两侧宽度，根据实际情况选用不同的索引如：4和13等等
        jawWidth = dist.euclidean(shape[3], shape[13])
        return mouthWidht/jawWidth                          #比值

        # 自定义函数，绘制嘴轮廓
    def drawMouth(mouth):
        # 针对嘴型构造凸包
        mouthHull = cv2.convexHull(mouth)
        # 把嘴的凸包轮廓绘制出来，便于观察
        cv2.drawContours(img, [mouthHull], -1, (0, 255, 0), 1)
    # 摄像头初始化
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # dlib初始化
    detector = dlib.get_frontal_face_detector()
    # 针对每一帧进行处理
    while True:
        # 捕获一帧
        ret, img = cap.read()
        # 没有捕获到帧，直接退出
        if ret is None:
            break
        # 可以将当前帧处理为灰度，方便后续计算
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #  参数gray：当前的视频帧（或者图像），参数1：上采样人脸（将人脸放大）
        faces = detector(img, 1)
        # 针对捕获到的多个人脸进行逐个处理
        for face in faces:
            # 针对脸部的关键点进行处理，构成坐标(x,y)形式
            shape = np.matrix([[p.x, p.y] for p in predictor(gray, face).parts()])
            mouth = shape[48:61]
            # 计算嘴的宽高比、嘴/脸颊值
            mar = MAR(mouth)  # 计算嘴部的高宽比
            mjr = MJR(shape)  # 计算“嘴宽/脸颊宽”
            result = "normal"  # 默认是正常表情
            # 嘴的宽高比，嘴脸颊宽比值，每个人不一样，我用0.5.
            # 大家可以根据实际情况确定不同的值
            # print("mar",mar,"mjr",mjr)  #测试一下实际值，可以根据该值确定
            if mar > 0.55:
                result = "laugh"
            elif mjr > 0.45:  # 任意一个超过阈值（都是0.5）为微笑
                result = "smile"
            cv2.putText(img, result, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # 绘制嘴部轮廓
            drawMouth(mouth)
            # 实时观察mar值
            cv2.putText(img, "MAR: {}".format(mar), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # 实时观察mjr值
            cv2.putText(img, "MJR: {}".format(mjr), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # ============使用函数drawConexHull绘制嘴、眼睛=========================
            # 获取嘴部的关键点集（在整个脸部索引中，其索引范围为[48,60],不包含61）
            drawConvexHull(48, 59)
            # 嘴内部
            drawConvexHull(60, 68)
            # 左眼
            drawConvexHull(42, 48)
            # 右眼
            drawConvexHull(36, 42)
            # ============使用函数drawLine绘制脸颊、眉毛、鼻子=========================
            # 将shape转换为np.array
            shape = np.array(shape)
            # 绘制脸颊，把脸颊的各个关键点（索引0-16，不含17）用线条连接起来
            drawLine(0, 17)
            # 绘制左眉毛，通过将关键点连接实现（索引18-21）
            drawLine(17, 22)
            # 绘制右眉毛（索引23-26）
            drawLine(22, 27)
            # 鼻子（索引27-36）
            drawLine(27, 36)
        cv2.imshow("Frame", img)
        # 捕获按键
        key = cv2.waitKey(1)
        # 如果按下Ecs键，则退出（Esc的ASCII码为27）
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    boundary_drawing()
# # 读取图像
# image=cv2.imread("image.jpg")
# # 色彩空间转换彩色(BGR)-->灰度（Gray）
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # 获取人脸
# faces = detector(gray, 0)
# # 对检测到的rects，逐个遍历
# for face in faces:
#     # 针对脸部的关键点进行处理，构成坐标(x,y)形式
#     shape = np.matrix([[p.x, p.y] for p in predictor(gray, face).parts()])
#     # ============使用函数drawConexHull绘制嘴、眼睛=========================
#     #获取嘴部的关键点集（在整个脸部索引中，其索引范围为[48,60],不包含61）
#     drawConvexHull(48,59)
#     # 嘴内部
#     drawConvexHull(60,68)
#     # 左眼
#     drawConvexHull(42,48)
#     # 右眼
#     drawConvexHull(36,42)
#     # ============使用函数drawLine绘制脸颊、眉毛、鼻子=========================
#     # 将shape转换为np.array
#     shape=np.array(shape)
#     # 绘制脸颊，把脸颊的各个关键点（索引0-16，不含17）用线条连接起来
#     drawLine(0,17)
#     # 绘制左眉毛，通过将关键点连接实现（索引18-21）
#     drawLine(17,22)
#     # 绘制右眉毛（索引23-26）
#     drawLine(22,27)
#     # 鼻子（索引27-36）
#     drawLine(27,36)
# cv2.imshow("Frame", image)
# cv2.waitKey()
# cv2.destroyAllWindows()


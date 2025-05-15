# 该文件是一个基于PyQt5的人脸识别应用程序。
# 提供了用户界面，支持打开摄像头、开始识别和选择不同功能。

import sys,os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import cv2,numpy

import Face_recognition
import applying
import attrbution
import boundary_drawing
import critical_detecting
# import attrbution
# import boundary_drawing
# import face_changing
import fatigue_detecting
import smile_detecting
from FaceRecognition.src.detection import facial_expression_recognition

from mainwindow import Ui_Face_recognition

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
class MyMainClass(QtWidgets.QMainWindow, Ui_Face_recognition):

    showSignal_opencamera = pyqtSignal()
    showSignal_startdetect = pyqtSignal()
    showSignal_showFile = pyqtSignal()

    def __init__(self, parent=None):
        super(MyMainClass, self).__init__(parent)
        self.setupUi(self)
        self.camera.clicked.connect(self.opencamera)
        self.recognite.clicked.connect(self.startdetect)
        self.functions.currentTextChanged.connect(self._fuctions)

        self.timer_camera = QTimer(self)
        self.cap = cv2.VideoCapture(0)
        self.timer_camera.start(30)

    def OpenDir_Clicked(self):

        # 打开文件选取对话框
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开')
        self.filename = str(self.filename)

        if self.filename:
            self.capturedImg = cv2.imread(self.filename)
            # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
            self.captured = cv2.cvtColor(self.capturedImg, cv2.COLOR_BGR2RGB)

            rows, cols, channels = self.captured.shape
            bytesPerLine = channels * cols
            QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.label.setScaledContents(True)

    # def OpenFile_returned(self):

    def opencamera(self):
        self.timer_camera.timeout.connect(self.show_video)

    def startdetect(self):
        self.timer_camera.timeout.connect(self.show_detect_video)

    def show_video(self):
        flag, img = self.cap.read()
        height, width, depth = img.shape
        if flag:
            im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转成RGB
            im = QImage(im.data, width, height,
                        width * depth, QImage.Format_RGB888)  # 对读取到的im进行转换
            self.label.setPixmap(QPixmap.fromImage(im))  # 用QPixmap.fromImage函数把im转换成可以放到QLable上的类型。
        else:
            self.cap.release()
            self.timer_camera.stop()

    # def show_detect_video(self):
    #     if len(sys.argv) != 1:
    #         print("Usage:%s camera_id\r\n" % (sys.argv[0]))
    #         sys.exit(0)
    #
    #     # 加载模型
    #     model = Model()
    #     model.load_model(file_path=r'F:/study/project/face/myface/model/zhouletian.face.model.h5')
    #
    #     # 框住人脸的矩形边框颜色
    #     color = (0, 255, 0)
    #
    #     # 捕获指定摄像头的实时视频流
    #     # cap = cv2.VideoCapture(0)
    #
    #     # 人脸识别分类器本地存储路径
    #     cascade_path = r"D:\OpenCV\opencv\build\etc\haarcascades\haarcascade_frontalface_default.xml "
    #
    #     # 循环检测识别人脸
    #     while True:
    #         ret, frame = self.cap.read()  # 读取一帧视频
    #         if ret:
    #
    #             if ret is True:
    #
    #                 # 图像灰化，降低计算复杂度
    #                 frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #                 im = QImage(frame_gray.data, frame_gray.shape[1], frame_gray.shape[0], QImage.Format_RGB888)  # 对读取到的im进行转换
    #                 self.label.setPixmap(QPixmap.fromImage(im))  # 用QPixmap.fromImage函数把im转换成可以放到QLable上的类型。
    #
    #             else:
    #                 continue
    #             # 使用人脸识别分类器，读入分类器
    #             cascade = cv2.CascadeClassifier(cascade_path)
    #
    #             # 利用分类器识别出哪个区域为人脸
    #             faceRects = cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    #             if len(faceRects) > 0:
    #                 for faceRect in faceRects:
    #                     x, y, w, h = faceRect
    #
    #                     # 截取脸部图像提交给模型识别这是谁
    #                     image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
    #                     faceID = model.face_predict(image)
    #
    #                     # 如果是“我”
    #                     if faceID == 0:
    #                         cv2.rectangle(im, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness=2)
    #
    #                         # 文字提示是谁
    #                         cv2.putText(im, 'zhouletian',
    #                                     (x + 30, y + 30),  # 坐标
    #                                     cv2.FONT_HERSHEY_SIMPLEX,  # 字体
    #                                     1,  # 字号
    #                                     (255, 0, 255),  # 颜色
    #                                     2)  # 字的线宽
    #                     # 如果非“我”
    #                     else:
    #                         cv2.rectangle(im, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), thickness=2)
    #                         cv2.putText(im, 'who????',
    #                                     (x + 30, y + 30),  # 坐标
    #                                     cv2.FONT_HERSHEY_SIMPLEX,  # 字体
    #                                     1,  # 字号
    #                                     (255, 0, 255),  # 颜色
    #                                     2)  # 字的线宽
    #
    #             self.label.setPixmap(QPixmap.fromImage(im))  # 用QPixmap.fromImage函数把im转换成可以放到QLable上的类型。
    #
    #             # 等待10毫秒看是否有按键输入
    #             k = cv2.waitKey(10)
    #             # 如果输入q则退出循环
    #             if k & 0xFF == ord('q'):
    #                 break
    #         else:
    #             # 释放摄像头并销毁所有窗口
    #             self.cap.release()
    #             self.timer_camera.stop()
    def show_detect_video(self):
        applying.CatchUsbVideo('人脸区域', 0)

    def smile_detecting(self):
        self.timer_camera.timeout().connect(self.show_detect_video1)

    def show_deect_video1(self):
        smile_detecting.smile_detecting()

    # def currentTextChanged(self, str):
    #     _functions(str)

    def _fuctions(self, str):
        if str == '人脸验证':
            Face_recognition.recognition()

        elif str == '微笑识别':
            smile_detecting.smile_detecting()
        elif str == '表情识别':
            boundary_drawing.boundary_drawing()
        elif str == '关键点检测':
            critical_detecting.critical_detecting()
        elif str == '疲劳检测':
            fatigue_detecting.fatigue_detecting()
        elif str == '年龄性别':
            attrbution.attribution()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MyMainClass()
    window.show()
    app.exec_()
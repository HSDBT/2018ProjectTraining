from __future__ import print_function

# encoding:utf-8
from arc_face import *
import torch
import torch.backends.cudnn as cudnn
from torch.nn import DataParallel

from utils import google_utils
from utils.datasets import *
from utils.utils import *

from silentFace_model.predict_net import *
from silentFace_model.predict_net import AntiSpoofPredict

from facetxt import information
from facetxt import button_sign
from facetxt import button_excel
from facetxt import allname
from facetxt import save_excel_em

import argparse
import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from math import hypot
from mainWindowLayout import logindialog
import cv2
import numpy as np
import dlib          # 人脸处理的库
from import_dir import import_face_photo
import warnings
warnings.filterwarnings("ignore")

sign_a = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
path_photos = ''
class MainWindow(QMainWindow, logindialog):
    returnSignal = pyqtSignal()
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.timer_camera = QTimer()  # 初始化定时器
        self.timer_camera_im = QTimer()  # 初始化定时器
        self.timer_camera_em = QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.CAM_NUM = 0
        self.setupUi(self)
        # self.initUI()
        self.signalSlots()
    # def initUI(self):
    #     self.setLayout(self.gridLayout)
    def signalSlots(self):
        # 方法绑定
        self.import_pushButton.clicked.connect(self.msg)
        # self.import_start_Button.clicked.connect(self.face_search())
        self.timer_camera.timeout.connect(self.show_camera)
        self.cameraButton.clicked.connect(self.slotCameraButton)
        self.sign_pushButton.clicked.connect(self.change_1)
        self.situation_pushButton.clicked.connect(self.change_2)
        self.out_pushButton.clicked.connect(self.change_3)

        #人脸录入
        self.import_savep.clicked.connect(self.change_6)
        self.import_newdir.clicked.connect(self.change_5)
        self.import_start_Button.clicked.connect(self.slotCameraButton_im)
        self.timer_camera_im.timeout.connect(self.face_search)
        self.import_newButton.clicked.connect(self.import_newButton_click)

        #课堂状态
        self.emotion_newButton.clicked.connect(self.slotCameraButton_em)
        self.timer_camera_em.timeout.connect(self.todo_em)
        self.emotion_input.clicked.connect(self.change_7)
        self.emotion_class.clicked.connect(self.change_8)
        self.emotion_out.clicked.connect(self.change_9)

    def todo_em(self):
        input_num =QInputDialog.getInt(self, "人数", "请输入已到人数", 50, 0, 7483647, 1)
        # print(type(input_num[0]))
        # print(input_num[0])
        if input_num[1] == True:
            self.class_emotion(input_num[0])
        else:
            self.timer_camera_em.stop()
            self.cap.release()
            self.cameraLabel_emotion.clear()
            self.emotion_newButton.setText('打开摄像头')

    def change_1(self):
        global sign_a
        sign_a[0] = 1
    def change_2(self):
        global sign_a
        sign_a[1] = 1
    def change_3(self):
        global sign_a
        sign_a[2] = 1
    #创建文件夹
    def change_5(self):
        global sign_a
        sign_a[5] = 1
    #保存图片
    def change_6(self):
        global sign_a
        sign_a[6] = 1
    #当前课堂状态
    def change_7(self):
        global sign_a
        sign_a[7] = 1
    #平均课堂状态
    def change_8(self):
        global sign_a
        sign_a[8] = 1
    #课堂状态导出
    def change_9(self):
        global sign_a
        sign_a[9] = 1
    def import_newButton_click(self):
        dir = QFileDialog.getExistingDirectory(self,
                                                  "选取文件夹",
                                                  "./")  # 起始路径
        global path_photos
        path_photos = dir + '/'
    def msg(self):
        directory1 = QFileDialog.getExistingDirectory(self,
                                                  "选取文件夹",
                                                  "./")  # 起始路径
        if len(directory1) != 0:
            import_face_photo(directory1)
            msg_box = QMessageBox(QMessageBox.Information, '提示', '导入成功')
            msg_box.exec_()

    def class_emotion(self,input_num):
        self.cameraLabel_import.clear()
        self.cameraLabel.clear()
        # 用于求上眼皮与下眼皮的重点
        def midpoint(p1, p2):
            return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

        # 用于计算眼睛长宽比，获取比值
        def get_blinking_ratio(eye_points, facial_landmarks):
            left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
            right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
            # 利用脸谱特征图上的点，获得人脸上眼睛两边的坐标

            center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
            center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
            # 利用脸谱特征图上的点，获得人脸上眼睛上下眼皮的坐标，同时计算中间点的坐标

            hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
            ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
            # 利用hypot函数计算得出线段的长度

            ratio = hor_line_lenght / ver_line_lenght
            # 得到长宽比
            return ratio

        # 使用特征提取器get_frontal_face_detector
        detector = dlib.get_frontal_face_detector()
        # dlib的68点模型，使用作者训练好的特征预测器
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        # # 建cv2摄像头对象，这里使用电脑自带摄像头，如果接了外部摄像头，则自动切换到外部摄像头
        # cap = cv2.VideoCapture(0)
        # # 设置视频参数，propId设置的视频参数，value设置的参数值
        # cap.set(3, 480)
        # 截图screenshoot的计数器
        cnt = 0

        EYE_AR_THRESH = 4
        # 睡眠多少帧之后
        EYE_AR_CONSEC_FRAMES = 50
        # 当前睡眠帧数
        sleep_COUNTER = 0

        # 当前系统中人数
        total = input_num

        # 总的抬头率
        ratio_face = 0

        count = 0
        # 眉毛直线拟合数据缓冲
        line_brow_x = []
        line_brow_y = []
        # 存储所有的情感二维
        all_emotion = []
        # 用于计算抬头率
        list_facenum = []
        global sign_a
        # cap.isOpened（） 返回true/false 检查初始化是否成功
        while (self.cap.isOpened()):
            count += 1
            # cap.read()
            # 返回两个值：
            #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
            #    图像对象，图像的三维矩阵
            flag, im_rd = self.cap.read()

            # 每帧数据延时1ms，延时为0读取的是静态帧
            k = cv2.waitKey(1)

            # 取灰度
            img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

            # 使用人脸检测器检测每一帧图像中的人脸。并返回人脸数rects
            faces = detector(img_gray, 0)
            # 当前抬头率
            # print('当前抬头率: [{:.2%}]'.format(len(faces) / self.total))
            tmp = len(faces) / total
            list_facenum.append(tmp)

            # 待会要显示在屏幕上的字体
            font = cv2.FONT_HERSHEY_SIMPLEX

            # 如果检测到人脸
            if (len(faces) != 0):
                num_happy = 0
                num_nature = 0
                num_yawn = 0

                # # 对每个人脸都标出68个特征点
                # for i in range(len(faces)):
                # enumerate方法同时返回数据对象的索引和数据，k为索引，d为faces中的对象
                for k, d in enumerate(faces):
                    # 用红色矩形框出人脸
                    cv2.rectangle(im_rd, (d.left(), d.top()), (d.right()+1, d.bottom()+1), (0, 0, 255))
                    # 计算人脸热别框边长
                    face_width = d.right() - d.left()

                    # 使用预测器得到68点数据的坐标
                    shape = predictor(im_rd, d)
                    # 圆圈显示每个特征点
                    # for i in range(68):
                    #   cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                    # cv2.putText(im_rd, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    #            (255, 255, 255))

                    # 分析任意n点的位置关系来作为表情识别的依据
                    mouth_width = (shape.part(54).x - shape.part(48).x) / face_width  # 嘴巴咧开程度
                    mouth_higth = (shape.part(66).y - shape.part(62).y) / face_width  # 嘴巴张开程度
                    # print("嘴巴咧开程度{:.2f}".format(mouth_width))
                    # print("嘴巴张开程度{:.2f}".format(mouth_higth))

                    # 通过两个眉毛上的10个特征点，分析挑眉程度和皱眉程度
                    brow_sum = 0  # 高度之和
                    frown_sum = 0  # 两边眉毛距离之和
                    for j in range(17, 21):
                        brow_sum += (shape.part(j).y - d.top()) + (shape.part(j + 5).y - d.top())
                        frown_sum += shape.part(j + 5).x - shape.part(j).x
                        line_brow_x.append(shape.part(j).x)
                        line_brow_y.append(shape.part(j).y)

                    # self.brow_k, self.brow_d = self.fit_slr(line_brow_x, line_brow_y)  # 计算眉毛的倾斜程度
                    tempx = np.array(line_brow_x)
                    tempy = np.array(line_brow_y)
                    z1 = np.polyfit(tempx, tempy, 1)  # 拟合成一次直线
                    brow_k = -round(z1[0], 3)  # 拟合出曲线的斜率和实际眉毛的倾斜方向是相反的

                    brow_hight = (brow_sum / 10) / face_width  # 眉毛高度占比
                    brow_width = (frown_sum / 5) / face_width  # 眉毛距离占比
                    # print("眉毛高度占比{:.2f}".format(brow_hight))
                    # print("眉毛距离占比{:.2f}".format(brow_width))

                    # 眼睛睁开程度
                    eye_sum = (shape.part(41).y - shape.part(37).y + shape.part(40).y - shape.part(38).y +
                               shape.part(47).y - shape.part(43).y + shape.part(46).y - shape.part(44).y)
                    eye_hight = (eye_sum / 4) / face_width
                    # print("眼睛睁开距离与识别框高度之比：",round(eye_open/self.face_width,3))

                    # 分情况讨论
                    if mouth_higth >= 0.1:
                        cv2.putText(im_rd, "yawn", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 0, 255), 2, 4)
                        num_yawn += 1
                    else:
                        if mouth_width >= 0.38:
                            cv2.putText(im_rd, "happy", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
                            num_happy += 1
                        else:
                            cv2.putText(im_rd, "nature", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
                            num_nature += 1

                # 当前课堂情绪状况
                if count % 10 == 0:
                    l_emotion = [num_yawn / len(faces), num_happy / len(faces),num_nature / len(faces)]
                    all_emotion.append(l_emotion)

                if sign_a[7] == 1:
                    ya = round((num_yawn / len(faces) *100),2)
                    ha = round((num_happy / len(faces) *100),2)
                    na = round((num_nature / len(faces) *100),2)
                    head = round((tmp *100),2)
                    msg_box = QMessageBox(QMessageBox.Information, '当前课堂情绪状况',
                    '打哈欠:'+str(ya)+'%、'
                    '开心:'+str(ha)+'%、'
                    '正常:'+str(na)+'%、'
                    '抬头率:' + str(head) + '%')
                    msg_box.exec_()
                    sign_a[7] =0

                for face in faces:
                    landmarks = predictor(img_gray, face)
                    left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
                    right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
                    # 利用函数获得左右眼的比值

                    blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
                    # 取平均数

                    if blinking_ratio > EYE_AR_THRESH:
                        sleep_COUNTER += 1
                        if sleep_COUNTER >= EYE_AR_CONSEC_FRAMES:
                            cv2.putText(im_rd, "Sleep", (10, 100),
                                        font, 1, (0, 0, 255), 1, cv2.LINE_AA)

                            # 睡觉未开发功能

                        cv2.putText(im_rd, "Warning", (10, 30),
                                    font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                    else:
                        sleep_COUNTER = 0
                        #EAR
                        # cv2.putText(im_rd, "EAR:{:.2f}".format(blinking_ratio), (300, 30),
                        #             font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

                # 标出人脸数
                # cv2.putText(im_rd, "Faces: "+str(len(faces)), (20,50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                # 没有检测到人脸
                cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                if sign_a[7] == 1:
                    msg_box = QMessageBox(QMessageBox.Information, '当前课堂情绪状况','抬头率:0.0%')
                    msg_box.exec_()
                    sign_a[7] =0
            if sign_a[8] == 1:
                head_all = round((np.mean(list_facenum) * 100), 2)
                emo = np.mean(all_emotion,0)
                # print(np.mean(all_emotion,0))
                ya_all = round(emo[0] * 100, 2)
                ha_all = round(emo[1] * 100, 2)
                na_all = round(emo[2] * 100, 2)
                msg_box = QMessageBox(QMessageBox.Information, '平均课堂情绪状况',
                                      '打哈欠:' + str(ya_all) + '%、'
                                      '开心:' + str(ha_all) + '%、'
                                      '正常:' + str(na_all) + '%、'
                                      '抬头率:' + str(head_all) + '%')
                msg_box.exec_()
                # print(all_emotion)
                sign_a[8] = 0
            if sign_a[9] == 1:
                head_out = str(round((np.mean(list_facenum) * 100), 2))+ '%'
                emo_out = np.mean(all_emotion,0)
                # print(np.mean(all_emotion,0))
                ya_out = str(round(emo_out[0] * 100, 2)) + '%'
                ha_out  = str(round(emo_out[1] * 100, 2))+ '%'
                na_out  = str(round(emo_out[2] * 100, 2))+ '%'
                dir_em = QFileDialog.getExistingDirectory(self,
                                                         "选取文件夹",
                                                            "./")  # 起始路径
                list_emo = ['打哈欠','开心','正常','抬头率']
                list_emnum = [ya_out,ha_out,na_out,head_out]
                # print(list_emnum)

                save_excel_em(list_emo,list_emnum,dir_em)
                msg_box = QMessageBox(QMessageBox.Information, '提示', '导出成功')
                msg_box.exec_()

                sign_a[9] = 0
            # # 添加说明
            # im_rd = cv2.putText(im_rd, "S: screenshot", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            # im_rd = cv2.putText(im_rd, "Esc: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            # 窗口显示
            # cv2.imshow("Mood and Fatigue Detection", im_rd)

            show = cv2.resize(im_rd, (600, 400))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.cameraLabel_emotion.setPixmap(QPixmap.fromImage(showImage))
            if sign_a[10] == 1:
                for i in range(len(sign_a)):
                    sign_a[i] = 0
                # sign_a[3] = 0
                self.timer_camera_em.stop()
                self.cap.release()
                self.cameraLabel_emotion.clear()
                self.emotion_newButton.setText('打开摄像头')
                return 0


    def face_search(self):
        self.cameraLabel.clear()
        self.cameraLabel_emotion.clear()
        global path_photos
        if len(path_photos) ==0:
            msg_box = QMessageBox(QMessageBox.Information, '提示', '请选择存储位置')
            msg_box.exec_()
            self.timer_camera_im.stop()
            self.cap.release()
            self.cameraLabel_import.clear()
            self.import_start_Button.setText('打开摄像头')
            return 0
        # Dlib的人脸检测器
        detector = dlib.get_frontal_face_detector()

        # Dlib的68点特征预测器
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        # 调用并设置摄像头
        # capture = cv2.VideoCapture(0)
        # capture.set(3, 480)

        # 存储拍照的数量
        counter_for_save_photos = 0

        # 存放所有人照片的路径  path_photos

        # # 判断这个路径（文件夹）是否存在的函数
        def check_folder_exists(path):
            global counter_for_save_photos
            if os.path.isdir(path):
                pass
            else:
                counter_for_save_photos = 0
                os.mkdir(path)

        # 判断'photo_from_camera/'是否存在，不存在就创建一个
        # check_folder_exists(path_photos)

        # 统计已经存在几个用户了，将以一个用户号码存储在person_count中
        # if os.listdir(path_photos):
        #     person_list = os.listdir(path_photos)
        #     person_num_list = []
        #     for person in person_list:
        #         person_num_list.append(int(person[-1]))
        #     person_count = max(person_num_list)
        # else:
        #     person_count = 0

        # sava_flag用来判断当前能否存储照片
        save_flag = 1

        # press_n_flag判断用户有没有按下n来创建新的用户照片文件夹
        press_n_flag = 0

        # 开始检测
        while (self.cap.isOpened()):
            # 读取摄像头数据
            flag, img = self.cap.read()
            # 按键判断
            k = cv2.waitKey(1)

            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            # 返回人脸的对象
            faces = detector(img, 0)

            # 选择字体
            font = cv2.FONT_HERSHEY_COMPLEX

            # 按下n键创建新的用户照片文件夹
            global sign_a
            if sign_a[5] == 1:
                # person_count += 1
                input_name = QInputDialog.getText(self, "创建", "请命名文件夹", text="")
                # print(type(input_name[1]))
                if input_name[1] == True:
                    current_face_dir = path_photos + input_name[0]
                    # current_face_dir = path_photos +  str(person_count)
                    if os.path.isdir(current_face_dir):
                        msg_box = QMessageBox(QMessageBox.Information, '提示', '当前目录下存在同名文件夹' + input_name[0])
                        msg_box.exec_()
                    else:
                        os.makedirs(current_face_dir)
                    # print('\n')
                    # print("新建的人脸照片文件夹:", current_face_dir)

                    counter_for_save_photos = 0
                    press_n_flag = 1
                sign_a[5] = 0
            # 如果人脸只有一个，就用矩形框将面部框起来
            if len(faces) == 1:
                for i, element in enumerate(faces):
                    x1, y1, x2, y2, w, h = element.left(), element.top(), element.right() + 1, element.bottom() + 1, element.width(), element.height()
                    # 矩形框为白色
                    color_rectangle = (255, 255, 255)

                    # 判断脸部矩形框有没有超过边界
                    if ((x2 + w / 2) > 640 or (y2 + h / 2 > 480) or (x1 - w / 2 < 0) or (y1 - h / 2 < 0)):
                        # 超过边界则显示out of range，并将矩形框颜色改为红色
                        cv2.putText(img, "Out of range", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                        color_rectangle = (0, 0, 255)
                        save_flag = 0

                        # 在超过的条件下，按save，提醒调整位置
                        if sign_a[6]==1:
                            # print("请调整位置")
                            msg_box = QMessageBox(QMessageBox.Information, '提示', '请调整位置')
                            msg_box.exec_()
                            sign_a[6] = 0
                    else:
                        # 没有超过边界的话，并且当前条件是只有一张人脸，判定为可以拍照，矩形框为白色
                        color_rectangle = (255, 255, 255)
                        save_flag = 1

                    # 绘制矩形框
                    cv2.rectangle(img, (x1 - int(w / 8), y1 - int(h / 2)), (x2 + int(w / 8), y2 + int(h / 8)),
                                  color_rectangle, 2)

                    # print(x1 - int(w / 8)-x2 - int(w / 8))
                    h_img_b = x2 + int(w / 8) - x1 + int(w / 8) + 45
                    w_img_b = y2 + int(h / 8) - y1 + int(h / 2) - 90
                    # print(h_img_b,w_img_b)
                    # 新建一个空白图像，存储人脸区域
                    # img_blank = np.zeros((int(h * 1.35), w * 1, 3), np.uint8)
                    img_blank = np.zeros((h_img_b, w_img_b, 3), np.uint8)
                    # 如果满足可以拍照的条件，即save_flag为1并且用户按下s，进入下一个判定条件
                    if save_flag and sign_a[6]==1:
                        # 如果用户已经创建了新的文件夹，就可以存储照片了
                        if press_n_flag:
                            # 每存一张照片成功，照片计数器加一
                            counter_for_save_photos += 1
                            # for i in range(int(h * 1.35)):
                            #     for j in range(w * 1):
                            for i in range(h_img_b):
                                for j in range(w_img_b):
                                    # (480, 640, 3)
                                    img_blank[i][j] = img[y1 - int(h / 2) + i + 10][x1 - int(w / 8) + j + 10]

                            # 这里的check主要是避免用户创建了文件夹，存了几张照片后，又将此文件夹销毁的情况
                            check_folder_exists(current_face_dir)
                            # 如果照片累加器大于0，就存放照片
                            if (counter_for_save_photos > 0):
                                path_img_face = current_face_dir + "/img_face_" + str(counter_for_save_photos) + ".jpg"
                                cv2.imwrite('{}'.format(path_img_face), img_blank)
                                # print("img_face_" + str(counter_for_save_photos) + ".jpg""写入文件夹：" + current_face_dir)
                            msg_box = QMessageBox(QMessageBox.Information, '提示', '保存成功')
                            msg_box.exec_()
                        else:
                            msg_box = QMessageBox(QMessageBox.Information, '提示', '请先点击创建文件夹')
                            msg_box.exec_()
                            # print("请按s前先按n新建人脸文件夹")
                        sign_a[6] = 0
            # 如果摄像头没有检测到人脸，用cv2.putText输出警告信息"No face detected"
            elif len(faces) == 0:
                if sign_a[6]==1:
                    msg_box = QMessageBox(QMessageBox.Information, '提示', '未检测到人脸')
                    msg_box.exec_()
                    sign_a[6] = 0
                #     print("未检测到人脸")
                # cv2.putText(img, "No face detected", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            # 如果摄像头检测到不止一张人脸，用cv2.putText输出警告信息"Only one can be detected"
            elif len(faces) > 1:
                if sign_a[6]==1:
                    # print("人脸数量大于1")
                    msg_box = QMessageBox(QMessageBox.Information, '提示', '人脸数量大于1')
                    msg_box.exec_()
                    sign_a[6] = 0
                # cv2.putText(img, "Only one can be detected", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            # 显示检测到人脸的数量
            cv2.putText(img, "faces: " + str(len(faces)), (20, 100), font, 0.8, (255, 0, 0), 1, cv2.LINE_AA)

            # 显示已经拍了几张照片了
            cv2.putText(img, str(counter_for_save_photos) + " pictures have been taken", (250, 40), font, 0.8,
                        (255, 0, 0), 1, cv2.LINE_AA)

            # 标题以及说明文字
            cv2.putText(img, "Face Register", (10, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            # cv2.putText(img, "N: New face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
            # cv2.putText(img, "S: Save current face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
            # cv2.putText(img, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

            # 如果按下q，就退出
            if sign_a[4] == 1:
                for i in range(len(sign_a)):
                    sign_a[i] = 0
                # sign_a[3] = 0
                self.timer_camera_im.stop()
                self.cap.release()
                self.cameraLabel_import.clear()
                self.import_start_Button.setText('打开摄像头')
                return 0
            show = cv2.resize(img, (600, 400))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.cameraLabel_import.setPixmap(QPixmap.fromImage(showImage))

    def show_camera(self):
        self.cameraLabel_import.clear()
        self.cameraLabel_emotion.clear()
        all_namelist = allname("./pic")
        def cv2_letterbox_image(image, expected_size):
            ih, iw = image.shape[0:2]
            ew, eh = expected_size, expected_size
            scale = min(eh / ih, ew / iw)  # 最大边缩放至416得比例
            nh = int(ih * scale)
            nw = int(iw * scale)
            image = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_CUBIC)  # 等比例缩放，使得有一边416
            top = (eh - nh) // 2  # 上部分填充的高度
            bottom = eh - nh - top  # 下部分填充的高度
            left = (ew - nw) // 2  # 左部分填充的距离
            right = ew - nw - left  # 右部分填充的距离
            # 边界填充
            new_img = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT)
            return new_img

        def cosin_metric(x1, x2):
            # 计算余弦距离
            return np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))

        def load_image(img_path):
            image = cv2.imread(img_path, 0)
            if image is None:
                return None
            # image = cv2_letterbox_image(image,128)
            image = cv2.resize(image, (128, 128))
            image = np.dstack((image, np.fliplr(image)))
            image = image.transpose((2, 0, 1))
            image = image[:, np.newaxis, :, :]
            image = image.astype(np.float32, copy=False)
            image -= 127.5
            image /= 127.5
            return image

        def get_featuresdict(model, dir):
            list_i = os.listdir(dir)
            person_dict_all = {}
            for i, each_i in enumerate(list_i):
                dir_j = dir + '/' + each_i
                list_j = os.listdir(dir_j)
                # print(dir_j)
                person_dict = {}
                for j, each_j in enumerate(list_j):
                    # print(j)
                    # print(each_j)
                    image = load_image(f"pic/{each_i}/{each_j}")
                    data = torch.from_numpy(image)
                    data = data.to(torch.device("cuda"))
                    output = model(data)  # 获取特征
                    output = output.data.cpu().numpy()
                    # print(output.shape)
                    # 获取不重复图片 并分组
                    fe_1 = output[0]
                    fe_2 = output[1]
                    # print("this",cnt)
                    # print(fe_1.shape,fe_2.shape)
                    feature = np.hstack((fe_1, fe_2))
                    # print(feature.shape)
                    person_dict[each_j] = feature
                person_dict_all[each_i] = person_dict
                # print(person_dict)
            # print(person_dict_all)
            return person_dict_all

        def get_ouyannanafeature(model):

            image = load_image("inference/ouyanana.jpg")
            # print(image.shape)

            data = torch.from_numpy(image)
            data = data.to(torch.device("cuda"))
            output = model(data)  # 获取特征
            output = output.data.cpu().numpy()
            # print(output.shape)

            # 获取不重复图片 并分组
            fe_1 = output[0]
            fe_2 = output[1]
            # print("this",cnt)
            # print(fe_1.shape,fe_2.shape)
            feature = np.hstack((fe_1, fe_2))
            # print(feature.shape)

            person_dict = {}
            person_dict["ouyannana"] = feature

            return person_dict

        def detect(save_img=False):
            out, source, weights, view_img, save_txt, imgsz = \
                opt.output, opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size  # 加载配置信息

            webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith(
                '.txt')  # 判断测试的资源类型

            # Initialize
            device = torch_utils.select_device(opt.device)
            dir = "pic"

            # 创建输出文件夹
            if os.path.exists(out):
                shutil.rmtree(out)  # delete output folder
            os.makedirs(out)  # make new output folder
            # gpu是否支持半精度 提高性能
            half = device.type != 'cpu'  # half precision only supported on CUDA

            # Load model

            model = torch.load(weights, map_location=device)['model'].float()  # load to FP32

            model.to(device).eval()

            arcface_model = resnet_face18(False)

            arcface_model = DataParallel(arcface_model)
            # load_model(model, opt.test_model_path)
            arcface_model.load_state_dict(torch.load('weights/resnet18_110.pth'), strict=False)
            arcface_model.to(torch.device("cuda")).eval()

            pred_model = AntiSpoofPredict(0)

            if half:
                model.half()  # to FP16

            features = get_featuresdict(arcface_model, dir)

            vid_path, vid_writer = None, None
            if webcam:
                view_img = True
                cudnn.benchmark = True  # set True to speed up constant image size inference
                dataset = LoadStreams(source, img_size=imgsz)
            else:
                # 图片和视频的加载
                save_img = True
                dataset = LoadImages(source, img_size=imgsz)
            view_img = True
            # Get names and colors 获得框框的类别名和颜色
            names = model.names if hasattr(model, 'names') else model.modules.names
            colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

            # Run inference 推理过程
            t0 = time.time()

            img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
            _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once 模拟启动
            # 数据预处理
            for path, img, im0s, vid_cap in dataset:
                img = torch.from_numpy(img).to(device)
                img = img.half() if half else img.float()  # uint8 to fp16/32
                img /= 255.0  # 0 - 255 to 0.0 - 1.0
                if img.ndimension() == 3:
                    img = img.unsqueeze(0)
                # Inference
                t1 = torch_utils.time_synchronized()
                pred = model(img, augment=opt.augment)[0]

                # Apply NMS 执行nms筛选boxes
                pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes,
                                           agnostic=opt.agnostic_nms)
                t2 = torch_utils.time_synchronized()

                # Process detections
                for i, det in enumerate(pred):  # detections per image
                    if webcam:  # batch_size >= 1
                        p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
                    else:
                        p, s, im0 = path, '', im0s

                    save_path = str(Path(out) / Path(p).name)
                    s += '%gx%g ' % img.shape[2:]  # print string

                    gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  #  normalization gain whwh

                    if det is not None and len(det):  # 假如预测到有目标（盒子存在）
                        # Rescale boxes from img_size to im0 size 还原盒子在原图上的位置
                        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                        # Print results 打印box的结果信息
                        for c in det[:, -1].unique():
                            n = (det[:, -1] == c).sum()  # detections per class
                            s += '%g %ss, ' % (n, names[int(c)])  # add to string

                        # Write results
                        for *xyxy, conf, cls in det:  # x1 y1 x2 y2 cls class
                            prediction = np.zeros((1, 3))
                            # crop
                            face_img = im0[int(xyxy[1]):int(xyxy[3]), int(xyxy[0]):int(xyxy[2])]
                            # rf_size
                            rf_img = cv2.resize(face_img, (80, 80))

                            # recognition
                            face_img = cv2.resize(face_img, (128, 128))

                            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

                            face_img = np.dstack((face_img, np.fliplr(face_img)))

                            face_img = face_img.transpose((2, 0, 1))
                            face_img = face_img[:, np.newaxis, :, :]

                            face_img = face_img.astype(np.float32, copy=False)
                            face_img -= 127.5
                            face_img /= 127.5

                            face_data = torch.from_numpy(face_img)
                            face_data = face_data.to(torch.device("cuda"))

                            _output = arcface_model(face_data)  # 获取特征
                            _output = _output.data.cpu().numpy()

                            fe_1 = _output[0]
                            fe_2 = _output[1]

                            _feature = np.hstack((fe_1, fe_2))

                            list = os.listdir(dir)
                            max_f = 0
                            t = 0
                            label = "none"
                            for i, each_i in enumerate(list):
                                dir_j = dir + '/' + each_i
                                list_j = os.listdir(dir_j)
                                for j, each_j in enumerate(list_j):
                                    # print(each_j)
                                    t = cosin_metric(features[each_i][each_j], _feature)
                                    # print(each, t)
                                    if t > max_f:
                                        max_f = t
                                        max_n = each_i
                                    # print(max_n,max_f)
                            if (max_f > 0.6):
                                max_f = round(max_f, 2)
                                # label = max_n + str(max_f)
                                label = max_n
                            # 活体检测 与for内部还是同级
                            if opt.open_rf:
                                # pred real or fack
                                for model_name in os.listdir("weights/anti_spoof_models"):
                                    # print(model_test.predict(img, os.path.join(model_dir, model_name)))

                                    prediction += pred_model.predict(rf_img, os.path.join("weights/anti_spoof_models",
                                                                                          model_name))
                                rf_label = np.argmax(prediction)
                                value = prediction[0][rf_label] / 2
                                print(rf_label, value)
                                if rf_label == 1 and value > 0.90:
                                    label += "_real"
                                else:
                                    label += "_fake"

                            plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

                    # Print time (inference + NMS)
                    # print('%sDone. (%.3fs)' % (s, t2 - t1)) # 输出执行时间
                    # Stream results # 显示输出
                    if view_img:
                        self.image = im0
                        show = cv2.resize(self.image, (600, 400))
                        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
                        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)

                        self.cameraLabel.setPixmap(QPixmap.fromImage(showImage))
                        global sign_a
                        if sign_a[0] == 1:
                            information(label)
                            sign_a[0] = 0

                        if sign_a[1] == 1:
                            button_sign(all_namelist)
                            sign_a[1] = 0

                        if sign_a[2] == 1:
                            dir_m = QFileDialog.getExistingDirectory(self,
                                                                          "选取文件夹",
                                                                          "./")  # 起始路径
                            # print(type(directory1))
                            # print(len(directory1))
                            sign_a[2] = 0
                            if len(dir_m) != 0:
                                button_excel(dir_m,all_namelist)
                                msg_box = QMessageBox(QMessageBox.Information, '提示', '导出成功')
                                msg_box.exec_()

                        if sign_a[3] == 1:
                            for i in range(len(sign_a)):
                                sign_a[i] = 0
                            # sign_a[3] = 0
                            self.timer_camera.stop()
                            self.cap.release()
                            self.cameraLabel.clear()
                            self.cameraButton.setText('打开摄像头')
                            return 0

                    # Save results (image with detections)
                    if save_img:  # 保存图片or视频
                        if dataset.mode == 'images':
                            cv2.imwrite(save_path, im0)
                        else:
                            if vid_path != save_path:  # new video
                                vid_path = save_path
                                if isinstance(vid_writer, cv2.VideoWriter):
                                    vid_writer.release()  # release previous video writer

                                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*opt.fourcc), fps,
                                                             (w, h))
                            vid_writer.write(im0)

            if save_txt or save_img:
                print('Results saved to %s' % os.getcwd() + os.sep + out)
                if platform == 'darwin':  # MacOS
                    os.system('open ' + save_path)

            print('Done. (%.3fs)' % (time.time() - t0))

        if __name__ == '__main__':
            parser = argparse.ArgumentParser()
            parser.add_argument('--weights', type=str, default='weights/best.pt', help='model.pt path')
            # parser.add_argument('--source', type=str, default='inference/images', help='source')  # file/folder, 0 for webcam
            parser.add_argument('--source', type=str, default='0', help='source')  # file/folder, 0 for webcam
            parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
            parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
            parser.add_argument('--conf-thres', type=float, default=0.4, help='object confidence threshold')
            parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
            parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
            parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
            parser.add_argument('--view-img', action='store_true', help='display results')
            parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
            parser.add_argument('--classes', nargs='+', type=int, help='filter by class')
            parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
            parser.add_argument('--augment', action='store_true', help='augmented inference')
            parser.add_argument('--open_rf', default=0, help='if open real/fake 1 0 ')
            opt = parser.parse_args()
            opt.img_size = check_img_size(opt.img_size)
            print(opt)

            with torch.no_grad():
                detect()
    # 打开关闭摄像头控制
    def slotCameraButton(self):
        if self.timer_camera.isActive() == False:

            # 打开摄像头并显示图像信息
            self.openCamera()
        else:
            # 关闭摄像头并清空显示信息
            global sign_a
            sign_a[3] = 1
            # self.closeCamera()

    # 打开摄像头
    def openCamera(self):
        flag = self.cap.open(self.CAM_NUM)

        if flag == False:
            msg = QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                      buttons=QMessageBox.Ok,
                                      defaultButton=QMessageBox.Ok)
            msg.exec_()
        else:
            for i in range(len(sign_a)):
                sign_a[i] = 0
            self.timer_camera_im.stop()
            # self.cameraLabel_import.clear()
            self.import_start_Button.setText('打开摄像头')
            self.timer_camera_em.stop()
            # self.cameraLabel_emotion.clear()
            self.emotion_newButton.setText('打开摄像头')

            self.timer_camera.start(30)
            self.cameraButton.setText('关闭摄像头')


    #人脸获取
    def slotCameraButton_im(self):
        if self.timer_camera_im.isActive() == False:

            # 打开摄像头并显示图像信息
            self.openCamera_im()
        else:
            # 关闭摄像头并清空显示信息
            global sign_a
            sign_a[4] = 1
            # self.closeCamera()

    # 打开摄像头
    def openCamera_im(self):
        flag = self.cap.open(self.CAM_NUM)

        if flag == False:
            msg = QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                      buttons=QMessageBox.Ok,
                                      defaultButton=QMessageBox.Ok)
            msg.exec_()
        else:
            for i in range(len(sign_a)):
                sign_a[i] = 0
            self.timer_camera.stop()
            # self.cameraLabel.clear()
            self.cameraButton.setText('打开摄像头')
            self.timer_camera_em.stop()
            # self.cameraLabel_emotion.clear()
            self.emotion_newButton.setText('打开摄像头')
            self.timer_camera_im.start(30)
            self.import_start_Button.setText('关闭摄像头')

    #人脸获取
    def slotCameraButton_em(self):
        if self.timer_camera_em.isActive() == False:

            # 打开摄像头并显示图像信息
            self.openCamera_em()
        else:
            # 关闭摄像头并清空显示信息
            global sign_a
            sign_a[10] = 1
            # self.closeCamera()

    # 打开摄像头
    def openCamera_em(self):
        flag = self.cap.open(self.CAM_NUM)

        if flag == False:
            msg = QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                      buttons=QMessageBox.Ok,
                                      defaultButton=QMessageBox.Ok)
            msg.exec_()
        else:
            self.timer_camera_em.start(30)
            for i in range(len(sign_a)):
                sign_a[i] = 0
            self.timer_camera_im.stop()
            # self.cameraLabel_import.clear()
            self.import_start_Button.setText('打开摄像头')
            self.timer_camera.stop()
            # self.cameraLabel.clear()
            self.cameraButton.setText('打开摄像头')

            self.emotion_newButton.setText('关闭摄像头')


    # 关闭摄像头
    # def closeCamera(self):
        # self.timer_camera.stop()
        #
        # self.cap.release()
        # self.cameraLabel.clear()
        # self.cameraButton.setText('打开摄像头')
if __name__=='__main__':

    app=QApplication(sys.argv)

    mw=MainWindow()
    mw.show()
    sys.exit(app.exec_())
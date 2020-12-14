
"""
从视屏中识别人脸，并实时标出面部特征点
"""

import dlib                     #人脸识别的库dlib
import numpy as np              #数据处理的库numpy
import cv2                      #图像处理的库OpenCv
from math import hypot
# 使用特征提取器get_frontal_face_detector
detector = dlib.get_frontal_face_detector()
# dlib的68点模型，使用作者训练好的特征预测器
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#建cv2摄像头对象，这里使用电脑自带摄像头，如果接了外部摄像头，则自动切换到外部摄像头
cap = cv2.VideoCapture(0)
# 设置视频参数，propId设置的视频参数，value设置的参数值
cap.set(3, 480)
# 截图screenshoot的计数器
cnt = 0

EYE_AR_THRESH = 4
#睡眠多少帧之后
EYE_AR_CONSEC_FRAMES = 50
#当前睡眠帧数
sleep_COUNTER = 0

# 当前系统中人数
total = 3

#总的抬头率
ratio_face = 0

count = 0

#用于求上眼皮与下眼皮的重点
def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

#用于计算眼睛长宽比，获取比值
def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    #利用脸谱特征图上的点，获得人脸上眼睛两边的坐标

    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    #利用脸谱特征图上的点，获得人脸上眼睛上下眼皮的坐标，同时计算中间点的坐标

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    #利用hypot函数计算得出线段的长度

    ratio = hor_line_lenght / ver_line_lenght
    #得到长宽比
    return ratio



# 眉毛直线拟合数据缓冲
line_brow_x = []
line_brow_y = []
#存储所有的情感二维
all_emotion = []
#用于计算抬头率
list_facenum = []

# cap.isOpened（） 返回true/false 检查初始化是否成功
while(cap.isOpened()):
    count +=1
    # cap.read()
    # 返回两个值：
    #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
    #    图像对象，图像的三维矩阵
    flag, im_rd = cap.read()

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
    if(len(faces)!=0):
        num_happy = 0
        num_nature = 0
        num_amazing = 0
        num_angry = 0

        # # 对每个人脸都标出68个特征点
        # for i in range(len(faces)):
            # enumerate方法同时返回数据对象的索引和数据，k为索引，d为faces中的对象
        for k, d in enumerate(faces):
            # 用红色矩形框出人脸
            cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
            # 计算人脸热别框边长
            face_width = d.right() - d.left()

            # 使用预测器得到68点数据的坐标
            shape = predictor(im_rd, d)
            # 圆圈显示每个特征点
            #for i in range(68):
             #   cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                #cv2.putText(im_rd, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                #            (255, 255, 255))

            # 分析任意n点的位置关系来作为表情识别的依据
            # mouth_width = (shape.part(54).x - shape.part(48).x) / face_width  # 嘴巴咧开程度
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

            # brow_hight = (brow_sum / 10) / self.face_width  # 眉毛高度占比
            # brow_width = (frown_sum / 5) / self.face_width  # 眉毛距离占比
            # print("眉毛高度占比{:.2f}".format(brow_hight))
            # print("眉毛距离占比{:.2f}".format(brow_width))

            # 眼睛睁开程度
            eye_sum = (shape.part(41).y - shape.part(37).y + shape.part(40).y - shape.part(38).y +
                       shape.part(47).y - shape.part(43).y + shape.part(46).y - shape.part(44).y)
            eye_hight = (eye_sum / 4) / face_width
            # print("眼睛睁开距离与识别框高度之比：",round(eye_open/self.face_width,3))

            # 分情况讨论
            # 张嘴，可能是开心或者惊讶
            if round(mouth_higth >= 0.03):
                if eye_hight >= 0.056:
                    cv2.putText(im_rd, "amazing", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 0, 255), 2, 4)
                    num_amazing += 1
                else:
                    cv2.putText(im_rd, "happy", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 0, 255), 2, 4)
                    num_happy += 1

            # 没有张嘴，可能是正常和生气
            else:
                if brow_k <= -0.3:
                    cv2.putText(im_rd, "angry", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 0, 255), 2, 4)
                    num_angry += 1
                else:
                    cv2.putText(im_rd, "nature", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 0, 255), 2, 4)
                    num_nature += 1
      # 当前课堂情绪状况
        if count %10 ==0:
            print('当前课堂情绪状况')
            print('amazing',num_amazing / len(faces))
            print('happy',num_happy/ len(faces))
            print('angry',num_angry / len(faces))
            print('nature',num_nature / len(faces))
            l_emotion = [num_amazing / len(faces), num_happy/ len(faces), num_angry / len(faces),num_nature / len(faces)]
            all_emotion.append(l_emotion)

        
        for face in faces:
                    landmarks = predictor(img_gray, face)
                    left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
                    right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
                    #利用函数获得左右眼的比值

                    blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
                    #取平均数

                    if blinking_ratio > EYE_AR_THRESH:
                        sleep_COUNTER += 1
                        if sleep_COUNTER  >= EYE_AR_CONSEC_FRAMES:
                           cv2.putText(im_rd, "Sleep", (10, 100),
                                    font, 1, (0, 0, 255), 1, cv2.LINE_AA)

                           #睡觉未开发功能

                        cv2.putText(im_rd, "Warning", (10, 30),
                                    font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                    else:
                        sleep_COUNTER = 0
                        cv2.putText(im_rd, "EAR:{:.2f}".format(blinking_ratio), (300, 30),
                                    font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

        # 标出人脸数
        # cv2.putText(im_rd, "Faces: "+str(len(faces)), (20,50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
    else:
        # 没有检测到人脸
        cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # 添加说明
    im_rd = cv2.putText(im_rd, "S: screenshot", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
    im_rd = cv2.putText(im_rd, "Esc: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

    key = cv2.waitKey(1) & 0xFF
    # 按下s键截图保存
    if (key == ord('s')):
        cnt+=1
        cv2.imwrite("screenshoot"+str(cnt)+".jpg", im_rd)

    # 按下Esc键退出
    if(key == 27):
        break

    # 窗口显示
    cv2.imshow("Mood and Fatigue Detection", im_rd)

# 释放摄像头
cap.release()

# 删除建立的窗口
cv2.destroyAllWindows()
x = 0
for i in list_facenum:
    x += i
ratio_face = x / len(list_facenum)


print(list_facenum)
print(ratio_face)
print(all_emotion)


# if __name__ == "__main__":
#     my_face = face_emotion()
#     my_face.learning_face()
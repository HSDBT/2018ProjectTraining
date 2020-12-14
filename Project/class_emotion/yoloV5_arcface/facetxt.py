import os
import cv2
import numpy as np
import pandas as pd

#签到姓名列表
from PyQt5.QtWidgets import QMessageBox

namelist = []
a = 1
nonamelist = []
#读取人脸数据中所有人的姓名
def allname(dir):
    all_namelist = []
    list_f = os.listdir(dir)
    for i in list_f:
        all_namelist.append(i)
    return all_namelist

# allnamelist = allname("./pic")
#
# print(allnamelist)

#未签到人名单
def no_sign_in(anl,nl=namelist):
    no_namelist = []
    for i in range(len(anl)):
        if anl[i] not in [ns for ns in nl]:
            no_namelist.append(anl[i])
    return no_namelist

# # 签到成功/失败
# def information(label,namel = namelist,nonamel = nonamelist):
#     if cv2.waitKey(1) == ord('t'):#  注释之后就可以实现实时签到（一人只在一个屏幕最好）
#         if label != 'none':
#             if label[:label.index('.')-1] not in [na for na in namel]:
#                 namel.append(label[:label.index('.')-1])
#                 print(label[:label.index('.')-1] + "签到成功")
#             else:
#                 print(label[:label.index('.')-1] + "请勿重复签到")
#         else:
#             print("识别失败")
#     #显示签到情况
#     if cv2.waitKey(1) == ord('p'):
#         print("已签到",namel)
#         print("未签到",no_sign_in(nl=namel))
#     # #导出签到情况
#     if cv2.waitKey(1) == ord('o'):        #出现nonamelist为空现象
#         save_excel(namel,no_sign_in(nl=namel))
#         print("导出成功")

# # 签到成功/失败
# def information(label):
#     if cv2.waitKey(1) == ord('t'):#  注释之后就可以实现实时签到（一人只在一个屏幕最好）
#         if label != 'none':
#             if label[:label.index('.')-1] not in [na for na in namelist]:
#             # if label not in [na for na in namelist]:
#                 namelist.append(label[:label.index('.')-1])
#                 print(label[:label.index('.')-1] + "签到成功")
#             else:
#                 print(label[:label.index('.')-1] + "请勿重复签到")
#         else:
#             print("识别失败")
#
# 签到成功/失败
def information(label):
    # if cv2.waitKey(1) == ord('t'):#  注释之后就可以实现实时签到（一人只在一个屏幕最好）
    if label != 'none':
        if label not in [na for na in namelist]:
        # if label not in [na for na in namelist]:
            namelist.append(label)
            # print(label + "签到成功")
            msg_box = QMessageBox(QMessageBox.Information, '提示', label + "签到成功")
            msg_box.exec_()
        else:
            # print(label + "请勿重复签到")
            msg_box = QMessageBox(QMessageBox.Information, '提示', label + "请勿重复签到")
            msg_box.exec_()
    else:
        # print("识别失败")
        msg_box = QMessageBox(QMessageBox.Information, '提示', "识别失败")
        msg_box.exec_()
# def button_sign():
#     #显示签到情况
#     if cv2.waitKey(1) == ord('p'):
#         print("已签到",namelist)
#         print("未签到",no_sign_in(nl=namelist))
def button_sign(anl):
    #显示签到情况
    no_slist = no_sign_in(anl,nl=namelist)
    # print("已签到",namelist)
    # print("未签到",no_slist)
    if len(no_slist) == 0:
        msg_box = QMessageBox(QMessageBox.Information, '提示', "全勤")
        msg_box.exec_()
    else :
        str_s = '未签到' + str(len(no_slist)) + '人' + ':'
        for i in range(len(no_slist)):
            if i == len(no_slist) -1 :
                str_s += no_slist[i]
            else:
                str_s += no_slist[i] + '、'
        msg_box = QMessageBox(QMessageBox.Information, '提示', str_s)
        msg_box.exec_()
def button_excel(dir,anl):
    # #导出签到情况
    # if cv2.waitKey(1) == ord('o'):        #出现nonamelist为空现象
    save_excel(namelist,no_sign_in(anl,nl=namelist),dir)
    # print("导出成功")


def save_excel(list_sign,list_no_sign,dir):
    dir_s = dir + '/'+'签到情况.xlsx'
    writer = pd.ExcelWriter(os.path.join(os.getcwd(), dir_s))
    t_sign = ["已签到" for i in list_sign]
    f_sign = ["未签到" for i in list_no_sign]
    #签到情况
    sign = t_sign +f_sign
    #姓名
    list_s = list_sign + list_no_sign
    df1 = pd.DataFrame(list_s)
    df2 = pd.DataFrame(sign)
    df1.to_excel(writer, index=False, header=['姓名'])  # startcol=**， startrow=**)
    df2.to_excel(writer, index=False, header=['签到情况'], startcol=1)  # startcol=**， startrow=**)
    writer.save()  # 写入硬盘

def save_excel_em(list_emo,list_emnum,dir):
    dir_s = dir + '/'+'课堂状态.xlsx'
    writer = pd.ExcelWriter(os.path.join(os.getcwd(), dir_s))

    df1 = pd.DataFrame(list_emo)
    df2 = pd.DataFrame(list_emnum)
    df1.to_excel(writer, index=False, header=['情感状态'])  # startcol=**， startrow=**)
    df2.to_excel(writer, index=False, header=['占比'], startcol=1)  # startcol=**， startrow=**)
    writer.save()  # 写入硬盘
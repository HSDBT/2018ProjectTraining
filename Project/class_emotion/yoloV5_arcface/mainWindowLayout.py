# 主要的思路就是创建两个frame（如果有两个以上同理）使用setVisible()函数显示或者隐藏frame 参数是bool值<br>import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets



class logindialog(object):
    def setupUi(self, CameraPage):
        self.setWindowTitle('课堂情感实时分析系统')
        self.resize(900, 700)

        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # #阴影bug

        # self.frame_m =  QFrame(self)
        # self.vertical = QtWidgets.QGridLayout(self.frame_m)
        # self.frame_m.setGeometry(QtCore.QRect(0, 0,900,700))
        # self.camLabel = QtWidgets.QLabel()
        # self.camLabel.setStyleSheet("background-color: white")
        # self.vertical.addWidget(self.camLabel,0,0,10,10)
        #
        # # 阴影效果
        # self.shadow = QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(15)
        # self.shadow.setOffset(0, 0)
        # self.camLabel.setGraphicsEffect(self.shadow)



        self.frame_minmax =  QFrame(self)
        self.frame_minmax.setGeometry(QtCore.QRect(10, 0,100,50))
        self.verticalLayout_minmax = QtWidgets.QGridLayout(self.frame_minmax)

        self.mini_pushButton = QPushButton()
        self.mini_pushButton.setText("")
        self.verticalLayout_minmax.addWidget(self.mini_pushButton, 0, 0, 1, 1)

        self.closs_pushButton = QPushButton()
        self.closs_pushButton.setText("")
        self.verticalLayout_minmax.addWidget(self.closs_pushButton, 0, 1, 1, 1)



        #登录界面
        self.frame_sign = QFrame(self)
        self.frame_sign.setGeometry(QtCore.QRect(280, 200, 400, 300))
        self.verticalLayout_sign = QtWidgets.QGridLayout(self.frame_sign)

        self.photo_sign = QtWidgets.QLabel()
        self.photo_sign.setText("课堂状态实时分析系统")
        self.verticalLayout_sign.addWidget(self.photo_sign, 0, 0, 1, 2)
        self.photo_sign.setFixedSize(300, 40)
        self.photo_sign.setStyleSheet("font-family:'楷体';font-size:30px;color:black;")


        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        self.lineEdit_account.setFixedSize(300, 40)
        self.verticalLayout_sign.addWidget(self.lineEdit_account,1,0,1,2)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.lineEdit_password.setFixedSize(300, 40)
        self.verticalLayout_sign.addWidget(self.lineEdit_password,2,0,1,2)

        self.pushButton_sign = QPushButton()
        self.pushButton_sign.setText("登录")
        self.pushButton_sign.setFixedSize(100, 40)
        self.verticalLayout_sign.addWidget(self.pushButton_sign,3,1,1,1)

        self.pushButton_register = QPushButton()
        self.pushButton_register.setText("注册")
        self.pushButton_register.setFixedSize(100, 40)
        self.verticalLayout_sign.addWidget(self.pushButton_register,3,0,1,1)

        #注册界面
        self.frame_register = QFrame(self)
        self.frame_register.setGeometry(QtCore.QRect(170, 200, 600, 300))
        self.verticalLayout_register = QtWidgets.QGridLayout(self.frame_register)
        self.lineEdit_account_register = QLineEdit()
        self.lineEdit_account_register.setPlaceholderText("请输入邮箱或手机号")
        self.lineEdit_account_register.setFixedSize(300, 40)
        self.verticalLayout_register.addWidget(self.lineEdit_account_register,0,0,1,1)


        self.lineEdit_password_register = QLineEdit()
        self.lineEdit_password_register.setPlaceholderText("请输入密码")
        self.lineEdit_password_register.setFixedSize(300, 40)
        self.verticalLayout_register.addWidget(self.lineEdit_password_register,1,0,1,1)

        self.lineEdit_password_register_two = QLineEdit()
        self.lineEdit_password_register_two.setPlaceholderText("请再次输入密码")
        self.lineEdit_password_register_two.setFixedSize(300, 40)
        self.verticalLayout_register.addWidget(self.lineEdit_password_register_two,2,0,1,1)

        self.lineEdit_Verification_Code = QLineEdit()
        self.lineEdit_Verification_Code.setPlaceholderText("验证码")
        self.lineEdit_Verification_Code.setFixedSize(300, 40)
        self.verticalLayout_register.addWidget(self.lineEdit_Verification_Code,3,0,1,1)

        self.pushButton_complete_register = QPushButton()
        self.pushButton_complete_register.setText("完成注册")
        self.pushButton_complete_register.setFixedSize(300, 40)
        self.verticalLayout_register.addWidget(self.pushButton_complete_register,4,0,1,1)

        self.pushButton_return_sign = QPushButton()
        self.pushButton_return_sign.setText("返回登录")
        self.pushButton_return_sign.setFixedSize(300, 40)
        self.verticalLayout_register.addWidget(self.pushButton_return_sign,5,0,1,1)



        #最上方三个功能
        self.frame = QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 30, 900, 100))
        self.verticalLayout = QtWidgets.QGridLayout(self.frame)
        #x,y,宽高
        # self.frame.setGeometry(QtCore.QRect(100,100,200,100))
        #用背景图来生成横线，上面下面不同颜色分割
        # self.frame.setStyleSheet('border:2px solid red')
        self.pushButton_enter_import = QPushButton()
        self.pushButton_enter_import.setText("人脸获取")
        self.pushButton_enter_import.setFixedSize(200,60)
        self.verticalLayout.addWidget(self.pushButton_enter_import,0,0,1,1)
        self.pushButton_enter_distinguish = QPushButton()
        self.pushButton_enter_distinguish.setText("人脸识别")
        self.pushButton_enter_distinguish.setFixedSize(200, 60)
        self.verticalLayout.addWidget(self.pushButton_enter_distinguish,0,1,1,1)
        self.pushButton_enter_emotion = QPushButton()
        self.pushButton_enter_emotion.setText("课堂状态")
        self.pushButton_enter_emotion.setFixedSize(200, 60)
        self.verticalLayout.addWidget(self.pushButton_enter_emotion,0,2,1,1)

        # self.line_t = QtWidgets.QPushButton()
        # self.line_t.setText("")
        # self.verticalLayout.addWidget(self.line_t, 1, 0, 1, 1)
        # self.line_t.setGeometry(QtCore.QRect(0, 0, 900, 500))
        # self.line_t.setStyleSheet("border-bottom:2px solid #fc5531;")
        # self.pushButton_sign_out = QPushButton()
        # self.pushButton_sign_out.setText("退出登录")
        # self.pushButton_sign_out.setFixedSize(200, 300)
        # self.verticalLayout.addWidget(self.pushButton_sign_out,1,0,1,1)


        #人脸识别
        self.frame_distinguish = QFrame(self)
        self.frame_distinguish.setGeometry(QtCore.QRect(10, 120, 900, 500))
        self.verticalLayout_distinguish = QtWidgets.QGridLayout(self.frame_distinguish)

        self.import_pushButton = QPushButton()
        self.import_pushButton.setText("导入图片")
        self.import_pushButton.setFixedSize(170,50)
        self.verticalLayout_distinguish.addWidget(self.import_pushButton, 1, 0, 1, 1)

        self.cameraButton = QPushButton()
        self.cameraButton.setText("打开摄像头")
        self.cameraButton.setFixedSize(170,50)
        self.verticalLayout_distinguish.addWidget(self.cameraButton, 1, 1, 1, 1)

        self.sign_pushButton = QPushButton()
        self.sign_pushButton.setText("点击签到")
        self.sign_pushButton.setFixedSize(170,50)
        self.verticalLayout_distinguish.addWidget(self.sign_pushButton, 1, 2, 1, 1)

        self.situation_pushButton = QPushButton()
        self.situation_pushButton.setText("签到情况")
        self.situation_pushButton.setFixedSize(170,50)
        self.verticalLayout_distinguish.addWidget(self.situation_pushButton, 1, 3, 1, 1)

        self.out_pushButton = QPushButton()
        self.out_pushButton.setText("签到导出")
        self.out_pushButton.setFixedSize(170,50)
        self.verticalLayout_distinguish.addWidget(self.out_pushButton, 1, 4, 1, 1)

        self.cameraLabel = QtWidgets.QLabel()
        self.cameraLabel.setText("")
        self.verticalLayout_distinguish.addWidget(self.cameraLabel, 2, 1, 5, 3)
        self.cameraLabel.setMinimumSize(QtCore.QSize(600, 450))
        # self.cameraLabel.setStyleSheet("background-color: RoyalBlue ")

        #人脸录入
        self.frame_import = QFrame(self)
        self.frame_import.setGeometry(QtCore.QRect(10, 120, 900, 500))
        #调整控件改变button但是摄像头会有问题
        self.verticalLayout_import= QtWidgets.QGridLayout(self.frame_import)

        self.import_start_Button = QPushButton()
        self.import_start_Button.setText("打开摄像头")
        self.import_start_Button.setFixedSize(170,50)
        self.verticalLayout_import.addWidget(self.import_start_Button, 0, 1, 1, 1)

        self.import_newButton = QPushButton()
        self.import_newButton.setText("选择存储位置")
        self.import_newButton.setFixedSize(170,50)
        self.verticalLayout_import.addWidget(self.import_newButton, 0, 0, 1, 1)

        self.import_newdir = QPushButton()
        self.import_newdir.setText("创建文件夹")
        self.import_newdir.setFixedSize(170,50)
        self.verticalLayout_import.addWidget(self.import_newdir, 0, 2, 1, 1)

        self.import_savep = QPushButton()
        self.import_savep.setText("保存图片")
        self.import_savep.setFixedSize(170,50)
        self.verticalLayout_import.addWidget(self.import_savep, 0, 3,1, 1)

        #凑比例
        self.import_none = QPushButton()
        self.import_none.setText("")
        self.import_none.setFixedSize(170,50)
        self.verticalLayout_import.addWidget(self.import_none, 0, 4,1, 1)

        self.cameraLabel_import = QtWidgets.QLabel()
        self.cameraLabel_import.setText("")
        self.verticalLayout_import.addWidget(self.cameraLabel_import, 2, 1, 5, 3)
        self.cameraLabel_import.setMinimumSize(QtCore.QSize(600, 450))
        # self.cameraLabel_import.setStyleSheet("background-color: RoyalBlue ")

        #情感检测
        self.frame_emotion = QFrame(self)
        self.frame_emotion.setGeometry(QtCore.QRect(10, 120, 900, 500))
        #调整控件改变button但是摄像头会有问题
        self.verticalLayout_emotion= QtWidgets.QGridLayout(self.frame_emotion)

        self.emotion_newButton = QPushButton()
        self.emotion_newButton.setText("打开摄像头")
        self.emotion_newButton.setFixedSize(170,50)
        self.verticalLayout_emotion.addWidget(self.emotion_newButton, 0, 0, 1, 1)

        self.emotion_input = QPushButton()
        self.emotion_input.setText("当前课堂状态")
        self.emotion_input.setFixedSize(170,50)
        self.verticalLayout_emotion.addWidget(self.emotion_input, 0, 1, 1, 1)

        self.emotion_class = QPushButton()
        self.emotion_class.setText("平均课堂状态")
        self.emotion_class.setFixedSize(170,50)
        self.verticalLayout_emotion.addWidget(self.emotion_class, 0, 2, 1, 1)

        self.emotion_out = QPushButton()
        self.emotion_out.setText("课堂状态导出")
        self.emotion_out.setFixedSize(170,50)
        self.verticalLayout_emotion.addWidget(self.emotion_out, 0, 3, 1, 1)

        self.tired_none = QPushButton()
        self.tired_none.setText("")
        self.tired_none.setFixedSize(170,50)
        self.verticalLayout_emotion.addWidget(self.tired_none, 0, 4, 1, 1)

        self.cameraLabel_emotion = QtWidgets.QLabel()
        self.cameraLabel_emotion.setText("")
        self.verticalLayout_emotion.addWidget(self.cameraLabel_emotion, 2, 1, 5, 3)
        # self.cameraLabel_emotion.setGeometry(QtCore.QRect(0, 0, 600, 450))
        self.cameraLabel_emotion.setMinimumSize(QtCore.QSize(600, 450))
        # self.cameraLabel_emotion.setStyleSheet("background-color: RoyalBlue ")


        #退出登录
        self.frame_out = QFrame(self)
        self.frame_out.setGeometry(QtCore.QRect(780, 620, 100, 100))
        self.verticalLayout_out= QtWidgets.QGridLayout(self.frame_out)
        self.pushButton_sign_out = QPushButton()
        self.pushButton_sign_out.setText("退出登录")
        self.verticalLayout_out.addWidget(self.pushButton_sign_out,0,0,1,1)



        #显示页面
        self.frame_out.setVisible(False)
        self.frame.setVisible(False)
        self.frame_register.setVisible(False)
        self.frame_sign.setVisible(True)
        self.frame_import.setVisible(False)
        self.frame_emotion.setVisible(False)
        self.frame_distinguish.setVisible(False)
        self.pushButton_enter_distinguish.clicked.connect(self.on_pushButton_enter_distinguish_clicked)
        self.pushButton_enter_import.clicked.connect(self.on_pushButton_enter_import_clicked)
        self.pushButton_sign.clicked.connect(self.pushButton_sign_clicked)
        self.pushButton_sign_out.clicked.connect(self.pushButton_sign_out_clicked)
        self.pushButton_return_sign.clicked.connect(self.pushButton_return_sign_clicked)
        self.pushButton_register.clicked.connect(self.pushButton_register_clicked)
        self.pushButton_enter_emotion.clicked.connect(self.pushButton_enter_emotion_clicked)
        self.closs_pushButton.clicked.connect(self.close)  #关闭窗口
        self.mini_pushButton.clicked.connect(self.showMinimized)#最小化窗口
        self.retranslateUi(self)

    def retranslateUi(self, window):
        window.setWindowOpacity(1.0)  # 设置窗口透明度
        # Ui_MainWindow3.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        window.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        pe = QPalette()
        window.setAutoFillBackground(True)
        # pe.setColor(QPalette.Window, Qt.white)  # 设置背景色
        pe.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("1.png")))
        # pe.setColor(QPalette.Background,Qt.blue)
        window.setPalette(pe)

        self.closs_pushButton.setStyleSheet('''QPushButton{background:#F76677;border-radius:15px;}
        QPushButton:hover{background:red;}''')
        # background:  # F76677;border-radius:15px;
        self.pushButton_enter_import.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:32px;}
        QPushButton:hover{border-bottom:2px solid #fc5531;color:#fc5531;}''')
        self.pushButton_enter_distinguish.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:32px;}
        QPushButton:hover{border-bottom:2px solid #fc5531;color:#fc5531;}''')
        self.pushButton_enter_emotion.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:32px;}
        QPushButton:hover{border-bottom:2px solid #fc5531;color:#fc5531;}''')
        self.pushButton_sign_out.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:20px;}
        QPushButton:hover{color:#fc5531;}''')
        # self.max_pushButton.setStyleSheet('''QPushButton{background:#F7D674;border-radius:15px;}
        # QPushButton:hover{background:yellow;}''')
        self.mini_pushButton.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:15px;}
        QPushButton:hover{background:green;}''')
        self.import_none.setStyleSheet("QPushButton{border:none;}")
        self.import_newdir.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.import_savep.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.import_newButton.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.import_start_Button.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.import_pushButton.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.cameraButton.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.sign_pushButton.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.situation_pushButton.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.out_pushButton.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.emotion_newButton.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.emotion_input.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.emotion_out.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.emotion_class.setStyleSheet('''QPushButton{border:none;font-family:'楷体';font-size:25px;color:#848484;}
        QPushButton:hover{color:#f89504;}''')
        self.tired_none.setStyleSheet("QPushButton{border:none;}")



    def pushButton_enter_emotion_clicked(self):
        self.frame_import.setVisible(False)
        self.frame_distinguish.setVisible(False)
        # self.frame_sign.setVisible(False)
        self.frame_emotion.setVisible(True)

    def on_pushButton_enter_distinguish_clicked(self):
        self.frame_import.setVisible(False)
        self.frame_distinguish.setVisible(True)
        # self.frame_sign.setVisible(False)
        self.frame_emotion.setVisible(False)

    def on_pushButton_enter_import_clicked(self):
        self.frame_import.setVisible(True)
        self.frame_distinguish.setVisible(False)
        # self.frame_sign.setVisible(False)
        self.frame_emotion.setVisible(False)

    def pushButton_sign_clicked(self):
        self.frame_out.setVisible(True)
        self.frame.setVisible(True)
        self.frame_import.setVisible(True)
        self.frame_distinguish.setVisible(False)
        self.frame_sign.setVisible(False)
        self.frame_emotion.setVisible(False)

    def pushButton_sign_out_clicked(self):
        self.frame_out.setVisible(False)
        self.frame.setVisible(False)
        self.frame_import.setVisible(False)
        self.frame_distinguish.setVisible(False)
        self.frame_sign.setVisible(True)
        self.frame_emotion.setVisible(False)

    #注册
    def pushButton_register_clicked(self):
        self.frame_register.setVisible(True)
        # self.frame.setVisible(False)
        # self.frame_import.setVisible(False)
        # self.frame_distinguish.setVisible(False)
        self.frame_sign.setVisible(False)

    #返回登录
    def pushButton_return_sign_clicked(self):
        self.frame_register.setVisible(False)
        # self.frame.setVisible(False)
        # self.frame_import.setVisible(False)
        # self.frame_distinguish.setVisible(False)
        self.frame_sign.setVisible(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标


    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()


    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog = logindialog()
#     if dialog.exec_() == QDialog.Accepted:
#         sys.exit(app.exec_())
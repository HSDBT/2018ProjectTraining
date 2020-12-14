#导入文件夹(只能选择文件夹)
import os
import shutil

from PyQt5.QtWidgets import QMessageBox

def try_dir(new_dir,i):
    if os.path.isdir(new_dir):
        msg_box = QMessageBox(QMessageBox.Information, '提示', '存在同名文件夹' + i)
        msg_box.exec_()
    else:
        os.mkdir(new_dir)

def import_face_photo(path):
    new_path = './pic'
    label = 0
    for root, dirs, files in os.walk(path):
        if label == 0:
            if len(dirs) == 0:
                dir_list = path.split('/')
                new_dir = new_path + '/' + dir_list[-1]
                try_dir(new_dir,dir_list[-1])
                for i in range(len(files)):
                    # 匹配想要复制转移的文件类型
                    file_path = root + '/' + files[i]
                    # print(file_path)
                    new_file_path = new_dir + '/' + files[i]
                    # print(new_file_path)
                    shutil.copy(file_path, new_file_path)
                return 0
            else:
                for i in dirs:
                    new_dir = new_path + '/' + i
                    try_dir(new_dir,i)
            label = 1
        for i in range(len(files)):
            f_len = root.index('\\')
            # 匹配想要复制转移的文件类型
            file_path = root + '/' + files[i]
            new_file_path = new_path + '/' + root[f_len + 1:] + '/' + files[i]
            shutil.copy(file_path, new_file_path)

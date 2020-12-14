
import os
import shutil
#导入文件夹(只能选择文件夹)
def import_face_photo(dir):
    new_path = 'D:/1'
    for root, dirs, files in os.walk(dir):
        # print(root,dirs,files)
        for i in range(len(files)):
            #以点拆分文件名
            f_len = files[i].index('.')
            #文件夹内图片
            photo_path = root + '/' + files[i]
            #新创建文件夹路径
            new_fold_dir = new_path + '/' + files[i][:f_len]
            print(new_fold_dir)
            #创建新文件夹
            os.mkdir(new_fold_dir)
            #要复制到的路径
            new_file_path = new_fold_dir + '/' + files[i]
            print(new_file_path)
            print(photo_path)
            # shutil.copy(photo_path, new_file_path)#正确
            shutil.copy(photo_path, new_fold_dir)#测试


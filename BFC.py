# -*- coding: utf-8 -*-
import hashlib
import os
import re
import shutil
import sys
import urllib
import urllib.request
import uuid
import oss2
import json

# 设置程序默认保存OSS服务器
# 阿里云账号AccessKey
auth = oss2.Auth('LTAI5tNBPod5nzCmcBPPRFjA', 'tQrxJUkhgu3KX1KraPBP2lZSmjoAZL')
# yourEndpoint填写Bucket所在地域对应的Endpoint。Endpoint填写为https://oss-cn-chengdu.aliyuncs.com
# 填写Bucket名称。
bucket = oss2.Bucket(auth, 'https://oss-cn-chengdu.aliyuncs.com', 'ffxivconfig')


# 压缩用户数据 输出对应用户ID为文件名的压缩包
def gen_zipfile(user_id, user_dir):
    shutil.make_archive(user_id, 'zip', user_dir)


# 用户压缩后数据包大小检查   返回：Ture，大小合格，允许上传；False，文件过大或不存在，报错
def check_size(urlin):
    file_size = os.path.getsize(urlin)
    file_size_mb = file_size / float(10240)
    if file_size_mb >= 10:
        return False
    elif file_size_mb == 0:
        return False
    elif file_size_mb <= 10:
        return True


# 获取json
def get_online_json(url):
    resp = urllib.request.urlopen(url)
    bfc_json = json.loads(resp.read())
    return bfc_json


# 获取欢迎信息
def welcome():
    welcome_data = get_online_json("https://portal.iinformation.info/bfc/welcom.json")
    help_len = int(len(welcome_data["Help"]))
    print("*" * 50)
    print(welcome_data["Title"])
    print("*" * 50)
    print("使用前您需要了解以下内容：")
    for i in range(help_len):
        print(welcome_data["Help"][i])
    print("公告如下：")
    for i in range(help_len):
        print(welcome_data["Announcement"][i])


# 用户ID获取
def get_user_id():
    key_exists = os.path.exists(os.getcwd() + "\\key.txt")
    if key_exists is False:
        return gen_user_id()
    else:
        with open("key.txt", "r") as f:
            user_id = f.readline()
            return user_id


# 获得唯一ID
def gen_user_id():
    # 利用sha256(uuid1())生成唯一用户ID
    user_id = hashlib.sha256(str(uuid.uuid1()).encode('utf-8')).hexdigest()
    with open("key.txt", "w") as f:
        f.write(user_id)
    return user_id


# 用户ID 返回用户需要使用的用户ID
def login():
    userid = get_user_id()
    print("*" * 50)
    print("您当前设备的备份密钥为：", userid)
    print("*" * 50)
    print("您是否需要更换密钥？不正确的密钥会导致云端备份文件夹匹配失败")
    print("0：不更换 ；1：更换")
    print("*" * 50)
    print("请输入您的选择：")
    key_change = input()
    print("*" * 50)
    # 进行密钥输出
    if key_change is "1":
        user_id = input("请输入您的密钥：")
        print("*" * 50)
    elif key_change is "0":
        print("您将使用以下密钥完成备份还原操作：", userid)
        print("\033[1;31m请收藏本密钥便于今后使用，密钥已同时备份至本程序目录下的key.txt中\033[0m")
        print("\033[1;32m若您需要修改已保存的密钥，请手动编辑本程序目录下的key.txt\033[0m")
        print("*" * 50)
        user_id = userid
    else:
        print("输入有误，请重新运行本程序。")
        user_id = "Error"

    return user_id


# 校验用户ID 请 check_user_id(login()) 以确保用户使用了合法的ID
def check_user_id(user_id):
    lower_regex = re.compile("[a-z]")
    digit_regex = re.compile("[0-9]")
    wrong_regex = re.compile("[^a-zA-Z0-9]")

    while True:
        if len(user_id) < 64:
            print('密钥格式有误，请勿乱输入密钥！或删除key.txt文件重试！')
            sys.exit(0)
        elif wrong_regex.search(user_id) is not None:
            print('密钥包含无效字符，请重新粘贴或删除key.txt文件重试！')
            sys.exit(0)
        else:
            if lower_regex.search(user_id) is None:
                print('密钥格式有误，请勿乱输入密钥！或删除key.txt文件重试！')
                sys.exit(0)
            elif digit_regex.search(user_id) is None:
                print('密钥格式有误，请勿乱输入密钥！或删除key.txt文件重试！')
                sys.exit(0)
            else:
                print('密钥校验成功')
                print("*" * 50)
                return user_id


# 上传文件
def upload_config(file_name, file_path):
    bucket.put_object_from_file(file_name, file_path)
    print("*" * 50)
    print("文件备份完成，上传缓存将在稍后删除。")
    print("*" * 50)
    os.remove(file_path)


# 进度条
def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()


# 下载文件
def download_config(user_id):
    cdn_data = get_online_json("https://portal.iinformation.info/bfc/welcom.json")
    download_url = cdn_data["ConfigCDN"] + "XIVConfig/" + user_id + "/" + user_id + ".zip"
    urllib.request.urlretrieve(download_url, "FFXIVConfig.zip")

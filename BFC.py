# -*- coding: utf-8 -*-
import hashlib
import os
import re
import urllib.request
import zipfile
import uuid
import oss2
import json


# 压缩用户数据


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


# 获得本机用户ID
def gen_user_id():
    user_id = hashlib.sha256(str(uuid.uuid1()).encode('utf-8')).hexdigest()
    # 利用sha256(uuid1())生成唯一用户ID
    # user_id 用于后续用户文件夹建立，并不保证用户文件夹安全性。My Games文件夹也不需要保证安全性。
    return user_id


# 用户ID
def login():
    print("*" * 50)
    print("您当前设备的备份密钥为：", gen_user_id())
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
        print("您将使用以下密钥完成备份还原操作：", gen_user_id())
        print("*" * 50)
        user_id = gen_user_id()
    else:
        print("输入有误，请重新运行本程序。")
        user_id = "Error"

    return user_id


# 校验用户ID
def check_user_id(user_id):
    lower_regex = re.compile("[a-z]")
    digit_regex = re.compile("[0-9]")
    wrong_regex = re.compile("[^a-zA-Z0-9]")

    while True:
        if len(user_id) < 64:
            print('密钥格式有误，请勿乱输入密钥！')
            break
        elif wrong_regex.search(user_id) is not None:
            print('密钥包含无效字符，请重新粘贴')
            break
        else:
            if lower_regex.search(user_id) is None:
                print('密钥格式有误，请勿乱输入密钥！')
                break
            elif digit_regex.search(user_id) is None:
                print('密钥格式有误，请勿乱输入密钥！')
                break
            else:
                print('密钥校验成功')
                print("*" * 50)
                return user_id


welcome()
# check_user_id(login())

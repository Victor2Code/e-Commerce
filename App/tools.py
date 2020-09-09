#! /usr/bin/env python
# -*- coding: utf-8 -*- 
# @author: xiaofu
# @date: 2020-Sep-08
import base64
import hashlib
import time


def my_password_generator(password: str) -> str:
    """先求md5，然后将时间戳添加到行首，用特定字符隔开，最后对整体进行base64编码"""
    str_after_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()  # 变量类型为str
    timestamp = time.time()
    whole_str = str(timestamp) + '#' + str_after_md5
    str_after_base64 = base64.b64encode(whole_str.encode('utf-8')).decode('utf-8')
    return str_after_base64


def my_password_checker(password: str, string: str) -> bool:
    """base64反编码以后提取出md5值，和密码的md5进行比较是否相同"""
    str_after_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    str_from_string = base64.b64decode(string.encode('utf-8')).decode('utf-8').split('#')[1]
    return str_after_md5 == str_from_string
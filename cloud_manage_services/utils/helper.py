"""
    File Name  : helper.py
    Created on : 2020/3/10
    Author     : mxm
"""
import datetime
import json
import os
import platform
import random
import re
import requests
import time
import uuid


def utc_2_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S.%fZ'):
    """
    utc时间转本地时间
    :param utc_time_str:
    :param utc_format:
    :return:
    """
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    if '.' in utc_time_str:
        utc_st = datetime.datetime.strptime(utc_time_str, utc_format)
    else:
        utc_st = datetime.datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
    local_st = utc_st + offset
    return local_st


def local_2_utc(local_st):
    """
    本地时间转换为utc时间
    :param local_st:
    :return:
    """
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st


def str_2_int(data, default=0):
    if data.isdigit():  # 判断字符串是否是数字组成
        return default if data is None or len(data) == 0 else int(data)
    else:
        return '字符串不是由数字组成，不能转换成整数类型'


def make_captcha(size=6):
    """
    生成验证码，默认生成6位的验证码，其中元素包括大小写字母，数字
    """
    code = ""
    for i in range(size):
        c_max = chr(random.randint(65, 90))
        c_min = chr(random.randint(97, 122))
        num = str(random.randint(0, 9))
        code += random.choice([c_max, c_min, num])
    return code


def check_time_validity(value):
    """
    检查时间的有效性
    :param value:时间字符串
    :return:
    """
    try:
        if "-" in value and ":" in value:
            time.strptime(value, "%Y-%m-%d %H:%M:%S")
        elif "-" in value:
            time.strptime(value, "%Y-%m-%d")
        elif "/" in value and ":" in value:
            time.strptime(value, "%Y/%m/%d %H:%M:%S")
        elif "/" in value:
            time.strptime(value, "%Y/%m/%d")
        elif ":" in value:
            time.strptime(value, "%Y%m%d %H:%M:%S")
        else:
            time.strptime(value, "%Y%m%d")
    except Exception as e:
        raise Exception("Not conform to the Date specification,"
                        " Example: 20171111; 20171111 11:11:11"
                        " 2017-11-11; 2017-11-11 11:11:11; "
                        " 2017/11/11; 2017/11/11 11:11:11; ")
    return value


def str_to_obj(params):
    """
    字符串转json
    :param params:
    :return:
    """
    try:
        params = params.replace("'", '"')
        return json.loads(params)
    except Exception as e:
        raise Exception("118 Not conform to the JSON specification %s" % e)


def obj_to_str(params):
    """
    json转字符串
    :param params:
    :return:
    """
    try:
        return json.dumps(params)
    except Exception as e:
        raise Exception("130 Not conform to the JSON specification %s" % e)


def check_file_type(filename, file_type):
    """
    检查文件类型
    :param filename:
    :param file_type:
    :return:
    """
    fileTypeList = {
        'image': [".png", ".jpg", ".jpeg", ".gif", ".JPG", ".JPEG"],
        'excel': [".xls", "xlsx"],
        'world': [".doc", ".docx"],
        'text': [".txt"],
        'json': [".json"],
        'csv': [".csv"],
        'markdown': [".md"],
        'ppt': [".ppt", ".pptx"],
        'pdf': [".pdf"],
        'Hypertext': [".htm", ".html"],
        'CompressedFile': [".gz", ".rar", ".tar", ".zip"]
    }
    name, suffix = os.path.splitext(filename)
    return suffix in fileTypeList.get(file_type, [])


def make_file_name(file_type='txt'):
    """
    生成文件名称
    :param file_type:
    :return:
    """
    value = str(uuid.uuid1()).replace('-', '')
    return value[:24]


def str2int(data, default=0):
    """
    将字符串转换为整数
    :param data:
    :param default:
    :return:
    """
    return int(data) if data.isdigit() else default


def paging(data_list, page_number, page_size):
    """
    分页
    :param data_list:
    :param page_number:
    :param page_size:
    :return:
    """
    if page_number == 'all':
        data_list = data_list.all()
    elif page_number == 'first':
        data_list = data_list.first()
    else:
        page_index = str2int(page_number, 1)
        page_size = str2int(page_size, 10)
        begin_index = (page_index - 1) * page_size
        end_index = begin_index + page_size
        data_list = data_list.all()[begin_index: end_index]
    return data_list

def isWindows():
    """
    如果pigtail名称中有 win，则认为是Windows平台
    :return:
    """
    platform_system = platform.system().lower()
    return platform_system.find("win") >= 0


def getIP():
    """
    获取本机公网IP
    :return:
    """
    url = requests.get("http://txt.go.sohu.com/ip/soip")
    text = url.text
    return re.findall(r'\d+.\d+.\d+.\d+', text)[0]


if __name__ == '__main__':
    res = getIP()
    print(res)

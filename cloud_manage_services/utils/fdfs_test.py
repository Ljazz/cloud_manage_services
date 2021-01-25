"""
    File Name       : fdfs_test.py
    Description     ：
    Author          : mxm
    Created on      : 2020/7/13
"""
from fdfs_client.client import *
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_system.settings')
from django.conf import settings
import time

tracker_path = get_tracker_conf(os.path.join(settings.BASE_DIR, 'static', 'config', 'client.conf'))
client = Fdfs_client(tracker_path)

if __name__ == '__main__':
    try:
        ret = client.upload_by_filename('helper.py')
        print('ret: ', ret)
        remote_file_id = ret['Remote file_id']
        print('Remote file_id: ', remote_file_id)
        remote_file_id = remote_file_id.decode("utf-8").replace('\\', '/')
        print('Remote file_id after decode: ', remote_file_id)
        name = ret['Local file name']
        print('Local file name: ', name)
        size = ret['Uploaded size']
        print('Uploaded size: ', size)
        storage_ip = ret['Storage IP']
        print('Storage IP: ', storage_ip)
        storage_ip = storage_ip.decode("utf-8")
        print('Storage IP after decode: ', storage_ip)

        remote_file_id = bytes(remote_file_id, encoding='utf-8')
        ret_download = client.download_to_buffer(remote_file_id)
        print('download result: ', ret_download)
        with open(os.path.join(settings.BASE_DIR, 'static', 'download', name), 'wb') as f:
            f.write(ret_download['Content'])
        # res = client.download_to_file('download.jpg', remote_file_id)
        # time.sleep(5)
        # print('download file: ', res)

        ret_delete = client.delete_file(remote_file_id)
        print(ret_delete)
    except Exception as e:
        print('error'+str(e))
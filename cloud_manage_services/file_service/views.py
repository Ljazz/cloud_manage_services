from django.conf import settings
from utils.apiview import GomAPIView
from fdfs_client.client import *
from pathlib import Path
from .models import FileService

tracker_path = get_tracker_conf(Path.joinpath(settings.BASE_DIR, 'static', 'config', 'client.conf'))
client = Fdfs_client(tracker_path)


class FileUpload(GomAPIView):
    """
    文件上传
    """
    def victim(self):
        fileBuffer = self.request.FILES.get('file', None)

        file_name = fileBuffer.name  # 获取文件名称
        file_ext_name = Path(fileBuffer).suffix[1:]
        # 对上传文件的后缀名作出判断     前端需要对文件后缀进行判断
        if file_ext_name not in ['jpg', 'png', 'gif']:
            self.code = 500
            self.result = '选择图片类型不正确!'
            return

        try:
            ret = client.upload_by_buffer(fileBuffer.read(), file_ext_name)
            if ret.get('Status') != 'Upload successed.':
                # 上传失败
                raise Exception('上传文件失败!')

            remote_file_id = ret['Remote file_id'].decode("utf-8").replace('\\', '/')
            url = settings.FILE_SERVER_ADDR + remote_file_id
            file_name = ret['Local file name'] if file_name is None else file_name
            file = FileService(
                name=file_name,
                path=url,
                type=file_ext_name.upper(),
                size=ret['Uploaded size']
            )
            file.save()
            self.code = 200
            self.data = {'link': url, 'id': file.id, 'name': file_name}
            self.result = '文件上传成功'
        except Exception as e:
            self.code = 404
            self.result = e


class FileDownLoad(GomAPIView):
    """
    文件下载
    """
    def victim(self):
        file_id = self.data_dict.get('file_id')
        file = FileService.objects.filter(id=file_id).first()
        remote_fileid = bytes(file.url.replace(settings.FILE_SERVER_ADDR, '').encode('utf-8'))
        ret_download = client.download_to_buffer(remote_fileid)
        with open(os.path.join(settings.BASE_DIR, 'static', 'download', 'file', file.name), 'wb') as f:
            f.write(ret_download['Content'])
        self.code = 200
        self.result = '文件下载成功！'


class FileDelete(GomAPIView):
    """
    文件删除
    """
    def victim(self):
        ids = self.data_dict.get('file_ids')
        files = FileService.objects.filter(id__in=ids)
        remote_fileid_list = [{
            item.name: bytes(item.url.replace(settings.FILE_SERVER_ADDR, '').encode('utf-8'))
        } for item in files]
        for item in remote_fileid_list:
            try:
                for key, value in item.items():
                    ret_delete = client.delete_file(value)
                    if ret_delete[0] != 'Delete file successed.':
                        raise Exception('{}删除失败！'.format(key))
            except Exception as e:
                self.code = 404
                self.result = e
        self.code = 200
        self.result = '文件删除成功'

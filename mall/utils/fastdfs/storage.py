from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.utils.deconstruct import deconstructible
from mall import settings


@deconstructible
class FastDFSStorage(Storage):
    """
    自定义文件上传类
    """
    def __init__(self, ip=None, conf_path=None):
        self.ip = ip
        self.conf_path = conf_path
        if not ip:
            self.ip = settings.FDFS_URL
        if not conf_path:
            self.conf_path = settings.FDFS_CLIENT_CONF

    def _open(self, name, model='rb'):
        pass

    def _save(self, name, content, max_length=None):
        client = Fdfs_client(self.conf_path)
        if not max_length:
            file_data = content.read()
        else:
            file_data = bytes()
            while True:
                part_data = content.read(max_length)
                if part_data:
                    file_data += part_data
                else:
                    break
        result = client.upload_by_buffer(file_data)
        if result.get('Status') == 'Upload successed.':
            return result.get('Remote file_id')
        else:
            raise Exception('图片上传失败')

    def exists(self, name):
        return False

    def url(self, name):
        return self.ip + name

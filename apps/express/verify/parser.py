import os
import urllib
from PIL import Image
import numpy as np
from django.conf import settings


class BaseParser(object):
    code_ext = 'jpg'
    code_url = None
    file_path = None

    def __init__(self):
        filename = '%s.%s' % (self.__class__.__name__, self.code_ext)
        self.file_path = self.get_file_path(filename)

    def get_file_path(self, filename):
        return os.path.join(settings.TEMP_ROOT, filename)

    def get_code(self, url):
        """download and load verify code"""
        if not url:
            raise

        if not os.path.exists(settings.TEMP_ROOT):
            os.makedirs(settings.TEMP_ROOT)

        urllib.urlretrieve(self.code_url, self.file_path)
        img = Image.open(self.file_path)
        return img

    def run(self, url=None):
        """parser entry"""
        url = url or self.code_url
        img = self.get_code(url)

        result = self.verify(img)
        img.close()

        if not result:
            err_file_name = '%s.err.%s' % (self.__class__.__name__, self.code_ext)
            err_file_path = self.get_file_path(err_file_name)
            os.rename(self.file_path, err_file_path)
        else:
            files = os.listdir(settings.TEMP_ROOT)
            for f in files:
                if f.startswith('%s.done' % self.__class__.__name__):
                    os.remove(os.path.join(settings.TEMP_ROOT, f))
            done_file_name = '%s.done.%s.%s' % (self.__class__.__name__, result, self.code_ext)
            done_file_path = self.get_file_path(done_file_name)
            os.rename(self.file_path, done_file_path)

        return result

    def verify(self, img):
        """recognise verify code from image"""
        raise NotImplementedError

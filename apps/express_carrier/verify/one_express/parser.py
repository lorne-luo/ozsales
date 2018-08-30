from PIL import Image
import numpy as np

from ..parser import BaseParser


class OneExpressParser(BaseParser):
    code_ext = 'png'
    code_url = 'http://www.one-express.cn/index.php/app/Index/verify'

    def verify(self, img):
        # load character models
        model_numbers = [8, 9, 3, 0, 2, 4, 6, 5, 7, 1]
        models = {}
        for i in model_numbers:
            models.update({i: Image.open('./apps/express_carrier/verify/one_express//model/%s.bmp' % i)})

        result = []
        imgArr = np.asarray(img)
        data = np.transpose(imgArr, (1, 0, 2))

        width, height = img.size
        x = 0
        while x < width:
            for y in range(height):
                for number in model_numbers:
                    if self.check_model(width, height, data, x, y, models[number]):
                        result.append(number)
                        x = x + models[number].size[0]
                        y = 0
                        break
            x += 1

        code = ''.join([str(x) for x in result])
        return code

    def check_model(self, width, height, img, x, y, model):
        """compare block on code image with number model"""
        model_w, model_h = model.size
        total = model_w * model_h
        max_miss = 1
        miss_match = 0
        model_px = model.load()

        if width - model_w < x or height - model_h < y:
            return False

        for i in range(model_w):
            for j in range(model_h):
                xx = x + i
                yy = y + j
                if not model_px[i, j] or img[xx, yy] == [100, 100]:
                    continue

                value = sum(img[xx, yy]) / 3 < 128
                if not value:
                    miss_match += 1
                    if miss_match >= max_miss:
                        return False
        return True

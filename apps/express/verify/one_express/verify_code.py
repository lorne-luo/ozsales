import os
from PIL import Image
import numpy as np


# import matplotlib.pyplot as plt

def test():
    name_tpl = "./verify/code/%s.png"
    for i in range(100):
        file_path = name_tpl % (i + 1)
        if os.path.exists(file_path):
            code = main(file_path)
            new_path = name_tpl % code
            os.rename(file_path, new_path)


def main(file):
    model_number = [8, 9, 3, 0, 2, 4, 6, 5, 7, 1]
    models = [Image.open('./verify/model/%s.bmp' % i) for i in model_number]

    result = []

    img = Image.open(file)  # open colour image
    # img = img.convert('L')  # convert image to monochrome - this works

    THRESHOLD_VALUE = 120
    imgData = np.asarray(img)
    data2 = np.transpose(imgData, (1, 0, 2))

    # thresholdedData = (data2 > THRESHOLD_VALUE) * 1.0

    width, height = img.size

    x = 0
    while x < width:
        for y in range(height):
            for m in range(len(models)):
                if check_model(width, height, data2, x, y, models[m], m):
                    result.append(m)
                    x = x + models[m].size[0]
                    y = 0
                    break
        x += 1

    code = ''.join([str(x) for x in result])
    print(code)
    return code

    # plt.imshow(thresholdedData)
    # plt.show()

    d = np.asarray(thresholdedData)

    Image.fromarray(d)


def check_model(width, height, img, x, y, model, number):
    model_w, model_h = model.size
    total = model_w * model_h
    max_miss = int(total * 0.08)
    miss_match = 0
    model_px = model.load()

    if width - model_w < x or height - model_h < y:
        return False

    for i in range(model_w):
        for j in range(model_h):
            if not model_px[i, j]:
                continue
            xx = x + i
            yy = y + j
            value = sum(img[xx, yy]) / 3 < 90
            if not value:
                miss_match += 1
                if miss_match >= max_miss:
                    return False
    return True

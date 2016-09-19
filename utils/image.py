import os
from PIL import Image, ImageOps
from wand.image import Image as WandImage
from StringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage


def resize(file, width=0, height=0, crop=0):
    """ resize jpg png and gif """
    width = int(width)
    height = int(height)
    crop = int(crop)

    if isinstance(file, str):
        file = open(file)

    if width == 0 and height == 0:
        return file

    width = 9999 if width is 0 else width
    height = 9999 if height is 0 else height

    temp = StringIO()

    filename, ext = os.path.splitext(file.name)
    ext = ext.strip('.')
    if ext == 'gif':
        with WandImage(file=file) as img:
            if crop == 1:
                width = width if width < img.width else img.width
                height = height if height < img.height else img.height
                img.crop(width=width, height=height, gravity='center')
            else:
                img.resize(width, height)
            img.save(file=temp)
    else:
        with Image.open(file) as image:
            if crop == 1:
                width = width if width < image.width else image.width
                height = height if height < image.height else image.height
                image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
            else:
                image.thumbnail((width, height), Image.ANTIALIAS)

            image.save(temp, ext)

    temp.seek(0)
    return SimpleUploadedFile(file.name,
                              temp.read(),
                              content_type='image/%s' % ext)

    # obj.filefield=SimpleUploadedFile
    # obj.save()


def resize_to_file(src, dst, width=0, height=0, crop=0):
    file = open(src)
    content = resize(file, width, height, crop)
    default_storage.save(dst, content)

import base64
import os
import zlib
import time
from PIL import Image


def imageToStr(image):
    with open(image, 'rb') as f:
        image_byte = base64.b64encode(f.read())
    image_str = image_byte.decode('ascii')
    return image_str


def strToImage(str, filename):
    image_str = str.encode('ascii')
    image_byte = base64.b64decode(image_str)
    image_json = open(filename, 'wb')
    image_json.write(image_byte)  # 将图片存到当前文件的fileimage文件中
    image_json.close()


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024


def get_outfile(infile, outfile=''):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}_out{}'.format(dir, suffix)
    return outfile


# def compress_image(infile, outfile='', mb=150, step=10, quality=80):
#     """不改变图片尺寸压缩到指定大小
#     :param infile: 压缩源文件
#     :param outfile: 压缩文件保存地址
#     :param mb: 压缩目标，KB
#     :param step: 每次调整的压缩比率
#     :param quality: 初始压缩比率
#     :return: 压缩文件地址，压缩文件大小
#     """
#     o_size = get_size(infile)
#     if o_size <= mb:
#         return infile
#     outfile = get_outfile(infile, outfile)
#     while o_size > mb:
#         im = Image.open(infile)
#         im.save(outfile, quality=quality)
#         if quality - step < 0:
#             break
#         quality -= step
#         o_size = get_size(outfile)
#     return outfile, get_size(outfile)


def resize(infile, limit):
    """缩放图片尺寸
    infile: 压缩源文件
    limit: 长或宽的最大像素个数
    return: 图片是否压缩
    """
    img = Image.open(infile)
    scale = 1
    flag = False
    w, h = img.size
    if w > limit or h > limit:
        scale = max(w / limit, h / limit)
        flag = True
    Img = img.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
    Img.save(get_outfile(infile))
    return flag


if __name__ == '__main__':
    time1 = time.time()
    path = "/mnt/d/vscode/Flower_app/server/image/user_image"
    filename1 = "/line.jpg"
    filename2 = "/default_out.jpg"
    # compress_image(path + filename1, mb=3)
    resize(path + filename1, 400)
    time2 = time.time()
    print('总共耗时：' + str(time2 - time1) + 's')

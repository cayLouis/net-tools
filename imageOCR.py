from PIL import Image
import pytesseract
import urllib.request
import os
from collections import defaultdict

pytesseract.pytesseract.tesseract_cmd = 'D://tesseract/tesseract.exe'

#获取图片阈值
def get_thershold(image):
    #用来记录各个像素出现的次数
    pixel_dict = defaultdict(int)
    #获取图片中的行和列
    rows, cols = image.size
    #统计像素出现的个数
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i,j))
            pixel_dict[pixel]+=1
    #获取像素出现最频繁的次数
    count_max = max(pixel_dict.values())
    #用次数作为键,反转原序列
    pixel_dict_reverse = {v:k for k,v in pixel_dict.items()}
    #返回阈值
    return pixel_dict_reverse[count_max]

#获取灰度转二值映射表
def get_convert_table(threshold):
    table = []
    rate = 0.1
    for i in range(256):
        #在threshold的适当范围内进行处理
        if threshold*(1-rate)<= i <=threshold*(1+rate):
            table.append(1)
        else:
            table.append(0)

    return table

#用于消除噪声
def cut_noise(image):
    #获取图片的高度和宽度
    rows, cols = image.size
    #记录噪声的位置
    change_pos = []
    #遍历图片中的每一个像素点，除去边缘部分
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            pixel_set = []
            for m in range(i-1, i+2):
                for n in range(j-1, j+2):
                    if image.getpixel((m,n)) == 0:
                        pixel_set.append(image.getpixel((m,n)))
            #如果像素点附近的黑色像素数量小于等于4，则记录下这个位置
            if len(pixel_set)<=4:
                change_pos.append((i,j))
    #对相应的位置进行像素修改，去除噪声
    for pos in change_pos:
        image.putpixel(pos, 1)
    #返回消除噪声后的图片
    return image

#用于识别图片中的数字加上字母
def OCR_img(img_path):
    #打开指定路径的图片
    image = Image.open(img_path)
    #转化为灰度图像
    image_convert= image.convert("L")
    #获取图像阈值
    max_pixel = get_thershold(image_convert)
    #根据阈值获取映射表
    table = get_convert_table(max_pixel)
    #根据映射表修改像素
    out_image = image_convert.point(table, '1')
    #消除图片中的噪声
    out = cut_noise(out_image)
    #识别图像中的字符
    text = pytesseract.image_to_string(out)
    #去除识别结果中的特殊字符
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'

    text = "".join([x for x in text if x not in exclude_char_list])
    #输出识别识别出来的验证码
    print(text)

def OCR_img_url(url):
    #从url中得到图片的名称
    imagename = url.split('/')[-1].split("=")[-1]
    #创建请求
    req = urllib.request.Request(url)
    #添加请求头部
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
    response = urllib.request.urlopen(req).read()
    #下载图片
    with open(imagename, "wb+") as f:
        f.write(response)
    #识别验证码
    OCR_img(imagename)
    #删除缓存的图片
    if os.path.exists(imagename):
        os.remove(imagename)
    else:
        print("缓存的图片不存在")


OCR_img_url("https://image-static.segmentfault.com/305/714/3057140151-5b1cb26de365c")













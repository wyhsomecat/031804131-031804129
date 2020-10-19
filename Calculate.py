from PIL import Image
import math
import operator
from functools import reduce
import os
import base64

# 这里的img承载了赛题方面的base64测试图像，对其解码、保存
img = ''
imgdata = base64.b64decode(img)
file = open('aitest.jpg', 'wb')
file.write(imgdata)
file.close()


# 比较两张图片的异同
def image_contrast(img1, img2):
    image1 = Image.open(img1)
    image2 = Image.open(img2)

    h1 = image1.histogram()
    h2 = image2.histogram()
    # 比较两张图片的像素距离，如果两张图片完全相同则result=0，差距越多result越大
    result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return result


# 将图像切割成3*3块正方形图像的函数
def splitimage(src, rownum, colnum, dstpath):
    img = Image.open(src)
    w, h = img.size  # 图片大小
    if rownum <= h and colnum <= w:
        print('original image info:%sx%s,%s,%s' % (w, h,
                                                   img.format, img.mode))
        print('开始处理图片切割，请稍候-')
        s = os.path.split(src)
        if dstpath == '':  # 没有输入路径
            dstpath = s[0]  # 使用源图片所在目录s[0]
        fn = s[1].split('.')  # s[1]是源图片文件名
        basename = fn[0]  # 主文件名
        ext = fn[-1]  # 扩展名
        num = 0
        rowheight = h // rownum
        colwidth = w // colnum
        for r in range(rownum):
            for c in range(colnum):
                box = (c * colwidth, r * rowheight, (c + 1) * colwidth, (r + 1) * rowheight)
                img.crop(box).save(os.path.join(dstpath, basename + '' + str(num) + '.' + ext))
                num = num + 1
        print('图片切割完毕，共生成%s张小图片。' % num)
    else:
        print('不合法的行列切割参数！')


# 以测试图像为目标进行切割
src = 'aitest.jpg'
if os.path.isfile(src):
    dstpath = ''
    if (dstpath == '') or os.path.exists(dstpath):
        row = 3
        col = 3
        splitimage(src, row, col, dstpath)
    else:
        print('图片输出目录%s不存在！' % dstpath)
else:
    print('图片文件%s不存在!' % src)

# 创建字符串piclist，用来存储测试图像对应的位置序列
piclist = ''
# 创建两个元组，对应切割图像中的纯黑或纯白方块，备用
tup1 = (255, 255, 255)
tup2 = (0, 0, 0)
#设置一个boolean变量判断是否有纯黑方块
blackblock = False
for i in range(9):
    #读取切割测试图像后的小方块
    img = Image.open("aitest" + str(i) + ".jpg")
    imgstr = "aitest" + str(i) + ".jpg"
    clrs = img.getcolors()#img.getcolors方法会返回数个列表，每个列表里包含图像内某种颜色的像素点数量和RGB向量，分别以元组的方式储存于列表中

    if (len(clrs) != 1):#如果长度不为1，即不只返回了一个列表，即图像方块内有超过一种颜色（非纯黑或纯白）
        file_names = []
        #调用已经切割好的本地图片库
        for parent, dirnames, filenames in os.walk('D:/char/charspec'):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            file_names = filenames
        for k in range(315):
            #比较切割后的测试图像和本地图片库
            if (image_contrast(imgstr, 'D:/char/charspec/' + file_names[k]) == 0):
                tempfn = file_names[k]
                if (len(tempfn) > 8):#根据图片名称长度进行分类
                    #获取picname，即测试图像对应本地图像的名称，如A _(2)
                    picname = tempfn[0:6]
                    #print(tempfn[0:6])
                    num = int(tempfn[6]) + 1
                    #由于图片库内切割图片都是按顺序排列的（从0到8），获得其名称后缀就是获得了切割图片在原图片内对应的位置
                    piclist = piclist + str(num)
                    # print(piclist)
                else:
                    # print(tempfn[0:2])
                    picname = tempfn[0:2]
                    # print(tempfn[2])
                    num = int(tempfn[2]) + 1
                    piclist = piclist + str(num)
            k = k + 1

    #如切割图像是纯白块，将其列表代号确定为0
    elif (clrs[0][1] == tup1):
        piclist = piclist + '0'
    #如切割图像是纯黑块，先将其列表代号表示为t
    elif (clrs[0][1] == tup2):
        piclist = piclist + 't'
        tmp = i
        blackblock = True
        # print('你这个黑块能把人烦死',tmp)
    i = i + 1

#在获得了测试图像对应的本地图像的名称后重新遍历本地图片库，确定纯黑块的对应位置
for m in range(9):
    if (len(tempfn) > 8 and blackblock == True):
        if (image_contrast("aitest" + str(tmp) + ".jpg", 'D:/char/charspec/' + tempfn[0:6] + str(m) + '.jpg') == 0):
            strm = str(m + 1)
            # print(strm)
            piclist = piclist.replace('t', strm)
    elif (len(tempfn) < 8 and blackblock == True):
        if (image_contrast("aitest" + str(tmp) + ".jpg", 'D:/char/charspec/' + tempfn[0:2] + str(m) + '.jpg') == 0):
            strm = str(m + 1)
            # print(strm)
            piclist = piclist.replace('t', strm)
#获得piclist，piclist表示为一个九个数字的字符串
print(piclist)

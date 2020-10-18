from PIL import Image
import math
import operator
from functools import reduce
import os
import base64

#这里的img承载了赛题方面的base64测试图像，对其解码、保存
img = ''
imgdata =base64.b64decode(img)
file = open('aitest.jpg', 'wb')
file.write(imgdata)
file.close()

#比较两张图片的异同
def image_contrast(img1, img2):

    image1 = Image.open(img1)
    image2 = Image.open(img2)

    h1 = image1.histogram()
    h2 = image2.histogram()
    # 比较两张图片的像素距离，如果两张图片完全相同则result=0，差距越多result越大
    result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return result

#将图像切割成3*3块正方形图像的函数
def splitimage(src,rownum,colnum,dstpath):
    img=Image.open(src)
    w,h=img.size #图片大小
    if rownum<=h and colnum<=w:
        print('original image info:%sx%s,%s,%s'%(w,h,
                                                 img.format,img.mode))
        print('开始处理图片切割，请稍候-')
        s=os.path.split(src)
        if dstpath=='':#没有输入路径
            dstpath=s[0]#使用源图片所在目录s[0]
        fn=s[1].split('.')#s[1]是源图片文件名
        basename=fn[0]#主文件名
        ext=fn[-1]#扩展名
        num = 0
        rowheight = h//rownum
        colwidth = w//colnum
        for r in range(rownum):
            for c in range(colnum):
                box=(c*colwidth,r*rowheight,(c+1)*colwidth,(r+1)*rowheight)
                img.crop(box).save(os.path.join(dstpath,basename+''+str(num)+'.'+ext))
                num=num+1
        print('图片切割完毕，共生成%s张小图片。'% num)
    else:
        print('不合法的行列切割参数！')

#以测试图像为目标进行切割
src= 'aitest.jpg'
if os.path.isfile(src):
    dstpath = ''
    if(dstpath=='')or os.path.exists(dstpath):
        row=3
        col=3
        splitimage(src,row,col,dstpath)
    else:
        print('图片输出目录%s不存在！'%dstpath)
else:
    print('图片文件%s不存在!'%src)

#创建字符串piclist，用来存储测试图像对应的位置序列
piclist = ''
#创建两个元组，对应切割图像中的纯黑或纯白方块，备用
tup1 = (255,255,255)
tup2 = (0,0,0)

blackblock = False
for i in range(9):
    img = Image.open("aitest"+ str(i) +".jpg")
    imgstr = "aitest"+ str(i) +".jpg"
    clrs = img.getcolors()

    if(len(clrs)!=1):
        file_names = []
        for parent, dirnames, filenames in os.walk('D:/char/charspec'):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            file_names = filenames
        for k in range(315):
            if(image_contrast(imgstr, 'D:/char/charspec/'+file_names[k]) == 0):
                tempfn = file_names[k]
                if (len(tempfn) > 8):
                    #print(tempfn[0:6])
                    picname = tempfn[0:6]
                    #print(tempfn[6])
                    num = int(tempfn[6])+1
                    #print(type(tempfn[6]))
                    piclist = piclist +str(num)
                    #print(piclist)
                else:
                    #print(tempfn[0:2])
                    picname = tempfn[0:2]
                    #print(tempfn[2])
                    #print(type(tempfn[2]))
                    num = int(tempfn[2]) + 1
                    piclist = piclist + str(num)
            k = k + 1
    elif(clrs[0][1] == tup1):
        piclist = piclist + '0'
    elif(clrs[0][1] == tup2):
        piclist = piclist + 't'
        tmp = i
        blackblock = True
        #print('你这个黑块能把人烦死',tmp)
    i=i+1
for m in range(9):
    if (len(tempfn) > 8 and blackblock == True):
        if(image_contrast("aitest"+ str(tmp) +".jpg", 'D:/char/charspec/' + tempfn[0:6] + str(m) + '.jpg')==0):
            strm = str(m+1)
            #print(strm)
            piclist= piclist.replace('t',strm)
    elif(len(tempfn) < 8 and blackblock == True):
        if(image_contrast("aitest"+ str(tmp) +".jpg", 'D:/char/charspec/' + tempfn[0:2] + str(m) + '.jpg')==0):
            strm = str(m+1)
            #print(strm)
            piclist= piclist.replace('t',strm)
print(piclist)




import PIL.Image as Image
def changeJpgToPng(w, h, path):
    # 修改图像大小
    image = Image.open(path)
    image = image.resize((w, h), Image.ANTIALIAS)

    # 将jpg转换为png
    png_name = str(path)[0:-len('.jpg')] + 'min.png'
    image.save(png_name)
    #print(png_name)
    return png_name
#w = 300
#h = 300
#path = 'D:char/test.jpg'
#changeJpgToPng(w, h, path)
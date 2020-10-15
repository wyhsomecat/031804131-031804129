from tkinter import*
from tkinter.messagebox import*
from PIL import Image,ImageTk
import os
import random
from PicFormChanger import changeJpgToPng

#从这里开始抽取图片
rootdir = "d:char/char"
file_names = []
for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    file_names = filenames
x = random.randint(0, len(file_names)-1)
print(file_names[x])

#从这里开始调整图片大小格式
w = 300
h = 300
#path = file_names[x]
jpgpath = rootdir + "/" +file_names[x]
changeJpgToPng(w, h, jpgpath)
pngpath = rootdir + "/" +file_names[x][0:-len('.jpg')] + 'min.png'

#从这里开始切割图片
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
        num=0
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
src = pngpath
if os.path.isfile(src):
        splitimage(src,3,3,rootdir)
else:
    print('图片文件%s不存在!'%src)

#定义常量
#画布的尺寸
WIDTH=300
HEIGHT=300
#图像块的边长
IMAGE_WIDTH=WIDTH//3
IMAGE_HEIGHT=HEIGHT//3
#游戏的行/列数
ROWS=3
COLS=3
#移动步数
steps=0
string = ""
#保存所有图像块的列表
board=[[0,1,2],
       [3,4,5],
       [6,7,8]]
root=Tk('#虽然不知道这是什么但我估计用不上')
root.title("拼图test")

#载入外部事先生成的9个小图像块
Pics=[]
for i in range(9):
    filename= rootdir + "/" +file_names[x][0:-len('.jpg')]+'min'+str(i)+".png"
    Pics.append(PhotoImage(file=filename))

class Square:
    def __init__(self,orderID):
        self.orderID=orderID
    def draw(self,canvas,board_pos):
        img=Pics[self.orderID]
        canvas.create_image(board_pos,image= img)

def init_board():#打乱图像块
    L=list(range(9))#L列表中[0,1,2,3,4,5,6,7,8]
    random.shuffle(L)
    unorder =0
    for i in range(9):
        for j in range(i):
            if L[i] * L[j] != 0:
                if L[j] > L[i]:
                    unorder = unorder + 1
    for i in range(ROWS):
        for j in range(COLS):
            idx=i*ROWS+j
            orderID=L[idx]
            if orderID is 8: #8号拼块不显示,所以存为None
                board[i][j]=None
            else:
                board[i][j]=Square(orderID)
    if(unorder%2==1):
        random.shuffle(L)

def drawBoard(canvas):
    canvas.create_polygon((0,0,WIDTH,0,WIDTH,HEIGHT,0,HEIGHT),
    width=1,outline='White',fill='White')
    #画所有图像块
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j]is not None:
                board[i][j].draw(canvas,(IMAGE_WIDTH*(j+0.5),
                     IMAGE_HEIGHT*(i+0.5)))

def mouseclick(pos):
    global steps
    # 将单击位置换算成拼图板上的棋盘坐标
    r = int(pos.y // IMAGE_HEIGHT)
    c = int(pos.x // IMAGE_WIDTH)
    global string
    if r < 3 and c < 3:  # 单击位置在拼图板内才移动图片
        if board[r][c] is None:  # 单击空位置,什么也不移动
            return
        else:
            # 依次检查被单击当前图像块的上、下、左、右是否有空位置,如果有,就移动当前图像块
            current_square = board[r][c]
            if r - 1 >= 0 and board[r - 1][c] is None:  # 判断上面
                board[r][c] = None
                board[r - 1][c] = current_square
                steps += 1
                string = string + 'w'
            elif c + 1 <= 2 and board[r][c + 1] is None:  # 判断右面
                board[r][c] = None
                board[r][c + 1] = current_square
                steps += 1
                string = string + 'd'
            elif r + 1 <= 2 and board[r + 1][c] is None:  # 判断下面
                board[r][c] = None
                board[r + 1][c] = current_square
                steps += 1
                string = string + 's'
            elif c - 1 >= 0 and board[r][c - 1] is None:  # 判断左面
                board[r][c] = None
                board[r][c - 1] = current_square
                steps += 1
                string = string + 'a'
            # print(board)
            label1["text"] = "步数：" + str(steps)
            #label2["text"] = "操作" + string
            cv.delete('all')
            # 清除画布上的内容
            drawBoard(cv)
    if win():
        showinfo(title="恭喜",message="你成功了！")
        print(string)

def win() :
    for i in range (ROWS) :
        for j in range (COLS) :
            if board[i][j] is not None and board[i][j].orderID!=i * ROWS + j:
                return False
    return True

def play_game() :
    global steps
    steps=0
    init_board()

def callBack2():
    print("重新开始")
    play_game()
    cv.delete('all')
    #清除画布上的内容
    drawBoard(cv)

path=pngpath
image1=Image.open(path)#通过Image=photo设置要展示的图片
image1 = image1.resize((150, 150), Image.ANTIALIAS)
photo1=ImageTk.PhotoImage(image1)#创建tkinter兼容的图片
cv=Canvas(root,bg='green',width=WIDTH,height=HEIGHT)
bl=Button(root,text="重新开始",command=callBack2,width=28)
b2=Label(root,image=photo1,width=200)
label1=Label(root,text="步数："+str(steps),fg="red",width=40)
label1.pack()
label2 = Label(root,text = "操作"+string,fg = "black",width = 100 )
label2.pack()
cv.bind("<Button-1>",mouseclick)
#cv.focus_set()  # 必须获取焦点
cv.pack(side='right')
bl.pack()
b2.place(y = 150,width = 150,height = 150)
play_game()
drawBoard(cv)
root.mainloop()


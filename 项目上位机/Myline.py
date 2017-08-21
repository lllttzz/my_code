from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import argparse

#绘制曲线主函数
def Mymain(x,y,im,am,pos,dir):
    plt.clf()
    n = ['rt','gt','bt']
    for i in range(3):
        n[i] = im[i].getdata() #获取图片参数
        n[i] = np.matrix(n[i]) #转换为矩阵
        n[i] = np.reshape(n[i],(x,y))

    a = range(x)
    a = np.matrix(a)
    b = range(x*y)
    b = np.matrix(b)

    #横向图片绘制
    if dir == 1:
        plt.xlim(0, x)
        plt.ylim(0, y)
        plt.plot(a[0,:].T, n[0][pos,:].T,'-',c='r')
        plt.plot(a[0,:].T, n[1][pos,:].T,'-',c='g')
        plt.plot(a[0,:].T, n[2][pos,:].T,'-',c='b')
        plt.title('line_regression_horizontal')

    #纵向图片绘制
    if dir == 0:
        plt.xlim(0, x)
        plt.ylim(0, y)
        plt.plot(a[0,:].T, n[0][:,pos],'-',c='r')
        plt.plot(a[0,:].T, n[1][:,pos],'-',c='g')
        plt.plot(a[0,:].T, n[2][:,pos],'-',c='b')
        plt.title('line_regression_vertical')

    #全图绘制
    elif dir == 2:
        plt.xlim(0, x*y+5)
        plt.ylim(0, y+5)
        plt.scatter(b[0,:],am[:,0],c='r',alpha=0.1)
        plt.scatter(b[0,:],am[:,1],c='g',alpha=0.1)
        plt.scatter(b[0,:],am[:,2],c='b',alpha=0.1)
        plt.title('scatter diagram')

    plt.xlabel("picture_position")
    plt.ylabel("RGB_value")
    plt.ion()
    plt.show()

def Pic(pos,dir):
    am = Image.open("lena.bmp").convert()
    x,y = am.size
    im = am.split()
    am = am.getdata()
    am = np.matrix(am)
    Mymain(x,y,im,am,pos,dir)

#作为模块导入使用，则不执行以下语句
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser() #命令行解析函数
#
#     parser.add_argument('picture')
#     parser.add_argument('x',type=int,choices=range(512))
#     parser.add_argument('y',type=int,choices=[0, 1, 2])
#     args = parser.parse_args() #解析上述函数
#     pos,dir=args.x,args.y #命令行自定参数赋值给pos和dir
#     IMG = args.picture
#
#     am = Image.open(IMG)
#     im = am.split()
#     am = am.getdata()
#     am = np.matrix(am)
#     Mymain(im,am,pos,dir)

def PPic(i,dir):
    import pygame
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt
    # from VideoCapture import Device
    # import time
    # import sys, pygame
    #
    # cam = Device(devnum=2, showVideoWindow=0)
    # cam.saveSnapshot('test.jpg', timestamp=3, boldfont=1, quality=75)

    #绘制曲线主函数
    def Pic(pos,dir,i):
        im = am.split()
        plt.clf()
        n = ['rt','gt','bt']
        for i in range(3):
            n[i] = im[i].getdata() #获取图片参数
            n[i] = np.matrix(n[i]) #转换为矩阵
            n[i] = np.reshape(n[i],(y,x))

        a = range(x)
        a = np.matrix(a)
        b = range(y)
        b = np.matrix(b)

        #横图片绘制
        if dir == 1:
            plt.xlim(0, x)
            plt.ylim(0, 255)
            plt.plot(a[0,:].T, n[0][pos,:].T,'-',c='r')
            plt.plot(a[0,:].T, n[1][pos,:].T,'-',c='g')
            plt.plot(a[0,:].T, n[2][pos,:].T,'-',c='b')
            plt.title('line_regression_horizontal')

        #纵图片绘制
        if dir == 0:
            plt.xlim(0, y)
            plt.ylim(0, 255)
            plt.plot(b[0,:].T, n[0][:,pos],'-',c='r')
            plt.plot(b[0,:].T, n[1][:,pos],'-',c='g')
            plt.plot(b[0,:].T, n[2][:,pos],'-',c='b')
            plt.title('line_regression_vertical')

        plt.xlabel("picture_p osition")
        plt.ylabel("RGB_value")
        plt.ion() # 显示图片的同时程序继续运行
        plt.show() # 显示

    pygame.init() #初始化pygame
    global am
    am = Image.open(i)
    global x
    global y
    x,y = am.size # 获取图片长和宽
    screen = pygame.display.set_mode((x,y),0,32) # 设置窗口
    pygame.display.set_caption("picture") #设置窗口标题

    while True:
        background = pygame.image.load(i) #载入图片
        m_x,m_y = pygame.mouse.get_pos() # 获取鼠标位置
        for event in pygame.event.get(): # 检测有无事件产生
            if event.type == pygame.QUIT:  #检测用户是否按下关闭
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # 检测鼠标是否被按下
                m_x,m_y = pygame.mouse.get_pos()
                if dir == 0:
                    Pic(m_x,dir,i)
                if dir == 1:
                    Pic(m_y,dir,i)
        if dir == 1:
            pygame.draw.line(background, (80,0,250), (0,m_y), (x,m_y), 1) # 画横线

        elif dir == 0:
            pygame.draw.line(background, (80,0,250), (m_x,0), (m_x,y), 1) # 画竖线

        screen.blit(background,(0,0)) # 把图片画进窗口
        pygame.display.update() #更新窗口变化

# PPic('test.jpg',1)

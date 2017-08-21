import wx
import os
import wx.xrc
import VideoCapture
import Photo as P
import pygame_pic11 as py

global filename
class Frame1(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,None,-1,'torcam',size=(600,300))#-1表示Id由系统自动分配，可以通过frame.GetId()来获取此值

        #创建菜单
        filemenu = wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN,'&Load Image','Open a Image to edit')
        menuExit = filemenu.Append(wx.ID_EXIT,'&Exit','Terminate the program')
        helpmenu = wx.Menu()
        menuAbout= helpmenu.Append(wx.ID_ABOUT,'&About','Information about this program')

        #创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,'&File')
        menuBar.Append(helpmenu,'&Help')
        self.SetMenuBar(menuBar)

        # 创建工具栏
        toolbar = self.CreateToolBar()
        bitm1 = wx.Bitmap("save.png")
        bitm1.SetSize(size=(24, 24))
        bitm2 = wx.Bitmap("pic1.png")
        bitm2.SetSize(size=(24, 24))
        bitm = wx.Bitmap("pic.png")
        bitm.SetSize(size=(24, 24))
        bitm3 = wx.Bitmap("play.png")
        bitm3.SetSize(size=(24, 24))
        bitm4 = wx.Bitmap("stop.png")
        bitm4.SetSize(size=(24, 24))
        saTool = toolbar.AddTool(wx.ID_ANY, 'Save', bitm1)
        picVTool = toolbar.AddTool(wx.ID_ANY, 'LineV', bitm2)
        playtool = toolbar.AddTool(wx.ID_ANY, 'Play', bitm3)
        stoptool = toolbar.AddTool(wx.ID_ANY, 'Stop', bitm4)
        tupian = toolbar.AddTool(wx.ID_ANY, 'Anger', bitm)
        toolbar.Realize()
        self.statusbar = self.CreateStatusBar()  # 状态栏
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-2,-1])

        #事件
        self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)
        self.Bind(wx.EVT_MENU,self.OnExit,menuExit)
        self.Bind (wx.EVT_MENU,self.OnAbout,menuAbout)
        self.Bind(wx.EVT_TOOL,self.OnSav,saTool)
        self.Bind(wx.EVT_TOOL,self.OnPicH,tupian)
        self.Bind(wx.EVT_TOOL, self.OnPicV, picVTool)
        self.Bind(wx.EVT_TOOL, self.OnButton, playtool)
        self.Bind(wx.EVT_TOOL, self.Stop, stoptool)

        self.SetMenuBar(menuBar)

        # self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL ) #布局子窗口部件
        # wx.TAB_TRAVERSAL：‎使用此启用非对话框窗口的选项卡遍历。‎
        # wx.ID_ANY：自动创建一个标识符‎
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL ) #创建绘画窗口
        # 0：对象将不改变尺寸，无论sizer如何变化
        # 1：表示绘画窗口的尺寸要随框架的改变而改变
        # wx.EXPAND表示完全填满
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 1 )
        # self.SetSizer( bSizer1 )
        # self.Layout() #强迫sizer去重新计算它的子类的尺寸和位置

        self.Centre() #窗口居中

        self.timer=wx.Timer(self) #时间事件
        self.Bind(wx.EVT_TIMER,self.OnIdel,self.timer)

    def OnButton( self, event ): # 拍照按键函数
        self.cam = VideoCapture.Device() # 摄像头初始化
        self.cam.saveSnapshot('Photo.jpg') # 保存图片
        self.timer.Start(100) # 时间事件间隔
        # event.Skip()

    def OnIdel(self,evnet): # 时间事件函数
        #cam = VideoCapture.Device()
        self.cam.saveSnapshot('test.jpg') # 保存图片
        # wx.Image(name, type=wx.BITMAP_TYPE_ANY, index=-1)
        img=wx.Image("test.jpg",wx.BITMAP_TYPE_ANY).ConvertToBitmap() # 导入图片
        dc=wx.ClientDC(self.m_panel1) # 设定绘画时机
        # DrawBitmap(bitmap,x, y, useMask=False)
        dc.DrawBitmap(img,0,0,False) # 绘制位图


    def OnPicH(self,p):
        try:
         py.PPic(filename,1)
        except NameError:
            warn = wx.MessageDialog(self,'Pleasse open a picture!','Error', wx.OK)
            warn.ShowModal()
            warn.Destroy()
    def OnPicV(self,p):
        try:
            py.PPic(filename, 0)
        except NameError:
            warn = wx.MessageDialog(self, 'Pleasse open a picture!', 'Error', wx.OK)
            warn.ShowModal()
            warn.Destroy()

    def OnSav(self,event):
        dlg = wx.FileDialog(self, u"保存文件", 'C:/Users/Administrator/Pictures', "",'jpg files (*.jpg)|*.jpg|All files|*',wx.FD_SAVE)
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self,p):
        global filename
        '''打开文件'''
        #file_wildcard = "Paint files(*.paint)|*.paint|All files(*.*)|*.*"
        win = Frame1(self)
        self.panel = wx.Panel(win)
        dlg = wx.FileDialog(self, "Open paint file",'C:/Users/Administrator/Pictures',style=wx.DD_DEFAULT_STYLE,wildcard='jpg files (*.jpg)|*.jpg|All files|*')
        if dlg.ShowModal() == wx.ID_OK:#当点击ok按钮

            filename= dlg.GetPath()#获取路径
            bm = wx.Bitmap(filename, wx.BITMAP_TYPE_ANY)
            wx.StaticBitmap(self.panel, 1, bm)#显示位图
            dlg.Destroy()
            sizer = wx.BoxSizer()#布局
            sizer.Add(self.panel,1, wx.EXPAND)
            win.SetSizerAndFit(sizer)#使窗口和布局的大小一致
            win.Centre()
        self.panel.Bind(wx.EVT_MOTION, self.OnMove)#绑定
        win.Show(True)

    def OnMove(self,event):
        # 设置状态栏1内容
        #self.statusbar.SetStatusText(u"当前线条长度：%s" % len(self.paint.curLine), 0)
        # 设置状态栏2内容
        pos = event.GetPosition()
        self.statusbar.SetStatusText(u"鼠标位置：%s,%s" %(pos.x,pos.y),1)
        event.Skip()

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self,'This is My First GUI Process.In this program you can take pictures and analyze data of picture.','About', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def Stop(self, event):
        self.timer.Stop()

    # def Pho(self,p):
    #     global filename
    #     P.Photo()
    #     filename = 'test.jpg'

app = wx.App()
frame = Frame1(None)
frame.Show(True)
app.MainLoop()

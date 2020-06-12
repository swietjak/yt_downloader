from pytube import YouTube
import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Hello World')
        self.panel = DownloadPanel(self)
        # self.create_menu()
        self.Show()

    """
    def create_menu(self):
        menu_bar =  wx.MenuBar()
        file_menu = wx.Menu()
        open_folder
    """


class DownloadPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.row_obj_dict = {}
        self.file_name = ''
        self.links = []
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.txt_ctrl = wx.TextCtrl(self)
        my_btn = wx.Button(self, label='Press Me',)
        file_btn = wx.Button(self, label='Choose File',)

        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 100),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, 'Title', width=140)
        self.list_ctrl.InsertColumn(1, 'Size', width=140)
        self.list_ctrl.InsertColumn(2, 'Link', width=140)
        box_sizer.Add(self.list_ctrl, 0, wx.ALL |
                      wx.EXPAND, 5)

        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        file_btn.Bind(wx.EVT_BUTTON, self.choose_file)

        box_sizer.Add(self.txt_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        box_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        box_sizer.Add(file_btn, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(box_sizer)

    def choose_file(self, event):
        title = "Choose File"
        dlg = wx.FileDialog(
            self, title, wildcard="txt files (*.txt)|*.txt", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_name = dlg.GetPath()
        print(self.file_name)
        dlg.Destroy()

    def download_film(self):
        for i, url in enumerate(self.links):
            print(url)
            try:
                yt = YouTube(url)
                video = yt.streams.get_highest_resolution()
                video.download("Dump")
                self.AddToList(i, url, video.title, video.filesize)
                print(video)
            except KeyError:
                print('KeyError')

    def AddToList(self, index, url, title, filesize):
        self.list_ctrl.InsertItem(index, title)
        self.list_ctrl.SetItem(index, 1, str(filesize))
        self.list_ctrl.SetItem(index, 2, url)

    def on_press(self, event):
        #value = self.txt_ctrl.GetValue()
        with open(self.file_name) as f:
            self.links = f.read().split("\n")

        self.download_film()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()

"""
links=[]
with open('test.txt') as f:
    links = f.read().split("\n")
print(links)
for url in links:
    print(url)
    try:
        yt = YouTube(url)
        video = yt.streams.filter(res="720p", mime_type="video/mp4")
        video[0].download("Dump")
        print(video[0])
    except KeyError:
        print('KeyError')
"""

#Boa:Dialog:AboutDialog

import wx

def create(parent):
    return AboutDialog(parent)

[wxID_ABOUTDIALOG, wxID_ABOUTDIALOGOK_BUTTON, wxID_ABOUTDIALOGSTATICTEXT2, 
 wxID_ABOUTDIALOGSTATICTEXT3, wxID_ABOUTDIALOGSTATICTEXT4, 
 wxID_ABOUTDIALOGTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class AboutDialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_ABOUTDIALOG, name='AboutDialog',
              parent=prnt, pos=wx.Point(482, 308), size=wx.Size(350, 234),
              style=wx.DEFAULT_DIALOG_STYLE, title='About PAWS')
        self.SetClientSize(wx.Size(342, 196))
        self.SetToolTipString('')
        self.Show(False)

        self.staticText2 = wx.StaticText(id=wxID_ABOUTDIALOGSTATICTEXT2,
              label='PAWS 2.0', name='staticText2', parent=self,
              pos=wx.Point(16, 16), size=wx.Size(149, 37), style=0)
        self.staticText2.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Arial'))

        self.staticText3 = wx.StaticText(id=wxID_ABOUTDIALOGSTATICTEXT3,
              label='Written by Roger Plowman', name='staticText3', parent=self,
              pos=wx.Point(16, 56), size=wx.Size(155, 16), style=0)
        self.staticText3.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Arial'))
        self.staticText3.Show(True)

        self.staticText4 = wx.StaticText(id=wxID_ABOUTDIALOGSTATICTEXT4,
              label='Copyright  1998 - 2008', name='staticText4', parent=self,
              pos=wx.Point(16, 72), size=wx.Size(131, 16), style=0)
        self.staticText4.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Arial'))
        self.staticText4.Show(True)

        self.OK_Button = wx.Button(id=wxID_ABOUTDIALOGOK_BUTTON, label='Ok',
              name='OK_Button', parent=self, pos=wx.Point(144, 152),
              size=wx.Size(64, 31), style=wx.BU_EXACTFIT)
        self.OK_Button.Bind(wx.EVT_BUTTON, self.OnOK_ButtonButton,
              id=wxID_ABOUTDIALOGOK_BUTTON)

        self.textCtrl1 = wx.TextCtrl(id=wxID_ABOUTDIALOGTEXTCTRL1,
              name='textCtrl1', parent=self, pos=wx.Point(16, 96),
              size=wx.Size(320, 21), style=0,
              value='Website: http://home.fuse.net/wolfonenet/PAWS.htm')
        self.textCtrl1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Arial'))
        self.textCtrl1.SetToolTipString('')
        self.textCtrl1.SetEditable(False)
        self.textCtrl1.SetBackgroundColour(wx.Colour(236, 233, 216))
        self.textCtrl1.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnOK_ButtonButton(self, event):
        self.Close()
        event.Skip()

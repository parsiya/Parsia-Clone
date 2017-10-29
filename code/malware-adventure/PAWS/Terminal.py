#!/usr/bin/env python
#Boa:App:BoaApp

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                      Python Adventure Writing System                          #
#                             wxPython Terminal                                 #
#                     Written by Roger Plowman (c) 2008                         #
#                                                                               #
# The C="""...""" statements scattered throughout this source code are actually #
# a work-around for Python's lack of block comments. Notepad++ can only fold    #
# block comments, not a series of comment lines. Using C="""...""" doesn't      #
# increase PAWS memory footprint, although it does have a tiny impact           #
# on loading time.                                                              #
#                                                                               #
C="""
  This module contains the skeleton of the terminal program, basically the 
  main loop code and a few references. Note it does NOT follow PAWS style
  guidelines, because the Boa Constructor IDE generated large portions of
  the program. Imposing the guidelines could confuse the code generator in
  the IDE, causing this program to fail.

  Written By: Roger Plowman
  Written On: 01/20/2008
  """
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import wx
import TerminalFrame

modules ={u'AboutDialog': [0, '', u'AboutDialog.py'],
 u'TerminalFrame': [1, 'Main frame of Application', u'TerminalFrame.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = TerminalFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()

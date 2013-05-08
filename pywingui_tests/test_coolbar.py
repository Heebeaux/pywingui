## 	   Copyright (c) 2003 Henk Punt

## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the
## "Software"), to deal in the Software without restriction, including
## without limitation the rights to use, copy, modify, merge, publish,
## distribute, sublicense, and/or sell copies of the Software, and to
## permit persons to whom the Software is furnished to do so, subject to
## the following conditions:

## The above copyright notice and this permission notice shall be
## included in all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
## EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
## MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
## NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
## LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
## OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
## WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

from pywingui.windows import *
from pywingui.wtl import *

from pywingui import comctl
from pywingui import gdi
from pywingui.lib import form
from pywingui.lib import list
from pywingui.lib import coolbar
from pywingui.lib import trackbar


comctl.InitCommonControls(comctl.ICC_LISTVIEW_CLASSES | comctl.ICC_COOL_CLASSES | comctl.ICC_USEREX_CLASSES | comctl.ICC_BAR_CLASSES)

ims = 32
iml = comctl.ImageList(ims, ims, comctl.ILC_COLOR32 | comctl.ILC_MASK, 0, 64)
iml.AddIconsFromModule('shell32.dll', ims, ims, LR_LOADMAP3DCOLORS)
iml.SetBkColor(gdi.CLR_NONE)

class MyTrackBar(trackbar.TrackBar):

	def __init__(self, *args, **kwargs):
		self.progress_bar = kwargs.pop('progress_bar', None)
		trackbar.TrackBar.__init__(self, *args, **kwargs)

	def OnScroll(self, event):
		#~ print "onscroll!"
		if self.progress_bar:
			self.progress_bar.SetPos(self.GetPos())

class MyForm(form.Form):
	_window_icon_ = Icon('cow.ico')
	_window_icon_sm_ = _window_icon_
	_window_background_ = 0
	_window_title_ = 'Supervaca al Rescate!'

	_form_accels_ = [(FCONTROL|FVIRTKEY, ord('N'), form.ID_NEW)]
	_form_exit_ = form.EXIT_ONDESTROY
	_form_status_msgs_ = {form.ID_NEW: 'Creates a new window.'}

	_form_menu_ = None #suppress default menu

	def __init__(self, *args, **kwargs):
		self.CreateMenu()
		form.Form.__init__(self, *args, **kwargs)

	def OnCreate(self, event):
		coolBar = coolbar.CoolBar(parent = self)

		commandBar = coolbar.CommandBar(parent = coolBar)
		commandBar.AttachMenu(self.menu)

		addressBar = comctl.ComboBox(parent = coolBar)

		buttons = coolbar.ToolBar(parent = coolBar)
		buttons.SetImageList(iml)
		buttons.SetButtonSize(ims, ims)

		button = comctl.TBBUTTON()
		button.idCommand = form.ID_NEW
		#~ button.idCommand = form.ID_CLOSE
		button.fsState = comctl.TBSTATE_ENABLED
		button.fsStyle = comctl.TBSTYLE_BUTTON
		for i in range(iml.GetImageCount()-6):
			button.iBitmap = 1 + i
			buttons.InsertButton(0, button)

		progressBar = comctl.ProgressBar(parent = coolBar, orStyle = comctl.PBS_SMOOTH)
		progressBar.SetBarColor(gdi.RGB(100, 200, 255))
		progressBar.SetBkColor(gdi.RGB(55, 55, 55))
		progressBar.MoveWindow(0, 0, 200, 20, False)
		progressBar.SetRange(0, 500)
		progressBar.SetPos(450)

		aTrackBar = MyTrackBar(parent = coolBar, progress_bar = progressBar, rcPos = RECT(0, 0, 200, 40))
		aTrackBar.SetRange(0, 500)
		aTrackBar.SetPos(450)

		coolBar.SetRedraw(False)
		coolBar.AddSimpleRebarBandCtrl(commandBar)
		coolBar.AddSimpleRebarBandCtrl(buttons, bNewRow = True)
		coolBar.AddSimpleRebarBandCtrl(aTrackBar, cxWidth = 100)
		coolBar.AddSimpleRebarBandCtrl(addressBar, bNewRow = True)
		coolBar.AddSimpleRebarBandCtrl(progressBar, bNewRow = True)
		#~ coolBar.AddSimpleRebarBandCtrl(aTrackBar, title = 'TrackBar', bNewRow = True)
		coolBar.SetRedraw(True)

		aList = list.List(parent = self, orExStyle = WS_EX_CLIENTEDGE)

		aList.InsertColumns([('blaat', 100), ('col2', 150)])
		aList.SetRedraw(0)
		for i in range(100):
			aList.InsertRow(i, ['blaat %d' % i, 'blaat col2 %d' % i])
		aList.SetRedraw(1)

		self.controls.Add(progressBar)
		self.controls.Add(addressBar)
		self.controls.Add(commandBar)
		self.controls.Add(buttons)
		self.controls.Add(aTrackBar)
		self.controls.Add(form.CTRL_COOLBAR, coolBar)
		self.controls.Add(form.CTRL_VIEW, aList)
		self.controls.Add(form.CTRL_STATUSBAR, comctl.StatusBar(parent = self))

	def CreateMenu(self):
		self.menu = Menu()

		self.menuFilePopup = PopupMenu()
		self.menuFilePopup.AppendMenu(MF_STRING, 1018, '&Blaat...\tCtrl+O')
		self.menuFilePopup.AppendMenu(MF_STRING, 1013, '&Piet...\tCtrl+S')

		self.menuFile = PopupMenu()
		self.menuFile.AppendMenu(MF_POPUP, self.menuFilePopup, '&New')
		self.menuFile.AppendMenu(MF_SEPARATOR)
		self.menuFile.AppendMenu(MF_STRING, form.ID_NEW, 'New window')
		self.menuFile.AppendMenu(MF_STRING, form.ID_OPEN, '&Open...\tCtrl+O')
		self.menuFile.AppendMenu(MF_STRING, form.ID_SAVE, '&Save...\tCtrl+S')
		self.menuFile.AppendMenu(MF_STRING, form.ID_SAVEAS, '&Save As...')
		self.menuFile.AppendMenu(MF_SEPARATOR)
		self.menuFile.AppendMenu(MF_STRING, form.ID_EXIT, '&Exit')
		self.menu.AppendMenu(MF_POPUP, self.menuFile, '&File')

		self.menuEdit = PopupMenu()
		self.menuEdit.AppendMenu(MF_STRING, form.ID_UNDO, '&Undo\bCtrl-Z')
		self.menuEdit.AppendMenu(MF_STRING, form.ID_REDO, '&Redo')
		self.menuEdit.AppendMenu(MF_SEPARATOR)
		self.menuEdit.AppendMenu(MF_STRING, form.ID_COPY, '&Copy')
		self.menuEdit.AppendMenu(MF_STRING, form.ID_PASTE, '&Paste')
		self.menuEdit.AppendMenu(MF_STRING, form.ID_CUT, '&Cut')
		self.menu.AppendMenu(MF_POPUP, self.menuEdit, '&Edit')

	def OnNew(self, event):
		frm = MyForm(parent = self, rcPos = RECT(0, 0, 320, 240))
		frm._form_exit_ = form.EXIT_ONLASTDESTROY
		frm.ShowWindow()

	cmd_handler(form.ID_NEW)(OnNew)

	def OnDestroy(self, event):
		application.Quit()

	msg_handler(WM_DESTROY)(OnDestroy)

if __name__ == '__main__':
	mainForm = MyForm()        
	mainForm.ShowWindow()

	application = Application()
	application.Run()

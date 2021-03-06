'''
Custom Icon example based on pyWinGUI, author Maxim Kolosov (2013).
Original was from C++ MSDN CreateIcon example,
see Platform SDK: Windows User Interface "Creating an Icon".
Differences is - this example use 32 bit colored masks with alpha channel.
'''

from pywingui.gdi import *
from pywingui.wtl import *

ANDmaskIcon = (DWORD*64)(
0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
0x00000000, 0x00000000, 0xFF000000, 0xFF000000, 0xFF000000, 0xFF000000, 0x00000000, 0x00000000,
0x00000000, 0xFF000000, 0x00000000, 0xFF000000, 0xFF000000, 0x00000000, 0xFF000000, 0x00000000,
0x00000000, 0xFF000000, 0xFF000000, 0x00000000, 0x00000000, 0xFF000000, 0xFF000000, 0x00000000,
0x00000000, 0xFF000000, 0xFF000000, 0x00000000, 0x00000000, 0xFF000000, 0xFF000000, 0x00000000,
0x00000000, 0xFF000000, 0x00000000, 0xFF000000, 0xFF000000, 0x00000000, 0xFF000000, 0x00000000,
0x00000000, 0x00000000, 0xFF000000, 0xFF000000, 0xFF000000, 0xFF000000, 0x00000000, 0x00000000,
0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000)

XORmaskIcon = (DWORD*64)(
0xFF00FF00, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFF00FF00,
0xFFFF0000, 0xFF0000FF, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0xFF0000FF, 0xFFFF0000,
0xFFFF0000, 0x00000000, 0xFF0000FF, 0x00000000, 0x00000000, 0xFF0000FF, 0x00000000, 0xFFFF0000,
0xFFFF0000, 0x00000000, 0x00000000, 0xFF00FF00, 0xFF00FF00, 0x00000000, 0x00000000, 0xFFFF0000,
0xFFFF0000, 0x00000000, 0x00000000, 0xFF00FF00, 0xFF00FF00, 0x00000000, 0x00000000, 0xFFFF0000,
0xFFFF0000, 0x00000000, 0xFF0000FF, 0x00000000, 0x00000000, 0xFF0000FF, 0x00000000, 0xFFFF0000,
0xFFFF0000, 0xFF0000FF, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0xFF0000FF, 0xFFFF0000,
0xFF00FF00, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFFFF0000, 0xFF00FF00)

class MyWindow(Window):
	_window_title_ = 'Alpha-Color Icon example, based on AND-XOR masks'
	_window_background_ = GetStockObject(WHITE_BRUSH)
	_window_icon_ = _window_icon_sm_ = IconEx(NULL, 8, 8, 1, 32, ANDmaskIcon, XORmaskIcon)

	def OnDestroy(self, event):
		application.Quit()

	msg_handler(WM_DESTROY)(OnDestroy)

myWindow = MyWindow()

application = Application()
application.Run()

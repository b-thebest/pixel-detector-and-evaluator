import win32ui
from PIL import Image
from ctypes import windll
from win32 import win32gui

from time import sleep

def capture_screen(hwnd, w, h):
    # https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        return im
    return None

def ypp_window_callback(hwnd, _extras):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    window_title = win32gui.GetWindowText(hwnd)
    if 'Merciless Client' in window_title:
        print('Window found! location=(%d, %d), size=(%d, %d)' % (x, y, w, h))
        pixelDetector(hwnd, w, h)

def pixelDetector(hwnd, w, h):
    while True:
        screen_image = capture_screen(hwnd, w, h)
        for x in range(2459, 2464, 1):
            for y in range(113, 118, 1):
                r, g, b = screen_image.getpixel((x, y))

                if r == 255 and g == 0 and b == 0:
                    # reddish area means sleep time
                    sleep(5)
                else:
                    #CLICK
                    pass


if __name__ == "__main__":
    win32gui.EnumWindows(ypp_window_callback, None)
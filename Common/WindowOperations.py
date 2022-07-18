import pyautogui
import win32gui
import dxcam
import time


def GetWindowPos(windowTitle=None):
    """
    Gets the x,y,x1,y1 position of a given window title
    Accepts the name of a windows window - string
    :returns the dimensions
    """
    pyautogui.press("alt")
    hwnd = win32gui.FindWindow(None, windowTitle)  # Finds the window title
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)  # sets window to foreground
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)  # finds edges
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1, y1))
        return x, y, x1, y1
    else:
        print('Window not found!')


def GetWindowScreenshot(windowTitle=None, x=None, y=None, x1=None, y1=None):
    """
    Gets the x,y,x1,y1 position of a given window title
    and takes a screen shot of that window.
    Accepts the name of a windows window - string
    :returns the image and the dimensions
    """
    if x is None:
        x, y, x1, y1 = GetWindowPos(windowTitle)

    cam1 = dxcam.create(device_idx=0, output_idx=0)
    cam2 = dxcam.create(device_idx=0, output_idx=1)
    time.sleep(0.005)
    # check if region is on monitor 1 or 2
    try:
        im = cam1.grab(region=(x, y, x1, y1))
    except Exception:
        im = cam2.grab(region=(x - 2560, y, x1 - 2560, y1 - 360))

    return im, x, y, x1, y1


def SelectWindow(windowTitle=None):
    """
    Sets the window to be active
    Accepts the name of a windows window - string
    """
    # needs the alt key as otherwise with a foreground app - OSK it breaks.
    pyautogui.press("alt")
    hwnd = win32gui.FindWindow(None, windowTitle)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
    else:
        print('Window not found!')


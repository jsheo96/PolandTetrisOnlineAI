from ctypes import windll, c_int, c_uint, c_char_p, c_buffer
from struct import calcsize, pack
from PIL import Image

gdi32 = windll.gdi32

# Win32 functions
CreateDC = gdi32.CreateDCA
CreateCompatibleDC = gdi32.CreateCompatibleDC
GetDeviceCaps = gdi32.GetDeviceCaps
CreateCompatibleBitmap = gdi32.CreateCompatibleBitmap
BitBlt = gdi32.BitBlt
SelectObject = gdi32.SelectObject
GetDIBits = gdi32.GetDIBits
DeleteDC = gdi32.DeleteDC
DeleteObject = gdi32.DeleteObject

# Win32 constants
NULL = 0
HORZRES = 8
VERTRES = 10
SRCCOPY = 13369376
HGDI_ERROR = 4294967295
ERROR_INVALID_PARAMETER = 87

def grab_screen(bbox=None):
    """
    Grabs a screenshot. This is a replacement for PIL's ImageGrag.grab() method
    that supports multiple monitors. (SEE: https://github.com/python-pillow/Pillow/issues/1547)

    Returns a PIL Image, so PIL library must be installed.

    Usage:
        im = grab_screen() # grabs a screenshot of the primary monitor
        im = grab_screen([-1600, 0, -1, 1199]) # grabs a 1600 x 1200 screenshot to the left of the primary monitor
        im.save('screencap.jpg')
    """
    bitmap = None
    screen_copy=None
    screen=None
    def cleanup():
        if bitmap:
            DeleteObject(bitmap)
        DeleteDC(screen_copy)
        DeleteDC(screen)
    try:
        screen = CreateDC(c_char_p('DISPLAY'.encode('utf-8')), NULL, NULL, NULL)
        screen_copy = CreateCompatibleDC(screen)

        if bbox:
            left,top,x2,y2 = bbox
            width = x2 - left + 1
            height = y2 - top + 1
        else:
            left = 0
            top = 0
            width = GetDeviceCaps(screen, HORZRES)
            height = GetDeviceCaps(screen, VERTRES)

        bitmap = CreateCompatibleBitmap(screen, width, height)
        if bitmap == NULL:
            print('grab_screen: Error calling CreateCompatibleBitmap. Returned NULL')
            return

        hobj = SelectObject(screen_copy, bitmap)
        if hobj == NULL or hobj == HGDI_ERROR:
            print('grab_screen: Error calling SelectObject. Returned {0}.'.format(hobj))
            return

        if BitBlt(screen_copy, 0, 0, width, height, screen, left, top, SRCCOPY) == NULL:
            print('grab_screen: Error calling BitBlt. Returned NULL.')
            return

        bitmap_header = pack('LHHHH', calcsize('LHHHH'), width, height, 1, 24)
        bitmap_buffer = c_buffer(bitmap_header)
        bitmap_bits = c_buffer((' ' * (height * ((width * 3 + 3) & -4))).encode('utf-8'))
        got_bits = GetDIBits(screen_copy, bitmap, 0, height, bitmap_bits, bitmap_buffer, 0)
        if got_bits == NULL or got_bits == ERROR_INVALID_PARAMETER:
            print('grab_screen: Error calling GetDIBits. Returned {0}.'.format(got_bits))
            return

        image = Image.frombuffer('RGB', (width, height), bitmap_bits, 'raw', 'BGR', (width * 3 + 3) & -4, -1)
        return image


    finally:
        cleanup()


if __name__ == "__main__":
    import time
    import numpy as np
    import cv2
    start = time.time()
    bbox = ((300,300,301,301))
    image_np = np.array(grab_screen(bbox))
    print(time.time() - start)
    cv2.imshow('f',image_np)
    cv2.waitKey(1000)

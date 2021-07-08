from main import *
import win32gui

def press_right_n_times(n):
    for i in range(n):
        PressKey(VK_RIGHT)
        time.sleep(0.001)
        ReleaseKey(VK_RIGHT)
        time.sleep(0.001)
        PressKey(VK_SPACE)
        time.sleep(0.001)
        ReleaseKey(VK_SPACE)
        time.sleep(0.001)

def get_first_layer(screenshot):
    screenshot = np.array(screenshot)
    screenshot = screenshot[132:135, 97:280]
    screenshot = cv2.resize(screenshot,(10,1))
    first_layer = [0]*10
    for i in range(10):
        if min(screenshot[0][i])!=max(screenshot[0][i]):
            first_layer[i]=1

    return first_layer
if __name__ == "__main__":
    # finding windows handle of tetris
    windows_list = []
    toplist = []

    def enum_win(hwnd, result):
        win_text = win32gui.GetWindowText(hwnd)
        windows_list.append((hwnd, win_text))


    win32gui.EnumWindows(enum_win, toplist)

    game_hwnd = 0
    for (hwnd, win_text) in windows_list:
        if "TetrisOnline" in win_text:
            game_hwnd = hwnd

    # set to foreground
    win32gui.SetForegroundWindow(game_hwnd)
    # get image fr om the window

    position = win32gui.GetWindowRect(game_hwnd)
    while True:
        while True:
            screenshot = grab_screen(position)
            screenshot = np.array(screenshot)
            screenshot = screenshot[99:102, 120:303]
            #screenshot = screenshot[132:497, 97:280]
            cv2.imshow('f',screenshot)
            cv2.waitKey(1)

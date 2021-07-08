import win32gui
import time
import cv2
import numpy as np
from PIL import ImageGrab
import random
from keyboard_util import *
from capture_util import grab_screen

I_BLOCK = 128
S_BLOCK = 242
L_BLOCK = 230
Z_BLOCK = 226
O_BLOCK = 163
J_BLOCK = 216
T_BLOCK = 225
BLANK = 43

def random_action():
    m = random.randint(-5, 5)
    while m != 0:
        if m < 0:
            m = m + 1
            PressReleaseKey(VK_RIGHT)
        else:
            m = m - 1
            PressReleaseKey(VK_LEFT)
    PressReleaseKey(VK_SPACE)


def get_board(screenshot):
    screenshot = np.array(screenshot)
    screenshot = screenshot[132:497, 97:280]
    board = cv2.resize(screenshot, (10, 20))
    # color matters
    for i in range(20):
        for j in range(10):
            bdata = board[i][j]
            if max(bdata)<50:
                board[i][j] = 0
            else:
                board[i][j] = 1
    return board[:,:,0]

def get_board_single(screenshot):
    screenshot = np.array(screenshot)
    screenshot = screenshot[99:464, 120:303]
    board = cv2.resize(screenshot, (10, 20))
    # color matters
    for i in range(20):
        for j in range(10):
            bdata = board[i][j]
            if max(bdata)<50:
                board[i][j] = 0
            else:
                board[i][j] = 1
    return board[:,:,0]

def get_next_block(screenshot):
    screenshot = np.array(screenshot)
    screenshot = screenshot[205:212, 330:344]
    next_block = screenshot
    next_block = cv2.resize(screenshot, (1,1))
    next_block = cv2.cvtColor(next_block, cv2.COLOR_RGB2GRAY)
    next_block = next_block[0][0]
    return next_block

def get_hold_block(screenshot):
    screenshot = np.array(screenshot)
    screenshot = screenshot[205:212, 50:64]
    hold_block = screenshot
    hold_block = cv2.resize(screenshot, (1, 1))
    hold_block = cv2.cvtColor(hold_block, cv2.COLOR_RGB2GRAY)
    hold_block = hold_block[0][0]
    return hold_block

def get_heights(board):
    heights = [20] * 10
    for j in range(10):
        for i in range(20):
            if board[i][j] != 0:
                break
            else:
                heights[j] -= 1
    return np.array(heights)

def get_actions(board, current_block):
    heights = get_heights(board)
    actions = []
    print('heights',heights)
    print(current_block)
    if current_block=='I_BLOCK':
        for i in range(7):
            if all(heights[i:i+4]==heights[i]):
                actions.append((0, -3+i, heights[i]))
        for i in range(10):
            actions.append((1,-5+i, heights[i]))
    elif current_block == 'O_BLOCK':
        for i in range(9):
            if heights[i]==heights[i+1]:
                actions.append((0, -4+i, heights[i]))
    elif current_block == 'T_BLOCK':
        for i in range(8):
            if all(heights[i:i+3]==heights[i]):
                actions.append((0, -3+i, heights[i]))
        for i in range(9):
            if heights[i+1]==heights[i]+1:
                actions.append((1, -4+i, heights[i]))
        for i in range(8):
            if heights[i]==heights[i+1] and heights[i]==heights[i+1]+1:
                actions.append((2, -3+i, heights[i+1]))
        for i in range(9):
            if heights[i]==heights[i+1]+1:
                actions.append((3, -3+i, heights[i+1]))
    elif current_block == 'S_BLOCK':
        for i in range(8):
            if heights[i]==heights[i+1] and heights[i]+1==heights[i+2]:
                actions.append((0, -3+i,heights[i]))
        for i in range(9):
            if heights[i+1]+1==heights[i]:
                actions.append((1, -4+i,heights[i+1]))
    elif current_block == 'Z_BLOCK':
        for i in range(8):
            if heights[i+1]==heights[i+2] and heights[i]==heights[i+1]+1:
                actions.append((0, -3+i,heights[i+1]))
        for i in range(9):
            if heights[i]+1==heights[i+1]:
                actions.append((1, -4+i,heights[i]))
    elif current_block == 'L_BLOCK':
        for i in range(8):
            if all(heights[i:i+3]==heights[i]):
                actions.append((0, -3+i,heights[i]))
        for i in range(9):
            if heights[i]==heights[i+1]:
                actions.append((1, -4+i,heights[i]))
        for i in range(8):
            if heights[i+1]==heights[i+2] and heights[i]+1==heights[i+1]:
                actions.append((2, -3+i,heights[i]))
        for i in range(9):
            if heights[i+1]+2==heights[i]:
                actions.append((3, -3+i,heights[i+1]))
    elif current_block == 'J_BLOCK':
        for i in range(7):
            if all(heights[i:i+3]==heights[i]):
                actions.append((0, -3+i,heights[i]))
        for i in range(8):
            if heights[i]+2==heights[i+1]:
                actions.append((1, -4+i,heights[i]))
        for i in range(7):
            if heights[i]==heights[i+1] and heights[i]==heights[i+2]+1:
                actions.append((2, -3+i,heights[i+2]))
        for i in range(8):
            if heights[i]==heights[i+1]:
                actions.append((3, -3+i,heights[i]))
    return actions

def get_best_action(heights, actions):
    print('actions', actions)
    best_action = min(actions, key=lambda x:x[2])
    return best_action

def get_first_layer(screenshot):
    first_layer = np.array(screenshot)
    first_layer = first_layer[132:135, 97:280]
    first_layer = cv2.resize(first_layer,(10,1))
    cv2.imshow('',first_layer)
    cv2.waitKey()
    return first_layer

def get_first_layer_single(screenshot):
    first_layer = np.array(screenshot)
    first_layer = first_layer[99:102, 120:303]
    cv2.imshow('',cv2.cvtColor(first_layer, cv2.COLOR_RGB2BGR))
    cv2.waitKey(1)
    first_layer = cv2.resize(first_layer,(10,1))
    return first_layer

def get_first_blocks(first_layer):
    first_blocks = [0]*10
    for i in range(10):
        if min(first_layer[0][i])!=max(first_layer[0][i]):
            first_blocks[i]=1
    return first_blocks

def get_current_block(first_layer):
    first_layer = cv2.cvtColor(first_layer, cv2.COLOR_RGB2HSV)
    color_block_map={
        43:'S_BLOCK',
        20:'L_BLOCK',
        26:'O_BLOCK',
        101:'I_BLOCK',#99
        143:'T_BLOCK',#147
        114:'J_BLOCK',
        0:'Z_BLOCK'
    }
    color_array = np.array([43,20,26,101,143,114,0])
    block_list = ['S_BLOCK',
                  'L_BLOCK',
                  'O_BLOCK',
                  'I_BLOCK',
                  'T_BLOCK',
                  'J_BLOCK',
                  'Z_BLOCK']

    #if first_layer[0][4][0] not in color_block_map.keys():
    #    print('None!!!!! (Color {})'.format(first_l ayer[0][4][0]))
    #    exit(0)
    #    return 'None'
    #else:

    return block_list[np.argmin(abs(color_array-first_layer[0][4][0]))]

        #return color_block_map[first_layer[0][4][0]]

def take_action(action):
    ups, offset, min_height = action
    print('action', action)

    if ups==3:
        PressReleaseKey(VK_CONTROL)
    else:
        for i in range(ups):
            PressReleaseKey(VK_UP)
    if offset == 0:
        PressReleaseKey(VK_SPACE)
        return
    screenshot = grab_screen(position)
    first_layer = get_first_layer_single(screenshot)
    first_blocks = get_first_blocks(first_layer)
    board = get_board_single(screenshot)
    first_blocks_ = np.array(first_blocks)
    first_blocks_ = np.expand_dims(first_blocks_, axis=0)
    sub_board = np.concatenate((first_blocks_, board[:3]))
    print(sub_board)
    target_x = np.argmax(sub_board[np.max(np.argmax(sub_board, axis=0))]) + offset
    if offset < 0:
        #cur_x = np.argmax(sub_board[np.max(np.argmax(sub_board, axis=0))])
        PressKey(VK_LEFT)
    else:
        #cur_x = 9-np.argmax(sub_board[np.max(np.argmax(sub_board, axis=0))][::-1])
        PressKey(VK_RIGHT)
    start = time.time()
    while True:
        start = time.time()
        screenshot = grab_screen(position)
        end = time.time()

        first_layer = get_first_layer_single(screenshot)
        first_blocks = get_first_blocks(first_layer)
        board = get_board_single(screenshot)

        first_blocks_ = np.array(first_blocks)
        first_blocks_ = np.expand_dims(first_blocks_, axis=0)
        sub_board = np.concatenate((first_blocks_, board[:3]))
        #last_blocks = sub_board[np.max(np.argmax(sub_board, axis=0))]
        #print(last_blocks)
        #print('cur_x+offset', cur_x, offset)
        print('proprtion of grab_screen {}%'.format((end-start)/(time.time()-start)*100))
        cur_x = np.argmax(sub_board[np.max(np.argmax(sub_board, axis=0))])

        if cur_x == target_x: ##TODO: correct placement if the block exceeds
            #time.sleep(0.015)
            PressKey(VK_SPACE)
            time.sleep(0.001)
            #time.sleep(0.0166)
            ReleaseKey(VK_LEFT)
            time.sleep(0.001)
            #time.sleep(0.0166)
            ReleaseKey(VK_RIGHT)
            break
        print('offset, cur_x, target_x', offset, cur_x, target_x)
        if offset < 0:
            if cur_x < target_x:
                print('back to right')
                ReleaseKey(VK_LEFT)
                time.sleep(0.001)
                PressKey(VK_RIGHT)
        else:
            if cur_x > target_x:
                print('back to left')
                ReleaseKey(VK_RIGHT)
                time.sleep(0.001)
                PressKey(VK_LEFT)


        #if offset < 0:
        #    PressKey(VK_LEFT)
            #ReleaseKey(VK_LEFT)
        #else:
        #    PressKey(VK_RIGHT)
            #time.sleep(0.015)
            #ReleaseKey(VK_RIGHT)
    time.sleep(0.0166)
    print('release space!')
    ReleaseKey(VK_SPACE)



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

        if "TetrisOnline" == win_text:
            game_hwnd = hwnd

    # set to foreground
    win32gui.SetForegroundWindow(game_hwnd)
    # get image fr om the window
    position = win32gui.GetWindowRect(game_hwnd)
    time.sleep(1)
    while True:
        # Take screenshot
        screenshot = grab_screen(position)
        first_layer = get_first_layer_single(screenshot)
        # cv2.imshow('f',cv2.resize(cv2.cvtColor(first_layer, cv2.COLOR_RGB2BGR),None,fx=20,fy=20,interpolation=cv2.INTER_NEAREST))
        # cv2.waitKey()
        current_block = get_current_block(first_layer)
        hold_block = get_hold_block(screenshot)
        board = get_board_single(screenshot)
        #board = cv2.cvtColor(board, cv2.COLOR_RGB2GRAY)
        #cv2.imshow("Screen", cv2.resize(board,None,fx=20,fy=20,interpolation=cv2.INTER_NEAREST))

        actions = get_actions(board, current_block)

        # If there is no where to place the block, then press hold key
        if actions == []:
            print('hold')
            PressReleaseKey(VK_SHIFT)
            screenshot = grab_screen(position)
            first_layer = get_first_layer_single(screenshot)
            current_block = get_current_block(first_layer)
            actions = get_actions(board, current_block)

        # If there is still no place to fit, just put it on random place
        if actions == []:
            actions.append((random.randint(0,4), random.randint(-3,3),0))

        action = get_best_action(get_heights(board), actions)
        take_action(action)
        time.sleep(0.02)
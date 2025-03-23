import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import time

window_title = '原神'
app_window = gw.getWindowsWithTitle(window_title)[0]
x_window, y_window, width, height = app_window.left, app_window.top, app_window.width, app_window.height


def screenshot():
    shot = pyautogui.screenshot(region=(x_window, y_window, width, height))
    image_np = np.array(shot)
    img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image = img[29:930, 8:1608]
    return image


def sure():
    """
    点击确认按钮
    """
    x = x_window + 789
    y = y_window + 789
    pyautogui.click(x, y, clicks=1, button='left')
    print('INFO:已点击')


def clean():
    time.sleep(1)
    pyautogui.click(797 + x_window, 443 + y_window, clicks=2, button='left')


def end():
    print('INFO:将结束本回合')
    time.sleep(2)
    pyautogui.click(64 + x_window, 445 + y_window, clicks=1, button='left')
    time.sleep(1)
    pyautogui.click(169 + x_window, 445 + y_window, clicks=1, button='left')
    time.sleep(5)


def harmony(t):
    """
    调和手牌
    """
    for _ in range(t):
        x1 = 840 + x_window
        y1 = 900 + y_window
        x2 = 1551 + x_window
        y2 = 499 + y_window
        pyautogui.click(797 + x_window, 443 + y_window, clicks=2, button='left')
        time.sleep(0.5)
        pyautogui.click(x1, y1, clicks=2, button='left')
        pyautogui.mouseDown()
        time.sleep(0.5)
        pyautogui.mouseUp()
        pyautogui.click(x1, y1, clicks=1, button='left')
        pyautogui.moveTo(x2, y2, duration=0.1)
        pyautogui.mouseUp()
        pyautogui.click(x2, y2, clicks=2, button='left')
        time.sleep(1)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        print('INFO:已调和')

        time.sleep(1)
        x = x_window + 789
        y = y_window + 789
        pyautogui.click(x, y, clicks=1, button='left')
        print('INFO:已点击')
        time.sleep(1)
        clean()


def click_dice(where: list[bool]):
    """
    点击重投骰子
    """
    screenshot()
    dices = [(318, 504), (318, 695), (318, 878), (318, 1067), (523, 504), (523, 695), (523, 878), (523, 1067)]
    for num, point in enumerate(where):
        if point:
            y1, x1 = dices[num]
            y = y_window + y1
            x = x_window + x1
            pyautogui.click(x, y, clicks=1, button='left')
            time.sleep(0.05)
    print('INFO:已点击')
    sure()


def click_skill(what):  # 123技能
    skill_x = [1316, 1423, 1500]
    pyautogui.click(skill_x[what - 1] + x_window, 807 + y_window, clicks=1, button='left')
    time.sleep(0.5)
    pyautogui.mouseDown()
    time.sleep(0.5)
    pyautogui.mouseUp()



def change(who):
    change_x = [619, 791, 972]
    if who <= 2:
        pyautogui.click(change_x[who] + x_window, 626 + y_window, clicks=1, button='left')
        time.sleep(1.4)
    pyautogui.moveTo(1519 + x_window, 798 + y_window, duration=0.1)
    pyautogui.mouseDown()
    time.sleep(0.35)
    pyautogui.mouseUp()
    pyautogui.mouseDown()
    time.sleep(0.35)
    pyautogui.mouseUp()
    clean()
    time.sleep(5)





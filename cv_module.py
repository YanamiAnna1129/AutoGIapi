import time
import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import pytesseract
from .load_img import hp_templ, dice_templ, dice_templ_, element_templ
pytesseract.pytesseract.tesseract_cmd = r'D:\OCR\tesseract.exe'

def screenshot():
    window_title = '原神'
    app_window = gw.getWindowsWithTitle(window_title)[0]
    x_window, y_window, width, height = app_window.left, app_window.top, app_window.width, app_window.height
    shot = pyautogui.screenshot(region=(x_window, y_window, width, height))
    image_np = np.array(shot)
    img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image = img[29:930, 8:1608]
    return image


def get_image(func):
    def wrapper(*args, **kwargs):
        image = screenshot()
        return func(image, *args, **kwargs)

    return wrapper


@get_image
def get_hp(image, activate1: int, activate2: int) -> tuple[list[int], list[int]]:
    templ = hp_templ
    image_list = []
    hp_list = []
    health_list1 = [(544, 584), (717, 757), (892, 930)]
    name = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for ii, (xx, yy) in enumerate(health_list1):
        if activate1 != ii:
            gray = cv2.cvtColor(image[535:565, xx:yy], cv2.COLOR_BGR2GRAY)
        if activate1 == ii:
            gray = cv2.cvtColor(image[500:530, xx:yy], cv2.COLOR_BGR2GRAY)
        image_list.append(gray)
        # cv2.imshow("d", gray)
        # cv2.waitKey(0)
    for ii, (xx, yy) in enumerate(health_list1):
        if activate2 != ii:
            gray = cv2.cvtColor(image[141:174, xx:yy], cv2.COLOR_BGR2GRAY)
        if activate2 == ii:
            gray = cv2.cvtColor(image[175:221, xx:yy], cv2.COLOR_BGR2GRAY)
        image_list.append(gray)

    for i, original in enumerate(image_list):
        min_list = []
        for j, templ_num in enumerate(templ):
            res = cv2.matchTemplate(templ_num, original, cv2.TM_SQDIFF_NORMED)
            min_val, _, _, _ = cv2.minMaxLoc(res)
            min_list.append(min_val)
        min_value = min(min_list)
        min_index = min_list.index(min_value)
        hp_list.append(name[min_index])

    return hp_list[:3], hp_list[3:]


@get_image
def get_attach_ele(image, activate1: int, activate2: int) -> tuple[list[int], list[int]]:
    """
    获取角色的附着元素
    :return: 双方角色的附着元素列表
    """
    templ = element_templ
    ele_list = []
    element_mane = []
    ele_x = [(604, 657), (779, 832), (953, 1006)]
    # self_y = [(452, 489), (483, 523)]
    # enemy_y = [(129, 166), (108, 132)]
    for i, (x, y) in enumerate(ele_x):
        if activate1 != i:
            gray = cv2.cvtColor(image[483:523, x:y], cv2.COLOR_BGR2GRAY)
        if activate1 == i:
            gray = cv2.cvtColor(image[452:489, x:y], cv2.COLOR_BGR2GRAY)
        ele_list.append(gray)
        cv2.imshow("d", gray)
        cv2.waitKey(0)
    for i, (x, y) in enumerate(ele_x):
        if activate2 != i:
            gray = cv2.cvtColor(image[99:136, x:y], cv2.COLOR_BGR2GRAY)
        if activate2 == i:
            gray = cv2.cvtColor(image[129:166, x:y], cv2.COLOR_BGR2GRAY)
        ele_list.append(gray)
    name = [0, 1, 2, 4, 5, 6]
    for i, original in enumerate(ele_list):
        min_list = []
        for j, templ_num in enumerate(templ):
            res = cv2.matchTemplate(templ_num, original, cv2.TM_SQDIFF_NORMED)
            min_val, _, _, _ = cv2.minMaxLoc(res)
            min_list.append(min_val)
        min_value = min(min_list)
        min_index = min_list.index(min_value)
        element_mane.append(name[min_index])

    return element_mane[:3], element_mane[3:]


@get_image
def get_reroll_dice(image, need_dices: list[int]) -> list[int]:
    """
    识别需要重掷的骰子
    :return: 按照从左到右的顺序, 需要的值为0, 不需要的值为1
    """
    name = ['万能', '水', '火', '风', '雷', '草', '冰', '岩']
    need_dices = need_dices
    templ1 = image[318:355, 504:530]
    templ2 = image[318:355, 695:717]
    templ3 = image[318:355, 878:906]
    templ4 = image[318:355, 1067:1094]
    templ5 = image[523:560, 504:530]
    templ6 = image[523:560, 695:717]
    templ7 = image[523:560, 878:906]
    templ8 = image[523:560, 1067:1094]
    match = [templ1, templ2, templ3, templ4, templ5, templ6, templ7, templ8]
    templ = dice_templ

    need = [1, 1, 1, 1, 1, 1, 1, 1]
    for j, diagram in enumerate(match):
        lst = []
        for i, imgs in enumerate(templ):
            re = cv2.matchTemplate(imgs, diagram, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(re)
            lst.append(min_val)

        min_value = min(lst)
        min_index = lst.index(min_value)
        print(name[min_index] + f' 为最佳匹配元素')
        if min_index in need_dices:
            need[j] = 0

    return need


@get_image
def get_current_dice(image, need_dices: list[int], n: int) -> list[int]:
    """
    获取当前可用的骰子
    :return: 可用骰子为1, 不可用为0
    """
    templ_1 = image[156:172, 1546:1565]
    templ_2 = image[194:209, 1546:1565]
    templ_3 = image[232:249, 1546:1565]
    templ_4 = image[270:287, 1546:1565]
    templ_5 = image[307:325, 1546:1565]
    templ_6 = image[346:363, 1546:1565]
    templ_7 = image[384:401, 1546:1565]
    templ_8 = image[422:439, 1546:1565]

    name = ['万能', '水', '火', '风', '雷', '草', '冰', '岩']
    need_element = need_dices
    for ele in need_dices:
        need_element.append(ele)

    match = [templ_1, templ_2, templ_3, templ_4, templ_5, templ_6, templ_7, templ_8]
    templ = dice_templ_

    need = [0, 0, 0, 0, 0, 0, 0, 0]
    for j, diagram in enumerate(match):
        if j < n:
            lst = []
            for i, imgs in enumerate(templ):
                re = cv2.matchTemplate(imgs, diagram, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(re)
                lst.append(min_val)

            min_value = min(lst)
            min_index = lst.index(min_value)
            print(name[min_index] + f' 为最佳匹配元素')

            if min_index in need_element:
                need[min_index] += 1

    return need


@get_image
def get_dice_num(image) -> int:
    """
    获取当前剩余骰子数量(行动点数)
    """
    gray = cv2.cvtColor(image[537:562, 56:76], cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 200, 225, cv2.THRESH_BINARY)
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(thresh, config=custom_config)
    print(f'INFO:当前剩余行动点数：{text}')
    if text != '':
        try:
            number = int(text)
            return number
        except:
            return 0
    else:
        print('WARMING:未识别到行动点数')
        return 0


@get_image
def get_activate(image) -> list[int]:
    best_position = []
    people_position = [(558, 687), (735, 864), (907, 1040)]
    people_position_y = [(484, 504), (377, 410)]
    for (y1, y2) in people_position_y:
        positions = []
        for x1_position, x2_position in people_position:
            gray = cv2.cvtColor(image[y1:y2, x1_position:x2_position], cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 224, 225, cv2.THRESH_BINARY_INV)
            white = np.sum(thresh == 0)
            positions.append(white)
            best = max(positions)
            best_position.append(positions.index(best))
    return best_position


@get_image
def judge_stage(image) -> str:
    gray = cv2.cvtColor(image[853:870, 119:180], cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 120, 225, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='chi_sim')
    return text


# 重投
@get_image
def judge_stage_pro(image):  # 重投
    gray = cv2.cvtColor(image[140:192, 700:900], cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 120, 225, cv2.THRESH_BINARY)

    # 应用一些形态学操作来减少噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='chi_sim')
    # print(f'识别到：{text}')
    return text


# 角色
@get_image
def judge_stage_pro_max(image):  # 角色
    gray = cv2.cvtColor(image[711:736, 1473:1566], cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 140, 225, cv2.THRESH_BINARY)

    # 应用一些形态学操作来减少噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='chi_sim')
    # print(f'识别到：{text}')
    return text


def judge() -> str:
    """
    判断当前的阶段
    :return: 行动阶段, 等待阶段, unknown, 重投阶段
    """
    response = judge_stage()

    if '行动' in response:
        print('INFO:识别到行动阶段，正在确认：5s')
        time.sleep(5)
        response = judge_stage()
        if '行动' in response:
            print('INFO:行动阶段——————————')
            return "行动阶段"
        else:
            print('WARMING:确认失败，当前阶段不为行动阶段')
    elif '等' in response:
        print('INFO:等待阶段——————————')
        time.sleep(1.5)
        return "等待阶段"

    else:
        print('INFO:未知阶段——————————')
        time.sleep(1.5)

        response2 = judge_stage_pro()
        if '重' in response2:
            print('INFO:识别到重投阶段，正在确认：2s')
            response2 = judge_stage_pro()
            if '重' in response2:
                print('INFO:重投阶段——————————')
                return "重投阶段"

        response3 = judge_stage_pro_max()
        if '角色' in response3:
            time.sleep(2)
            rr = judge_stage_pro_max()
            if '角色' in rr:
                print('INFO:选择角色——————————')
                return "选择角色"
        return "unknown"

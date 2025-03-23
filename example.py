import time
from AutoGIapi import *
import random

sure()
while True:
    state = get_state()

    if state == "重投阶段":
        q = get_reroll_dice(need_dices=[0])
        click_dice(q)
        time.sleep(5)

    if state == "行动阶段":

        a = get_activate()
        hp1, hp2 = get_hp(activate1=a[0], activate2=a[1])
        n = get_dice_num()
        e = get_current_dice(need_dices=[0], n=n)
        print(f"出战角色:{a},hp1:{hp1},hp2:{hp2}\n总骰子:{n},可用骰子:{e}")

        if n >= 3 and n != 0:
            action = random.randint(0, 1)
            if action == 0:
                if e < 3:
                    harmony(3 - e)
                click_skill(2)
            elif action == 1:
                c_list = [x for x in [0, 1, 2] if x != a[0]]
                c = random.choice(c_list)
                change(c)
        else:
            end()

        time.sleep(5)

    if state == "选择角色":
        change(random.randint(0, 2))
        time.sleep(5)

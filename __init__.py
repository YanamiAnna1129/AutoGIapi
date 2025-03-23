from . import cv_module
from . import gui_module
from .cv_module import get_hp, get_attach_ele, get_reroll_dice, get_current_dice, get_dice_num, get_activate, get_state
from .gui_module import screenshot, sure, clean, end, harmony, click_dice, click_skill, change

print("AutoGIapi is imported successfully")

__all__ = ["cv_module", "gui_module", "get_hp", "get_attach_ele", "get_reroll_dice", "get_current_dice", "get_dice_num",
           "get_activate", "get_state", "screenshot", "sure", "clean", "end", "harmony", "click_dice", "click_skill", "change"]

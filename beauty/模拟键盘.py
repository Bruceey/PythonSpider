import pyautogui
import time

# 参考使用链接 https://huaweicloud.csdn.net/63807a6cdacf622b8df88a0c.html


#最小化当前窗口
# pyautogui.hotkey('winleft', 'd')
pyautogui.hotkey('alt', 'space', 'n')

pyautogui.moveTo(50, 400, duration=0.25)
# pyautogui.moveTo(3450, 70, duration=0.25)
pyautogui.doubleClick()
time.sleep(1)
#最大化窗口
pyautogui.hotkey('alt', 'space', 'x')
time.sleep(1.5)

pyautogui.moveTo(400, 330, duration=0.25)
# pyautogui.moveTo(1300, 330, duration=0.25)
# # 滚动鼠标，正数向上
# for i in range(30):
#     pyautogui.scroll(-500)
#     time.sleep(.1)

# time.sleep(3)
pyautogui.click()

pyautogui.press('space')
time.sleep(1)

for _ in range(100):
    time.sleep(0.8)
    pyautogui.press('right')
    # pyautogui.press('down')



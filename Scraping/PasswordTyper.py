from pynput.keyboard import Key,Controller
import time
keyboard = Controller()
time.sleep(6)
for c in "username":
    keyboard.press(c)
    keyboard.release(c)
time.sleep(2)
keyboard.press(Key.tab)
keyboard.release(Key.tab)
time.sleep(2)
for c in "Password":
    keyboard.press(c)
    keyboard.release(c)
time.sleep(2)
keyboard.press(Key.enter)
keyboard.release(Key.enter)

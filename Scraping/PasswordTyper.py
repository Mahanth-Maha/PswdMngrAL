from pynput.keyboard import Key,Controller
import time
keyboard = Controller()

def in_Username(Uname):
    time.sleep(2)
    for c in Uname:
        keyboard.press(c)
        keyboard.release(c)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
def in_Password(pswd):
    time.sleep(2)
    for c in pswd:
        keyboard.press(c)
        keyboard.release(c)
    time.sleep(2)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
if __name__ == '__main__':
    in_Username("username@mail.com")
    in_Password("P@$$w0rd")

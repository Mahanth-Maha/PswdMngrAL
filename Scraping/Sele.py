import time
from getpass import getpass

from pynput.keyboard import Key, Controller
from selenium import webdriver

import OpenBrowser
import PasswordTyper

keyboard = Controller()

global driver


def Site_FaceBook(username, password):
    global driver
    driver = webdriver.Chrome(".\\WebDriver\\chromedriver.exe")
    driver.get("https://www.facebook.com/")
    username_textbox = driver.find_element_by_id("email")
    password_textbox = driver.find_element_by_id("pass")
    login_button = driver.find_element_by_name("login")
    username_textbox.send_keys(username)
    password_textbox.send_keys(password)
    login_button.submit()


def Site_Twitter(username, password):
    global driver
    driver = webdriver.Chrome(".\\WebDriver\\chromedriver.exe")
    driver.get("https://twitter.com/login/")
    username_textbox = driver.find_element_by_name("session[username_or_email]")
    password_textbox = driver.find_element_by_name("session[password]")
    login_button = driver.find_element_by_class_name("css-1dbjc4n")
    username_textbox.send_keys(username)
    password_textbox.send_keys(password)
    login_button.click()


def Site_Google(username, password):
    global driver
    driver = webdriver.Chrome(".\\WebDriver\\chromedriver.exe")
    driver.get("https://accounts.google.com/Login")
    username_textbox = driver.find_element_by_id("identifierId")
    username_textbox.send_keys(username)
    # login_button = driver.find_element_by_name("Vf*")
    # login_button.submit()
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(2)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    # password_textbox = driver.find_element_by_id("pass")
    # password_textbox.send_keys(password)


def Site_Instagram(username, password):
    global driver
    # Not Working as Expected
    driver = webdriver.Chrome(".\\WebDriver\\chromedriver.exe")
    driver.get("https://www.instagram.com/accounts/login/")
    # username_textbox = driver.find_element_by_name("username")
    # username_textbox.send_keys(username)
    # password_textbox = driver.find_element_by_name("password")
    # password_textbox.send_keys(password)
    # login_button = driver.find_element_by_class_name("Log In")
    # login_button.submit()
    time.sleep(2)
    for c in username:
        keyboard.press(c)
        keyboard.release(c)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(2)
    for c in password:
        keyboard.press(c)
        keyboard.release(c)
    time.sleep(2)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


if __name__ == '__main__':
    try:
        c = int(input("Select one of the Site For Auto Login :\n1.FaceBook\n2.Twitter\n3.Instagram\n4.Google\n5.Others\nEnter A Choice : "))
        username = input("Enter in your username: ")
        password = getpass("Enter your password: ")
        if (c == 1):
            Site_FaceBook(username, password)
        elif (c == 2):
            Site_Twitter(username, password)
        elif (c == 3):
            Site_Instagram(username, password)
        elif (c == 4):
            Site_Google(username, password)
        elif (c == 5):
            Addr = input("Enter Adress for login (Trys if possible):")
            OpenBrowser.open_browser(OpenBrowser.get_Address(Addr))
            time.sleep(6)
            PasswordTyper.in_Username(username)
            PasswordTyper.in_Password(password)
    except :
        print("Not an Integer")
        input()

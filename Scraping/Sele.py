import time
import webbrowser
from getpass import getpass

from pynput.keyboard import Key, Controller
from selenium import webdriver

keyboard = Controller()

class OpenBrowser:
    def get_Address(self, addr):
        if (addr != None):
            AddressOfLoginPage = addr
        else:
            AddressOfLoginPage = "https://www.facebook.com/login.php"
        return AddressOfLoginPage

    def open_browser(self, Address_Of_Login_Page):
        webbrowser.get('windows-default').open(str(Address_Of_Login_Page))


class PasswordTyper:
    keyboard = Controller()

    def in_Username(self, Uname):
        time.sleep(2)
        for un in Uname:
            self.keyboard.press(un)
            self.keyboard.release(un)
        time.sleep(2)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)

    def in_Password(self, pswd):
        time.sleep(2)
        for c in pswd:
            self.keyboard.press(c)
            self.keyboard.release(c)
        time.sleep(2)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)


class AutoFill:
    def __init__(self):
        pass

    driver = None

    def Site_FaceBook(self, username, password):
        global driver
        self.driver = webdriver.Chrome(".\\WebDriver\\chromedriver.exe")
        self.driver.get("https://www.facebook.com/")
        username_textbox = self.driver.find_element_by_id("email")
        password_textbox = self.driver.find_element_by_id("pass")
        login_button = self.driver.find_element_by_name("login")
        username_textbox.send_keys(username)
        password_textbox.send_keys(password)
        login_button.submit()
        return 0

    def Site_Twitter(self, username, password):
        driver = webdriver.Chrome(".\\WebDriver\\chromedriver.exe")
        driver.get("https://twitter.com/login/")
        username_textbox = driver.find_element_by_name("session[username_or_email]")
        password_textbox = driver.find_element_by_name("session[password]")
        login_button = driver.find_element_by_class_name("css-1dbjc4n")
        username_textbox.send_keys(username)
        password_textbox.send_keys(password)
        login_button.click()
        return 0

    def Site_Google(self, username, password):
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
        return 0

    def Site_Instagram(self, username, password):
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
        return 0

    sites = ["FaceBook", "Twitter", "Instagram", "Google"]

    def FillIn(self, site, username, password):
        if site in self.sites:
            c = self.sites.index(site)
        else:
            c = 5
        if (c == 1):
            self.Site_FaceBook(username, password)
        elif (c == 2):
            self.Site_Twitter(username, password)
        elif (c == 3):
            self.Site_Instagram(username, password)
        elif (c == 4):
            self.Site_Google(username, password)
        elif (c == 5):
            Addr = site
            OpenBrowser.open_browser(OpenBrowser.get_Address(Addr))
            time.sleep(6)
            PasswordTyper.in_Username(username)
            PasswordTyper.in_Password(password)
        return 0

if __name__ == '__main__':
    try:
        c = int(input(
            "Select one of the Site For Auto Login :\n1.FaceBook\n2.Twitter\n3.Instagram\n4.Google\n5.Others\nEnter A Choice : "))
        username = input("Enter in your username: ")
        password = getpass("Enter your password: ")
        A = AutoFill
        A.FillIn("https://www.instagram.com/accounts/login/",username,password)
    except:
        #print("Not an Integer")
        input("Invalid input Press Any Key to exit...")

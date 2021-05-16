import webbrowser
import time
import PasswordTyper

def get_Address(addr):
  if(addr != None):
    AddressOfLoginPage = addr
  else:
    AddressOfLoginPage = "https://www.facebook.com/login.php"
  return AddressOfLoginPage
    
def open_browser(Address_Of_Login_Page):
  webbrowser.get('windows-default').open(str(Address_Of_Login_Page))

if __name__ == '__main__':
  open_browser(get_Address(None))
  time.sleep(6)
  PasswordTyper.in_Username("username@mail.com")
  PasswordTyper.in_Password("P@$$w0rd")

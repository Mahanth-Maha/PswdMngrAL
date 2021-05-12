import webbrowser
import time

def get_Address(addr):
  if(addr != None):
    AddressOfLoginPage = addr
  else:
    AddressOfLoginPage = "https://login.salesforce.com/"
  return AddressOfLoginPage
    
def open_browser(Address_Of_Login_Page):
  webbrowser.get('windows-default').open(str(Address_Of_Login_Page))

if __name__ == '__main__':
  open_browser(get_Address(None))
  time.sleep(1)
  

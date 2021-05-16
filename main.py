# Main File to perform all operations
from getpass import getpass

from securing.Securing import AES
from DataBase.DataBaseFile import DataBaseRecords
from Scraping.Sele import AutoFill
from tkinter import Tk

class PasswordManager:
    def __init__(self):
        pass

    sites = ["FaceBook", "Twitter", "Instagram", "Google"]

    def New_Record(self):
        S = int(
            input("Pre Available Sites \t1.FaceBook\t2.Twitter\n3.Instagram\n4.Google\n5.Other Site\n Select a Site:"))
        if S in (1, 2, 3, 4):
            Site = self.sites[S]
        else:
            addr = input("Enter Login Site Address https://")
            Site = "https://" + addr

        Username = input("Enter the ID / Mail / Username :")
        # to Charan : Construct a Class in securing Folder as Filename : Securing.py -> with class name : AES and methods :
        # 1. Encrypt - takes password gives Encrypted text
        # 2. Decrypt - takes Encrypted text gives password
        Password = AES.Encrypt(getpass("Enter the Password :"))

        # to Shivatej : Construct a Class in Database Folder as Filename : DataBaseFile.py -> with class name : DataBaseRecords and methods :
        # 1. insert_records - takes (username,password,site) gives success - 0 or fail - 1
        # 2. get_records - takes (username,site) gives (username,password,site)
        DataBaseRecords.insert_record(Username, Password, Site)

    def Get_Record(self):
        S = int(
            input("Pre Available Sites \t1.FaceBook\t2.Twitter\n3.Instagram\n4.Google\n5.Other Site\n Select a Site:"))
        if S in (1, 2, 3, 4):
            Site = self.sites[S]
        else:
            addr = input("Enter Login Site Address https://")
            Site = "https://" + addr
        Username = input("Enter the ID / Mail / Username :")
        PasswordEncrypted,Site2 = DataBaseRecords.get_records(Username, Site)
        Password = AES.Decrypt(PasswordEncrypted)
        Err = True
        while(Err):
            try:
                select = int(input("\n1 : Copy Password to clipboard \n2 : Open in browser\n3 : Dicard Password \nEnter (1/2) :"))
                if(select == 1 ):
                    print(Password)
                    Err = False
                elif select == 2:
                    AutoFill.FillIn(Site2,Username,Password)
                    Err = False
                elif select == 3:
                    Err = False
                else:
                    print("invalid Input")
            except:
                print("invalid Input")
    def ListRecords(self):
        recordsAvail = DataBaseRecords.get_list_of_records()
        for i in recordsAvail:
            print(i, " - ", recordsAvail[i])

if __name__ == '__main__':
    Master_Password = int(input("Enter Master Password : "))
    if(Master_Password == "PswdMgnrAL"):
        User = PasswordManager()
        Run = True
        print("-> Welcome User <-")
        while(Run):
            option = input("Options Avaliable\n 1. Insert New Password \n2. Retrive a Password \n3. List Avaliable Passwords For\n4.Exit\nSelect an Option :")
            if(int(option) == 1):
                User.New_Record()
            elif(int(option) ==2 ):
                User.Get_Record()
            elif (int(option) == 3):
                User.ListRecords()
            elif (int(option) == 4):
                Run = False
            else:
                print("Invalid input")







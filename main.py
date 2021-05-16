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
    siteAddr = dict(FaceBook='https://www.facebook.com/', Twitter='https://twitter.com/login/',
                    Instagram='https://www.instagram.com/accounts/login/',
                    Google='https://accounts.google.com/Login')

    # noinspection PyArgumentList
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
        RawPassCode = getpass("Enter the Password :")
        AESObj = AES()
        EncryptPassword = AESObj.Encrypt(RawPassCode)

        # to Shivatej : Construct a Class in Database Folder as Filename : DataBaseFile.py -> with class name : DataBaseRecords and methods :
        # 1. insert_records - takes (username,password,site) gives success - 0 or fail - 1
        # 2. get_records - takes (username,site) gives (username,password,site)
        DataBaseObj = DataBaseRecords()
        DataBaseObj.insert_record(Username, EncryptPassword, self.siteAddr[Site])

    def Get_Record(self):
        S = int(
            input("\nPre Available Sites \t1.FaceBook\t2.Twitter\t3.Instagram\t4.Google\t5.Other Site\n Select a Site:"))
        if S in (1, 2, 3, 4):
            Site = self.sites[S]
        else:
            addr = input("Enter Login Site Address https://")
            Site = "https://" + addr
        Username = input("Enter the ID / Mail / Username :")
        DataBaseObj = DataBaseRecords()
        PasswordEncrypted,Site2 = DataBaseObj.get_records(Username, self.siteAddr[Site])
        AESObj = AES()
        Password = AESObj.Decrypt(PasswordEncrypted)
        Err = True
        while(Err):
            try:
                select = int(input("\n1 : Copy Password to clipboard \n2 : Open in browser\n3 : Dicard Password \nEnter (1/2) :"))
                if(select == 1 ):
                    r = Tk()
                    r.withdraw()
                    r.clipboard_clear()
                    r.clipboard_append(Password)
                    r.update()
                    r.destroy()
                    Err = False
                elif select == 2:
                    AutoFillObj = AutoFill()
                    AutoFillObj.FillIn(Site2,Username,Password)
                    Err = False
                elif select == 3:
                    Err = False
                else:
                    print("invalid Input")
            except:
                print("invalid Input")
    def ListRecords(self):
        DataBaseObj = DataBaseRecords()
        recordsAvail = DataBaseObj.get_list_of_records()
        print("\nUsername\t\tSite")
        print('-'*25)
        for i in recordsAvail:
            print(i, "\t\t", recordsAvail[i])
        print()

if __name__ == '__main__':
    Tried = 0
    Try = True
    while(Try):
        Master_Password = input("Enter Master Password : ")
        if(Master_Password == "PswdMngrAL"):
            User = PasswordManager()
            Run = True
            print("-> Welcome User <-")
            while(Run):
                option = input("\nOptions Avaliable\n\t1. Insert New Password \n\t2. Retrive a Password \n\t3. List Avaliable Passwords For\n\t4.Exit\nSelect an Option :")
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
        else:
            Tried +=1
            if(Tried >= 3):
                Try = False
                input("\n\tIncorret trails Limit Exceeded...Bye (Press Enter)")
            else:
                print("\t\tINCORRECT PASSWORD\n\nTrails Left :", 3 - Tried,"\n")












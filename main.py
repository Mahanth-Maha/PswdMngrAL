# Main File to perform all operations
from getpass import getpass
from tkinter import Tk

from CreateMasterPswd import MasterPasswordGen
from DataBase.DataBaseFile import DataBaseRecords
from Scraping import Sele
from securing.Securing import AES


class PasswordManager:
    def __init__(self):
        pass

    sites = ["FaceBook", "Twitter", "Instagram", "Google"]
    siteAddr = dict(FaceBook='https://www.facebook.com/', Twitter='https://twitter.com/login/',
                    Instagram='https://www.instagram.com/accounts/login/',
                    Google='https://accounts.google.com/Login')
    # noinspection PyArgumentList
    def New_Record(self):
        try:
            S = int(
                input("Pre Available Sites \n1.FaceBook\n2.Twitter\n3.Instagram\n4.Google\n5.Other Site\n Select a Site:"))
            if S in (1, 2, 3, 4):
                Site = self.sites[S-1]
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
        except:
            print("INVALID Option")
    def Get_Record(self):
        try:
            S = int(
                input("\nPre Available Sites \t1.FaceBook\t2.Twitter\t3.Instagram\t4.Google\t5.Other Site\n Select a Site:"))
            if S in (1, 2, 3, 4):
                Site = self.sites[S-1]
            else:
                addr = input("Enter Login Site Address https://")
                Site = "https://" + addr
            Username = input("Enter the ID / Mail / Username :")
            DataBaseObj = DataBaseRecords()
            PasswordEncrypted, Site2 = DataBaseObj.get_records(Username, self.siteAddr[Site])
            AESObj = AES()
            Password = AESObj.Decrypt(PasswordEncrypted)
            Err = True
            while (Err):
                try:
                    select = int(input("\n1 : Copy Password to clipboard \n2 : Open in browser\n3 : Discard Password \nEnter (1/2/3) :"))
                    print(select)
                    if (select == 1):
                        r = Tk()
                        r.withdraw()
                        r.clipboard_clear()
                        r.clipboard_append(Password)
                        r.update()
                        r.destroy()
                        Err = False
                    elif(select == 2):
                        Sele.FillIn(Site2, Username, Password)
                        Err = False
                    elif(select == 3):
                        Err = False
                    else:
                        print("invalid Input")
                except:
                    print("invalid Input Only Number allowed")
        except:
            print("Invalid Input")

    def ListRecords(self):
        DataBaseObj = DataBaseRecords()
        recordsAvail = DataBaseObj.get_list_of_records()
        print("\nUsername\t\tSite")
        print('-' * 25)
        for i in recordsAvail:
            print(i, "\t\t", recordsAvail[i])
        print()


def LogIn():
    Tried = 0
    Try = True
    while (Try):
        Master_Password = getpass("Enter Master Password : ")
        token = UserSession.Verify_Password(Master_Password)
        if (token == 0):
            User = PasswordManager()
            Run = True
            print("-> Welcome " + UserSession.get_username() + " <-")
            while (Run):
                option = input(
                    "\nOptions Avaliable\n\t1. Insert New Password \n\t2. Retrive a Password \n\t3. List Avaliable Passwords For\n\t4. Delete Master Password\n\t5. Exit\nSelect an Option :")
                if (int(option) == 1):
                    User.New_Record()
                elif (int(option) == 2):
                    User.Get_Record()
                elif (int(option) == 3):
                    User.ListRecords()
                elif(int(option)==4):
                    UserSession.DeleteMP()
                    Run = False
                    Try = False
                elif (int(option) == 5):
                    Run = False
                    Try = False
                    print("Have a Nice and Secure Day "+UserSession.get_username())
                else:
                    print("Invalid input")
        else:
            Tried += 1
            if (Tried >= 3):
                Try = False
                input("\n\tIncorret trails Limit Exceeded...Bye (Press Enter)")
            else:
                print("\t\tINCORRECT PASSWORD\n\nTrails Left :", 3 - Tried, "\n")


if __name__ == '__main__':
    UserSession = MasterPasswordGen()
    if(UserSession.If_MasterPassNotCreated() == 1):
        UserSession.CreateMP()
        print("MasterPassword Created Succesfully... Please Restart To use")
    else:
        LogIn()
    input("\n\n\n\tPress Any Key to Exit . . . ")

# Main File to perform all operations
from getpass import getpass
from tkinter import Tk

from CreateMasterPswd import MasterPasswordGen
from DataBase.DataBaseFile import DataBaseRecords
from Scraping import Sele
from securing.Securing import AES_Salted_Crypted


class PasswordManager:
    def __init__(self, Session_Password):
        self.Session_Password = Session_Password

    sites = ["FaceBook", "Twitter", "Instagram", "Google"]
    siteAddr = dict(FaceBook='https://www.facebook.com/', Twitter='https://twitter.com/login/',
                    Instagram='https://www.instagram.com/accounts/login/',
                    Google='https://accounts.google.com/Login')

    # noinspection PyArgumentList
    def New_Record(self):
        try:
            S = int(
                input(
                    "Pre Available Sites \n1.FaceBook\n2.Twitter\n3.Instagram\n4.Google\n5.Other Site\n Select a Site:"))
            if S in (1, 2, 3, 4):
                Site = self.sites[S - 1]
                address_of_site = self.siteAddr[Site]
            else:
                addr = input("Enter Login Site Address https://")
                Site = "https://" + addr
                address_of_site = Site
            Username = input("Enter the ID / Mail / Username :")
            RawPassCode = getpass("Enter the Password :")

            AESObj = AES_Salted_Crypted()
            EncryptPassword = AESObj.encrypt(RawPassCode, self.Session_Password)

            DataBaseObj = DataBaseRecords()
            DataBaseObj.InsertInto(EncryptPassword, Username, address_of_site)
        except:
            print("INVALID Option")

    def Get_Record(self):
        Err = True
        try:
            S = int(input(
                "\nPre Available Sites \t1.FaceBook\t2.Twitter\t3.Instagram\t4.Google\t5.Other Site\n Select a Site:"))
            if S in (1, 2, 3, 4):
                Site = self.sites[S - 1]
                address_of_site = self.siteAddr[Site]
            else:
                addr = input("Enter Login Site Address https://")
                Site = "https://" + addr
                address_of_site = Site
            Username = input("Enter the ID / Mail / Username :")
            DataBaseObj = DataBaseRecords()
            PasswordEncrypted = DataBaseObj.get_record(Username, address_of_site)
            AESObj = AES_Salted_Crypted()
            if (len(PasswordEncrypted) != 0):
                Password = AESObj.decrypt(PasswordEncrypted, self.Session_Password)
            else:
                print("No Such Record found !")
                Err = False
            while (Err):
                try:
                    select = int(input(
                        "\n1 : Copy Password to clipboard \n2 : Open in browser\n3 : Discard Password \nEnter (1/2/3) :"))
                    Password = Password.decode('UTF-8')
                    if (select == 1):
                        r = Tk()
                        r.withdraw()
                        r.clipboard_clear()
                        r.clipboard_append(Password)
                        r.update()
                        r.destroy()
                        print('Password : ', Password)
                        Err = False
                    elif (select == 2):
                        Sele.FillIn(Site, Username, Password)
                        Err = False
                    elif (select == 3):
                        Err = False
                    else:
                        print("invalid Input")
                except:
                    print("invalid Input Only Number allowed")
        except:
            print("Invalid Input")

    def ListRecords(self):
        DataBaseObj = DataBaseRecords()
        recordsAvail = DataBaseObj.All_List()
        print("\nUsername\t\tSite")
        print('-' * 10 + '\t\t' + '-' * 30)
        for i in recordsAvail:
            print(i[0], "\t\t", i[1])
        print()

    def del_one_record(self):
        Username = input("Enter the ID / Mail / Username :")
        S = int(input(
            "\nPre Available Sites \t1.FaceBook\t2.Twitter\t3.Instagram\t4.Google\t5.Other Site\n Select a Site:"))
        if S in (1, 2, 3, 4):
            Site = self.sites[S - 1]
            address_of_site = self.siteAddr[Site]
        else:
            addr = input("Enter Login Site Address https://")
            Site = "https://" + addr
            address_of_site = Site
        User_Passwords = DataBaseRecords()
        User_Passwords.del_record(Username, address_of_site)


def LogIn():
    Tried = 0
    Try = True
    while (Try):
        Master_Password = getpass("Enter Master Password : ")
        token = UserSession.Verify_Password(Master_Password)
        if (token == 0):
            User = PasswordManager(Master_Password)
            User_Passwords = DataBaseRecords()
            Run = True
            print("\t\t\t-> Welcome " + UserSession.get_username() + " <-")
            while (Run):
                option = input(
                    "\nOptions Avaliable\n\t1. Insert New Password \n\t2. Retrive a Password \n\t3. List Avaliable Passwords For\n\t4. Delete A Saved Password\n\t5.Delete All Saved Passwords\n\t6. Delete Master Password\n\t0. Exit\nSelect an Option :")
                if (int(option) == 1):
                    User.New_Record()
                elif (int(option) == 2):
                    User.Get_Record()
                elif (int(option) == 3):
                    User.ListRecords()
                elif (int(option) == 4):
                    User.del_one_record()
                elif (int(option) == 5):
                    User_Passwords.del_All_Records()
                elif (int(option) == 6):
                    status = UserSession.DeleteMP()
                    if (status == 0):
                        User_Passwords.del_All_Records()
                        Run = False
                        Try = False
                elif (int(option) == 0):
                    Run = False
                    Try = False
                    print("\n\n\tHave a Nice and Secure Day " + UserSession.get_username())
                else:
                    print("Invalid input")
        else:
            Tried += 1
            if (Tried >= 3):
                Try = False
                print("\n\tIncorret trails Limit Exceeded...Bye")
            else:
                print("\t\tINCORRECT PASSWORD\n\nTrails Left :", 3 - Tried, "\n")


if __name__ == '__main__':
    UserSession = MasterPasswordGen()
    if (UserSession.If_MasterPassNotCreated() == 1):
        UserSession.CreateMP()
        print("MasterPassword Created Succesfully... Please Restart To use")
    else:
        LogIn()
    input("\n\n\n\tPress Any Key to Exit . . . ")

import sqlite3 as lite
import hashlib
import pyperclip
import time
import os
from getpass import getpass
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

CLIPBOARDTIME = 30

class PasswordManager:
    def __init__(self, Session_Password):
        self.Session_Password = Session_Password

    sites = ["FaceBook", "Twitter", "Instagram", "Google"]
    siteAddr = dict(FaceBook='https://www.facebook.com/',
                    Twitter='https://twitter.com/login/',
                    Instagram='https://www.instagram.com/accounts/login/',
                    Google='https://accounts.google.com/Login')

    # noinspection PyArgumentList
    def New_Record(self):
        try:
            S = int(input(
                "Pre Available Sites \t1.FaceBook\t2.Twitter\t3.Instagram\t4.Google\t5.Other Site\t Select a Site:"))
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
            print("Invalid Option")

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
                        "\n1 : Copy Password to Clipboard (It will be Erased in 30 seconds) \n2 : Discard Password \nEnter (1/2) :"))
                    Password = Password.decode('UTF-8')
                    if (select == 1):
                        pyperclip.copy(Password)
                        print("Password copied to clip board - clip board will be cleared in 30 seconds\n")
                        time.sleep(CLIPBOARDTIME)
                        pyperclip.copy("")
                        Err = False
                    elif (select == 2):
                        Password = None
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
        if len(recordsAvail) != 0:
            print("\nUsername\t\tSite")
            print('-' * 10 + '\t\t' + '-' * 30)
            for i in recordsAvail:
                print(i[0], "\t\t", i[1])
            print()
        else:
            print("\nNo Records found\n")

    def del_one_record(self):
        User_Passwords = DataBaseRecords()
        if len(User_Passwords.FetchTable()) != 0:
            S = int(input(
                "\nPre Available Sites \t1.FaceBook\t2.Twitter\t3.Instagram\t4.Google\t5.Other Site\n Select a Site:"))
            Username = input("Enter the ID / Mail / Username :")
            if S in (1, 2, 3, 4):
                Site = self.sites[S - 1]
                address_of_site = self.siteAddr[Site]
            else:
                addr = input("Enter Login Site Address https://")
                Site = "https://" + addr
                address_of_site = Site
            User_Passwords.del_record(Username, address_of_site)
        else:
            print("No Records to delete")



def LogIn():
    Tried = 0
    Try = True
    print("\n\t\tHello ",UserSession.get_username(),"\n\tWelcome back to Password Manager\n")
    while (Try):
        Master_Password = getpass("Enter Master Password : ")
        token = UserSession.Verify_Password(Master_Password)
        if (token == 0):
            User = PasswordManager(Master_Password)
            User_Passwords = DataBaseRecords()
            Run = True
            print("\t\t\t-> Welcome " + UserSession.get_username() + " <-")
            while (Run):
                try:
                    option = input(
                        "\nOptions Avaliable\n\t1. Insert New Password \n\t2. Retrive a Password \n\t3. List Avaliable Passwords For\n\t4. Delete A Saved Password\n\t5. Delete All Saved Passwords\n\t6. Delete Master Password\n\t0. Exit\nSelect an Option :")
                    if (int(option) == 1):
                        User.New_Record()
                    elif (int(option) == 2):
                        User.Get_Record()
                    elif (int(option) == 3):
                        User.ListRecords()
                    elif (int(option) == 4):
                        User.del_one_record()
                    elif (int(option) == 5):
                        del_all = input("\aAre you sure (Y/N): ")
                        if del_all in ('Y','y','Yes','yes'):
                            User_Passwords.del_All_Records()
                            print("ALL Passwords Deleted")
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
                except:
                    print("\nYou have entered invalid input Please select from Options")
        else:
            Tried += 1
            if (Tried >= 3):
                Try = False
                print("\n\t\a\aIncorrect trails Limit Exceeded...Bye")
            else:
                print("\t\t\aINCORRECT PASSWORD\n\nTrails Left :", 3 - Tried, "\n")


class MasterPasswordDataBase:
    def __init__(self):
        self.CreateDB()

    con = lite.connect('MasterPasswordDataBase.db')

    def CreateDB(self):
        cur = self.con.cursor()
        already_exists = self.tables_in_sqlite_db()
        if len(already_exists) == 0:
            try:
                print("\n\ninstalling...")
                os.system("pip3 install selenium pynput PyCryptodome pyperclip")
            except:
                print("\n\n\n\aConnect to Internet and Run Again\n\n\n")
            cur.execute("CREATE TABLE MasterPassword(Id INT Primary Key, User TEXT,Hash TEXT)")
        elif len(already_exists) == 1:
            # print("DB Created Already Exist")
            pass
        else:
            for i in already_exists:
                cur.execute('DROP TABLE')
            self.CreateDB()

    def InsertInto(self, hash, username):
        cur = self.con.cursor()
        all_ids = self.AllIdsInTable()
        if len(all_ids) == 0:
            SQL = "INSERT INTO MasterPassword VALUES(1,'" + username + "','" + hash + "')"
            # print(SQL)
            cur.execute(SQL)
            # print("Row inserted")
            self.con.commit()
        else:
            # print("ALready Stored")
            pass

    def AllIdsInTable(self):
        cur = self.con.cursor()
        cur.execute("SELECT ID FROM MasterPassword")
        ids = cur.fetchall()
        return ids

    def FetchHash(self):
        cur = self.con.cursor()
        cur.execute('SELECT Hash,User FROM MasterPassword')
        rows = cur.fetchall()
        if len(rows) != 0:
            return rows[0]
        return rows

    def tables_in_sqlite_db(self):
        cursor = self.con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [
            v[0] for v in cursor.fetchall()
            if v[0] != "sqlite_sequence"
        ]
        cursor.close()
        return tables

    def DeleteEntry(self):
        cur = self.con.cursor()
        cur.execute('DELETE FROM MasterPassword')
        self.con.commit()


class RSA:
    def PasswordHasher(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


class MasterPasswordGen:

    def CreateMP(self):
        # setup.Install_dependencies()
        print("MasterPassword - A single Password for All Passwords \n\n"
              "--- Creating A Master Password ---\n\t* We can't Retrive Master Password if you lost it, so please not it down\n\t"
              "* You can only login in with Master password Created \n\t* Password will not visible as you type\n\tDont give spaces in end or start unnecessarly")
        password_1 = getpass("Enter You Master PassWord :")
        password_2 = getpass("Enter Again :")
        if (password_1 == password_2 and password_1 != ''):
            username = input("Enter User-Name :")
            Hasher = RSA()
            hash_generated = Hasher.PasswordHasher(password_1)
            HashDB = MasterPasswordDataBase()
            HashDB.CreateDB()
            HashDB.InsertInto(hash_generated, username)
        else:
            print("\n\aSorry password not matched Try Again")

    def DeleteMP(self):
        print(
            "\a\nMasterPassword - A single Password for All Passwords \n\nWARNING : If you delete this You will lost All saved passwords also")
        agree = input("\n\nDelete Master Password (Y/N) :")
        if agree in ('Y', 'Yes', 'YES', 'y', 'yes'):
            HashDB = MasterPasswordDataBase()
            HashDB.DeleteEntry()
            return 0
        return 1

    def Verify_Password(self, PasswordReEntry):
        Hasher = RSA()
        hash_generated = Hasher.PasswordHasher(PasswordReEntry)
        HashDB = MasterPasswordDataBase()
        in_table = HashDB.FetchHash()
        if len(in_table) != 0:
            PassHash, UserName = in_table
            if (hash_generated == PassHash):
                return 0
            else:
                return 1

    def If_MasterPassNotCreated(self):
        HashDB = MasterPasswordDataBase()
        in_table = HashDB.FetchHash()
        if len(in_table) != 0:
            return 0
        return 1

    def get_username(self):
        HashDB = MasterPasswordDataBase()
        in_table = HashDB.FetchHash()
        if len(in_table) != 0:
            PassHash, UserName = in_table
            return UserName
        return None


class DataBaseRecords:
    def __init__(self):
        self.CreateDB()

    con = lite.connect('PasswordsDataBase.db')

    def CreateDB(self):
        cur = self.con.cursor()
        already_exists = self.tables_in_sqlite_db()
        if len(already_exists) == 0:
            cur.execute(
                "CREATE TABLE Passwords(username TEXT,Site TEXT,cipher_text TEXT,salt TEXT,nonce TEXT,tag TEXT,PRIMARY KEY(username,Site))")
        elif len(already_exists) == 1:
            pass
        else:
            for i in already_exists:
                cur.execute('DROP TABLE;')
            self.CreateDB()

    def InsertInto(self, enc_dict, username, site):
        cur = self.con.cursor()
        record = self.get_record(username, site)
        if len(record) == 0:
            SQL = "INSERT INTO Passwords VALUES('" + username + "','" + site + "','" + enc_dict['cipher_text'] + "','" + \
                  enc_dict['salt'] + "','" + enc_dict['nonce'] + "','" + enc_dict['tag'] + "');"
            # print(SQL)
            cur.execute(SQL)
            print("Password Saved !")
            self.con.commit()
        else:
            print("Username,Password for this Site is ALready Stored !")
            pass

    def All_List(self):
        cur = self.con.cursor()
        cur.execute("SELECT username,site FROM Passwords;")
        pks = cur.fetchall()
        return pks

    def FetchTable(self):
        cur = self.con.cursor()
        cur.execute('SELECT * FROM Passwords;')
        rows = cur.fetchall()
        return rows

    def get_record(self, username, site):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Passwords WHERE username = '" + username + "' AND site = '" + site + "';")
        row = cur.fetchall()
        enc_dict = dict()
        if (len(row) != 0):
            tup = row[0]
            enc_dict = dict()
            enc_dict['cipher_text'] = tup[2]
            enc_dict['salt'] = tup[3]
            enc_dict['nonce'] = tup[4]
            enc_dict['tag'] = tup[5]
        return enc_dict

    def del_record(self, username, site):
        cur = self.con.cursor()
        if len(self.get_record(username,site)) != 0:
            cur.execute("DELETE FROM Passwords WHERE username = '" + username + "' AND site = '" + site + "';")
            self.con.commit()
            print("Password DELETED")
        else:
            print("No such Record to Delete")

    def tables_in_sqlite_db(self):
        cursor = self.con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [
            v[0] for v in cursor.fetchall()
            if v[0] != "sqlite_sequence"
        ]
        cursor.close()
        return tables

    def del_All_Records(self):
        cur = self.con.cursor()
        cur.execute('DELETE FROM Passwords')
        self.con.commit()


class AES_Salted_Crypted:
    def encrypt(self, plain_text, password):
        salt = get_random_bytes(AES.block_size)
        private_key = hashlib.scrypt(password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        cipher_config = AES.new(private_key, AES.MODE_GCM)
        cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
        return {
            'cipher_text': b64encode(cipher_text).decode('utf-8'),
            'salt': b64encode(salt).decode('utf-8'),
            'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
            'tag': b64encode(tag).decode('utf-8')
        }

    def decrypt(self, enc_dict, password):
        salt = b64decode(enc_dict['salt'])
        cipher_text = b64decode(enc_dict['cipher_text'])
        nonce = b64decode(enc_dict['nonce'])
        tag = b64decode(enc_dict['tag'])
        private_key = hashlib.scrypt(password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(cipher_text, tag)
        return decrypted


if __name__ == '__main__':
    UserSession = MasterPasswordGen()
    if (UserSession.If_MasterPassNotCreated() == 1):
        UserSession.CreateMP()
        print("MasterPassword Created Succesfully... Please Restart To use")
    else:
        LogIn()
    input("\n\n\n\tPress Any Key to Exit . . . ")

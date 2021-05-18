import hashlib
import sqlite3 as lite
from getpass import getpass

import setup

class MasterPasswordDataBase:
    def __init__(self):
        self.CreateDB()

    con = lite.connect('DataBase/MasterPasswordDataBase.db')

    def CreateDB(self):
        cur = self.con.cursor()
        already_exists = self.tables_in_sqlite_db()
        if len(already_exists) == 0:
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
        #setup.Install_dependencies()
        print("MasterPassword - A single Password for All Passwords \n\n"
              "--- Creating A Master Password ---\n\t* We can't Retrive Master Password if you lost it, so please not it down\n\t"
              "* You can only login in with Master password Created \n\t* Password will not visible as you type\n\tDont give spaces in end or start unnecessarly")
        password_1 = getpass("Enter You Master PassWord :")
        password_2 = getpass("Enter Again :")
        if (password_1 == password_2 and password_1 != ''):
            username = input("Enter User-Name :")
            Hasher = RSA()
            hash_generated = Hasher.PasswordHasher(password_1)
            #print(hash_generated)
            HashDB = MasterPasswordDataBase()
            HashDB.CreateDB()
            HashDB.InsertInto(hash_generated, username)
        else:
            print("\nSorry password not matched Try Again")

    def DeleteMP(self):
        print(
            "\nMasterPassword - A single Password for All Passwords \n\nWARNING : If you delete this You will lost All saved passwords also")
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

if __name__ == '__main__':
    # Hasher = RSA()
    # hash_generated = Hasher.PasswordHasher("Maha3")
    UserSession = MasterPasswordGen()
    password_3 = getpass("Enter MP :")
    print(UserSession.Verify_Password(password_3))
    # k = MasterPasswordDataBase()
    # k.CreateDB()
    # k.InsertInto(hash_generated,"maha")
    # print(k.tables_in_sqlite_db())
    # in_table =k.FetchHash()
    # if len(in_table) !=0:
    #    PassHash, UserName = in_table
    #    print(PassHash,UserName)
    # k.DeleteEntry()
    input()

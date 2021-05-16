import sqlite3 as lite


class DataBaseRecords:
    def __init__(self):
        self.CreateDB()

    con = lite.connect('DataBase/PasswordsDataBase.db')

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
            # print("Row inserted")
            self.con.commit()
        else:
            # print("ALready Stored")
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
        cur.execute("DELETE FROM Passwords WHERE username = '" + username + "' AND site = '" + site + "';")
        self.con.commit()

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


if __name__ == '__main__':
    a = DataBaseRecords()
    a.CreateDB()
    a.InsertInto({'cipher_text': '/WniTBgY61iKi+/JGx19LByxmdw+0Z+RX50=', 'salt': '1gP/RWke6RxIs4Tmt40LgQ==',
                  'nonce': 'X0BSBNb8Tfr/XjOlUQi5sg==', 'tag': '4HCzJz2D4iD3YnaGoh3T0Q=='}
                 , "maha", 'Google')
    a.InsertInto({'cipher_text': '/WniTBgY61iKi+/JGx19LByxmdw+0Z+RX50=', 'salt': '1gP/RWke6RxIs4Tmt40LgQ==',
                  'nonce': 'X0BSBNb8Tfr/XjOlUQi5sg==', 'tag': '4HCzJz2D4iD3YnaGoh3T0Q=='}
                 , "maha", 'Insta')
    k = a.get_record("maha", 'Google')
    print(k)
    # a.del_record("maha",'Google')
    table = a.FetchTable()
    print(table)
    a.del_All_Records()
    table = a.FetchTable()
    print(table)

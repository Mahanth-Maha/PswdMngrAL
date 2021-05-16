

class DataBaseRecords:

    def get_records(self ,username,site):
        password ="albfh12$%9daduhsdf%#Qvw$$8n0934hpovhf2"
        print(password,site)
        return (password,site)

    def insert_record(self, Username, Password, Site):
        print("inserted",Username,Password,Site)
        return 1

    def get_list_of_records(self):
        out = {'username1':'site1','username2':'site2','username3':'site3','username4':'site4'}
        return out


import psycopg2

from config.dbconfig import pg_config

class Medicine:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)
    
    def getAllMedicine(self):
        cursor = self.conn.cursor()
        query = "select * from Medicine;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getAllMedicineById(self, medicineid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Medicine where medicineid = %s;"
        cursor.execute(query, (medicineid,))
        result = cursor.fetchone()
        return result

    def getAllMedicineBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Medicine where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMedicineByName(self, medname):
        cursor = self.conn.cursor()
        query = "select * from Medicine where medname = %s;"
        cursor.execute(query, (medname,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getMedicineByPrice(self, medprice):
        cursor = self.conn.cursor()
        query = "select * from Medicine where medprice = %s;"
        cursor.execute(query, (medprice,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMedicineByDose(self, meddose):
        cursor = self.conn.cursor()
        query = "select * from Medicine where meddose = %s;"
        cursor.execute(query, (meddose,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getMedicineByDescription(self, meddescription):
        cursor = self.conn.cursor()
        query = "select * from Medicine where meddescription = %s;"
        cursor.execute(query, (meddescription,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def insert(self, resourceid, medname, meddose, meddescription):
        cursor = self.conn.cursor()
        query = "insert into Medicine(resourceid, medname, meddose, meddescription) values(%s, %s, %s, %s) returning medid;"
        cursor.execute(query, (resourceid, medname, meddose, meddescription,))
        medid = cursor.fetchone()[0]
        self.conn.commit()
        return medid
    
    def delete(self, medid):
        cursor = self.conn.cursor()
        query = "delete from Medicine where medid = %s;"
        cursor.execute(query, (medid,))
        self.conn.commit()
        return medid
    
    def update(self, medid, medname, meddose, meddescription):
        cursor = self.conn.cursor()
        query = "update Medicine set medname = %s, meddose = %s, meddescription = %s;"
        cursor.execute(query, (medname, meddose, meddescription,))
        self.conn.commit()
        return medid
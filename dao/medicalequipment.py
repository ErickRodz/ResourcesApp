import psycopg2

from config.dbconfig import pg_config

class MedicalEquipmentDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)
    
    def getAllMedicalEquipment(self):
        cursor = self.conn.cursor()
        query = "select * from MedicalEquipment;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMedicalEquipmentById(self, medeqid):
        cursor = self.conn.cursor()
        query = "select * from MedicalEquipment where medeqid = %s;"
        cursor.execute(query)
        result = cursor.fetchone()
        return result
    
    def getMedicalEquipmentBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join MedicalEquipment where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getMedicalEquipmentByName(self, medeqname):
        cursor = self.conn.cursor()
        query = "select * from MedicalEquipment where medname= %s;"
        cursor.execute(query, (medeqname,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMedicalEquipmentByBrand(self, medeqbrand):
        cursor = self.conn.cursor()
        query = "select * from MedicalEquipment where medeqbrand = %s;"
        cursor.execute(query, (medeqbrand,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMedicalEquipmentByDescription(self, medeqdescription):
        cursor = self.conn.cursor()
        query = "select * from MedicalEquipment where medeqdescription = %s;"
        cursor.execute(query, (medeqdescription,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByMedEqID(self, medeqid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join MedicalEquipment where medeqid = %s;"
        cursor.execute(query, (medeqid,))
        result = cursor.fetchone()
        return result

    def getMedEqByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join MedicalEquipment where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result
    
    def insert(self, resourceid, medeqbrand, medeqdescription):
        cursor = self.conn.cursor()
        query = "insert into MedicalEquipment(resourceid, medbrand, medeqdescription) values (%s, %s, %s) returning medeqid;"
        cursor.execute(query, (resourceid, medeqbrand, medeqdescription,))
        medeqid = cursor.fetchone()[0]
        self.conn.commit()
        return medeqid
    
    def delete(self, medeqid):
        cursor = self.conn.cursor()
        query = "delete from MedicalEquipment where medeqid = %s;"
        cursor.execute(query, (medeqid,))
        self.conn.commit()
        return medeqid
    
    def update(self, medeqid, medeqbrand, meddescription):
        cursor = self.conn.cursor()
        query = "update MedicalEquipment set medeqbrand = %s, medeqdescription = %s;"
        cursor.execute(query, (medeqbrand, meddescription, medeqid,))
        self.conn.commit()
        return medeqid
    
import psycopg2

from config.dbconfig import pg_config

class IceDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)
    
    def getAllIce(self):
        cursor = self.conn.cursor()
        query = "select * from Ice;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getIceById(self, iceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Ice where iceid = %s;"
        cursor.execute(query, (iceid,))
        result = cursor.fetchone()
        return result

    def getIceBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Ice where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result 

    def getIceBySize(self, icesize):
        cursor = self.conn.cursor()
        query = "select * from Ice where icesize = %s;"
        cursor.execute(query, (icesize,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByIceID(self, iceid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join Ice where iceid = %s;"
        cursor.execute(query, (iceid,))
        result = cursor.fetchone()
        return result

    def getIceByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Ice where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def insert(self, icesize, icedescription, resourceid):
        cursor = self.conn.cursor()
        query = "insert into Ice(resourceid, icesize, icedescription) values(%s, %s, %s) returning iceid;"
        cursor.execute(query, (icesize, icedescription,resourceid, ))
        iceid = cursor.fetchone()[0]
        self.conn.commit()
        return iceid
    
    def delete(self, iceid):
        cursor = self.conn.cursor()
        query = "delete from Ice where iceid = %s;"
        cursor.execute(query, (iceid,))
        self.conn.commit()
        return iceid

    def update(self, iceid, icesize, icedescription):
        cursor = self.conn.cursor()
        query = "update Ice set icesize = %s, icedescription = %s;"
        cursor.execute(query, (icesize, icedescription, iceid,))
        self.conn.commit()
        return iceid
import psycopg2

from config.dbconfig import pg_config


class PartsDAO:
    def _init_(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllParts(self):
        cursor = self.conn.cursor()
        query = "select * from Parts;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPartsById(self, Partsid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Parts where partsid = %s;"
        cursor.execute(query, (Partsid,))
        result = cursor.fetchone()
        return result

    def getPartsBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Parts where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByPartsID(self, Partsid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join Parts where Partsid = %s;"
        cursor.execute(query, (Partsid,))
        result = cursor.fetchone()
        return result

    def insert(self, Partsmaterial, Partscolor, Partsdescription, resourceid):
        cursor = self.conn.cursor()
        query = "insert into Parts(PartsMaterial, PartsColor, PartsDescription, ResourceID) values (%s, %s, %s, %s) returning Partsid;"
        cursor.execute(query, (Partsmaterial, Partscolor, Partsdescription, resourceid,))
        Partsid = cursor.fetchone()[0]
        self.conn.commit()
        return Partsid

    def delete(self, Partsid):
        cursor = self.conn.cursor()
        query = "delete from Parts where partsid = %s;"
        cursor.execute(query, (Partsid,))
        self.conn.commit()
        return Partsid

    def update(self, Partsid, Partsmaterial, Partscolor, Partsdescription):
        cursor = self.conn.cursor()
        query = "update Parts set PartsMaterial = %s, PartsColor = %s, PartsDescription = %s where PartsID = %s;"
        cursor.execute(query, (Partsmaterial, Partscolor, Partsdescription, Partsid,))
        self.conn.commit()
        return Partsid


import psycopg2

from config.dbconfig import pg_config


class ClothingDAO:
    def _init_(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllClothing(self):
        cursor = self.conn.cursor()
        query = "select * from Clothing;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getClothingById(self, Clothingid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Clothing where Clothingid = %s;"
        cursor.execute(query, (Clothingid,))
        result = cursor.fetchone()
        return result

    def getClothingBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Clothing where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByClothingID(self, Clothingid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join Clothing where Clothingid = %s;"
        cursor.execute(query, (Clothingid,))
        result = cursor.fetchone()
        return result

    def getClothingByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Clothing where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def insert(self, Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, resourceid):
        cursor = self.conn.cursor()
        query = "insert into Clothing(Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, resourceid) values (%s, %s, %s, %s, %s) returning Clothingid;"
        cursor.execute(query, (Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, resourceid,))
        Clothingid = cursor.fetchone()[0]
        self.conn.commit()
        return Clothingid

    def delete(self, Clothingid):
        cursor = self.conn.cursor()
        query = "delete from Clothing where Clothingid = %s;"
        cursor.execute(query, (Clothingid,))
        self.conn.commit()
        return Clothingid

    def update(self, Clothingid, Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription):
        cursor = self.conn.cursor()
        query = "update Clothing set Clothingbrand = %s,Clothingsize = %s,  Clothingfabric = %s, Clothingdescription = %s where Clothingid = %s;"
        cursor.execute(query, (Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, Clothingid,))
        self.conn.commit()
        return Clothingid


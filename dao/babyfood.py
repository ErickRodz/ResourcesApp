import psycopg2

from config.dbconfig import pg_config


class BabyFoodDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllBabyFood(self):
        cursor = self.conn.cursor()
        query = "select * from BabyFood;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBabyFoodById(self, babyfoodid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join BabyFood where babyfoodid = %s;"
        cursor.execute(query, (babyfoodid,))
        result = cursor.fetchone()
        return result

    def getBabyFoodBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join BabyFood where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBabyFoodBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Babyfood where supplierid = %s"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByBFoodID(self, bfoodid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join BabyFood where bfoodid = %s;"
        cursor.execute(query, (bfoodid,))
        result = cursor.fetchone()
        return result

    def getBFoodByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join BabyFood where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def insert(self, bfoodflavor, bfooddescription, resourceid):
        cursor = self.conn.cursor()
        query = "insert into BabyFood(bfoodflavor, bfooddescription, resourceid) values (%s, %s, %s) returning bfoodid;"
        cursor.execute(query, (bfoodflavor, bfooddescription, resourceid, ))
        bfoodid = cursor.fetchone()[0]
        self.conn.commit()
        return bfoodid

    def delete(self, bfoodid):
        cursor = self.conn.cursor()
        query = "delete from BabyFood where bfoodid = %s;"
        cursor.execute(query, (bfoodid,))
        self.conn.commit()
        return bfoodid

    def update(self, bfoodid, bfoodflavor, bfooddescription):
        cursor = self.conn.cursor()
        query = "update BabyFood set bfoodflavor = %s, bfooddescription = %s where bfoodid = %s;"
        cursor.execute(query, (bfoodflavor, bfooddescription, bfoodid,))
        self.conn.commit()
        return bfoodid


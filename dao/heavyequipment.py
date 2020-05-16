import psycopg2

from config.dbconfig import pg_config


class HeavyEquipmentDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllHeavyEquipment(self):
        cursor = self.conn.cursor()
        query = "select * from HeavyEquipment;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getHeavyEquipmentById(self, heavyeqid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join HeavyEquipment where heavyeqid = %s;"
        cursor.execute(query, (heavyeqid,))
        result = cursor.fetchone()
        return result

    def getHeavyEquipmentBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join HeavyEquipment where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByHeavyEqID(self, heavyeqid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join HeavyEquipment where heavyeqid = %s;"
        cursor.execute(query, (heavyeqid,))
        result = cursor.fetchone()
        return result

    def getHeavyEqByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join HeavyEquipment where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def insert(self, heavyeqbrand, heavyeqdescription, resourceid ):
        cursor = self.conn.cursor()
        query = "insert into HeavyEquipment(heavyeqbrand, heavyeqdescription, resourceid) values (%s, %s, %s) returning heavyeqid;"
        cursor.execute(query, (heavyeqbrand, heavyeqdescription, resourceid, ))
        heavyeqid = cursor.fetchone()[0]
        self.conn.commit()
        return heavyeqid

    def delete(self, heavyeqid):
        cursor = self.conn.cursor()
        query = "delete from HeavyEquipment where heavyeqid = %s;"
        cursor.execute(query, (heavyeqid,))
        self.conn.commit()
        return heavyeqid

    def update(self, heavyeqid, heavyeqbrand, heavyeqdescription):
        cursor = self.conn.cursor()
        query = "update HeavyEquipment set heavyeqbrand = %s, heavyeqdescription = %s where heavyeqid = %s;"
        cursor.execute(query, (heavyeqbrand, heavyeqdescription, heavyeqid,))
        self.conn.commit()
        return heavyeqid


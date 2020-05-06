import psycopg2

from config.dbconfig import pg_config


class CannedFoodDAO:
    def _init_(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllCannedFood(self):
        cursor = self.conn.cursor()
        query = "select * from CannedFood;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCannedFoodById(self, cfoodid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join CannedFood where cfoodid = %s;"
        cursor.execute(query, (cfoodid,))
        result = cursor.fetchone()
        return result

    def getCannedFoodBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join CannedFood where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    #def getSupplierByBatteryID(self, batteryid):
        #cursor = self.conn.cursor()
        #query = "select supplierid from Suppliers natural inner join Resources where resourceid = %s;"
        #cursor.execute(query, (batteryid,))
        #result = cursor.fetchone()
        #return result\

    def getResourceIDByCFoodID(self, cfoodid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join CannedFood where cfoodid = %s;"
        cursor.execute(query, (cfoodid,))
        result = cursor.fetchone()
        return result

    def getCFoodByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join CannedFood where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def insert(self, cfoodbrand, cfoodserving, cfooddescription, resourceid, ):
        cursor = self.conn.cursor()
        query = "insert into CannedFood(cfoodbrand, cfoodserving, cfooddescription, resourceid) values (%s, %s, %s, %s) returning cfoodid;"
        cursor.execute(query, (cfoodbrand, cfoodserving, cfooddescription, resourceid,))
        cfoodid = cursor.fetchone()[0]
        self.conn.commit()
        return cfoodid

    def delete(self, cfoodid):
        cursor = self.conn.cursor()
        query = "delete from CannedFood where cfoodid = %s;"
        cursor.execute(query, (cfoodid,))
        self.conn.commit()
        return cfoodid

    def update(self, cfoodid, cfoodbrand, cfoodserving, cfooddescription):
        cursor = self.conn.cursor()
        query = "update CannedFood set cfoodbrand = %s, cfoodserving = %s, cfooddescription = %s where cfoodid = %s;"
        cursor.execute(query, (cfoodbrand, cfoodserving, cfooddescription, cfoodid,))
        self.conn.commit()
        return cfoodid


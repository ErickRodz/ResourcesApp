import psycopg2

from config.dbconfig import pg_config


class FuelDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllFuel(self):
        cursor = self.conn.cursor()
        query = "select * from Fuel;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getFuelById(self, Fuelid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Fuel where Fuelid = %s;"
        cursor.execute(query, (Fuelid,))
        result = cursor.fetchone()
        return result

    def getFuelBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Fuel where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByFuelID(self, Fuelid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join Fuel where Fuelid = %s;"
        cursor.execute(query, (Fuelid,))
        result = cursor.fetchone()
        return result

    def getFuelByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Fuel where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def insert(self,Fueltype, Fueloctenage, Fueldescription, resourceid):
        cursor = self.conn.cursor()
        query = "insert into Fuel(Fueltype, Fueloctenage, Fueldescription, resourceid) values (%s, %s, %s, %s) returning Fuelid;"
        cursor.execute(query, (Fueltype, Fueloctenage, Fueldescription, resourceid,))
        Fuelid = cursor.fetchone()[0]
        self.conn.commit()
        return Fuelid

    def delete(self, Fuelid):
        cursor = self.conn.cursor()
        query = "delete from Fuel where Fuelid = %s;"
        cursor.execute(query, (Fuelid,))
        self.conn.commit()
        return Fuelid

    def update(self, Fuelid, Fueltype, Fueloctenage, Fueldescription):
        cursor = self.conn.cursor()
        query = "update Fuel set Fueltype = %s, Fueloctenage = %s, Fueldescription = %s where Fuelid = %s;"
        cursor.execute(query, (Fuelid, Fueltype, Fueloctenage, Fueldescription, Fuelid,))
        self.conn.commit()
        return Fuelid


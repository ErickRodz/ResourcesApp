import psycopg2

from config.dbconfig import pg_config


class BatteriesDAO:
    def _init_(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllBatteries(self):
        cursor = self.conn.cursor()
        query = "select * from Batteries;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBatteriesById(self, batteryid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Batteries where batteryid = %s;"
        cursor.execute(query, (batteryid,))
        result = cursor.fetchone()
        return result

    def getBatteriesBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Batteries where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByBatteryID(self, batteryid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join Batteries where batteryid = %s;"
        cursor.execute(query, (batteryid,))
        result = cursor.fetchone()
        return result

    def insert(self, batterybrand, batterytype, batterydescription, resourceid):
        cursor = self.conn.cursor()
        query = "insert into Batteries(batterybrand, batterytype, batterydescription, resourceid) values (%s, %s, %s, %s) returning batteryid;"
        cursor.execute(query, (batterybrand, batterytype, batterydescription, resourceid,))
        batteryid = cursor.fetchone()[0]
        self.conn.commit()
        return batteryid

    def delete(self, batteryid):
        cursor = self.conn.cursor()
        query = "delete from Batteries where batteryid = %s;"
        cursor.execute(query, (batteryid,))
        self.conn.commit()
        return batteryid

    def update(self, batteryid, batterybrand, batterytype, batterydescription):
        cursor = self.conn.cursor()
        query = "update Batteries set batterybrand = %s, batterytype = %s, batterydescription = %s where batteryid = %s;"
        cursor.execute(query, (batterybrand, batterytype, batterydescription, batteryid,))
        self.conn.commit()
        return batteryid


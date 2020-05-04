import psycopg2

from config.dbconfig import pg_config


class WaterDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)
    
    def getAllWater(self):
        cursor = self.conn.cursor()
        query = "select * from Water;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getWaterById(self, waterid):
        cursor = self.conn.cursor
        query = "select * from Resources natural inner join Water where waterid = %s;"
        cursor.execute(query, (waterid,))
        result = cursor.fetchone()
        return result
    
    def getWaterBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Water where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByWaterID(self, waterid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join Water where waterid = %s;"
        cursor.execute(query, (waterid,))
        result = cursor.fetchone()
        return result

    def getWaterBySupplierAndSize(self, supplierid, watersize):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Water where suppleirid = %s && watersize = %s;"
        cursor.execute(query, (supplierid, watersize,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Este query no depende de resources
    def getWaterBySize(self, watersize):
        cursor = self.conn.cursor()
        query = "select * from Water where watersize = %s;"
        cursor.execute(query, (watersize,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getWaterByDescription(self, waterdescription):
        cursor = self.conn.cursor()
        query = "select * from Water where waterdescription = %s;"
        cursor.execute(query, (waterdescription,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, resourceid, watersize, waterdescription):
        cursor = self.conn.cursor()
        query = "insert into Water(resourceid, watersize, waterdescription) values (%s, %s, %s) returning waterid;"
        cursor.execute(query, (resourceid, watersize, waterdescription,))
        waterid = cursor.fetchone()[0]
        self.conn.commit()
        return waterid

    def delete(self, waterid):
        cursor = self.conn.cursor()
        query = "delete from Water where waterid = %s;"
        cursor.execute(query, (waterid,))
        self.conn.commit()
        return waterid
    
    def update(self, waterid, watersize, waterdescription):
        cursor = self.conn.cursor()
        query = "update Water set watersize = %s, waterdescription = %s;"
        cursor.execute(query, (watersize, waterdescription, waterid,))
        self.conn.commit()
        return waterid
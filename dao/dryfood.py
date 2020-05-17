import psycopg2

from config.dbconfig import pg_config


class DryFoodDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllDryFood(self):
        cursor = self.conn.cursor()
        query = "select * from DryFood;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getDryFoodById(self, dfoodid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join DryFood where dfoodid = %s;"
        cursor.execute(query, (dfoodid,))
        result = cursor.fetchone()
        return result

    def getDryFoodBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join DryFood where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByDFoodID(self, dfoodid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join DryFood where dfoodid = %s;"
        cursor.execute(query, (dfoodid,))
        result = cursor.fetchone()
        return result

    def getDFoodByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join DryFood where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def insert(self, dfoodserving, dfooddescription, resourceid):
        cursor = self.conn.cursor()
        query = "insert into DryFood(dfoodserving, dfooddescription, resourceid) values (%s, %s, %s) returning dfoodid;"
        cursor.execute(query, (dfoodserving, dfooddescription,resourceid,))
        dfoodid = cursor.fetchone()[0]
        self.conn.commit()
        return dfoodid

    def delete(self, dfoodid):
        cursor = self.conn.cursor()
        query = "delete from Dryfood where dfoodid = %s;"
        cursor.execute(query, (dfoodid,))
        self.conn.commit()
        return dfoodid

    def update(self, dfoodid, dfoodserving, dfooddescription):
        cursor = self.conn.cursor()
        query = "update Dryfood set dfoodserving = %s, dfooddescription = %s where dfoodid = %s;"
        cursor.execute(query, (dfoodserving, dfooddescription, dfoodid,))
        self.conn.commit()
        return dfoodid


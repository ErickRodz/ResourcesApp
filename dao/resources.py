from config.dbconfig import pg_config
import psycopg2

class ResourcesDAO:
    def _init_(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllResources(self):
        cursor = self.conn.cursor()
        query = "select resourceid, resourcename, resourcetype, resourcevendor, resourcelocation, resourceprice from Resources;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceById(self, resourceid):
        cursor = self.conn.cursor()
        query = "select resourceid, resourcename, resourcetype, resourcevendor, resourcelocation, resourceprice from Resources where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def getResourcesByType(self, resourcetype):
        cursor = self.conn.cursor()
        query = "select * from Resources where resourcetype = %s;"
        cursor.execute(query, (resourcetype,))
        result = []
        for row in cursor:
            result.append(row)
        return result
    def getResourcesByVendor(self, resourcevendor):
        cursor = self.conn.cursor()
        query = "select * from Resources where resourcevendor = %s;"
        cursor.execute(query, (resourcevendor,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourcesByTypeAndVendor(self, resourcetype, resourcevendor):
        cursor = self.conn.cursor()
        query = "select * from Resources where resourcetype = %s and resourcevendor = %s"
        cursor.execute(query, (resourcetype, resourcevendor))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self,resourcename, resourcetype, resourcevendor, resourcelocation, resourceprice):
        cursor = self.conn.cursor()
        query = "insert into Resources(resourcename, resourcetype, resourcevendor, resourcelocation, resourceprice) values (%s, %s, %s, %s, %s) returning resourceid;"
        cursor.execute(query, (resourcename, resourcetype, resourcevendor,resourcelocation, resourceprice,))
        resourceid = cursor.fetchone()[0]
        self.conn.commit()
        return resourceid

    def delete(self, resourceid):
        cursor = self.conn.cursor()
        query = "delete from Resources where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        self.conn.commit()
        return resourceid

    def update(self, resourceid, resourcename, resourcetype, resourcevendor, resourcelocation, resourceprice):
        cursor = self.conn.cursor()
        query = "update Resources set resourcename = %s, resourcetype = %s, resourcevendor = %s, resourcelocation = %s, resourceprice = %s where resourceid = %s;"
        cursor.execute(query, (resourcename, resourcetype, resourcevendor, resourcelocation, resourceprice, resourceid,))
        self.conn.commit()
        return resourceid





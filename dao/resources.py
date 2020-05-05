from config.dbconfig import pg_config
import psycopg2

class ResourcesDAO:
    def _init_(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllResources(self):
        cursor = self.conn.cursor()
        query = "select resourceid, supplierid, resourcename, resourceprice, resourcequantity from Resources;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceById(self, resourceid):
        cursor = self.conn.cursor()
        query = "select resourceid, supplierid, resourcename, resourceprice, resourcequantity, from Resources where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def getResourcesBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select supplierid from Resources where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def getResourcesByCategoryName(self, categoryname):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Categories where categoryname = %s;"
        cursor.execute(query, (categoryname,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourcesByName(self, resourcename):
        cursor = self.conn.cursor()
        query = "select * from Resources where resourcename = %s order by resourcename;"
        cursor.execute(query, (resourcename,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourcesAvailable(self):
        cursor = self.conn.cursor()
        query = "select * from Resources where resourcequantity > 0 order by resourcename;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourcesByNameAndSupplier(self, resourcename, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources where resourcename = %s and supplierid = %s"
        cursor.execute(query, (resourcename, supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, supplierid, resourcename, resourceprice, resourcequantity):
        cursor = self.conn.cursor()
        query = "insert into Resources(supplierid, resourcename, resourceprice, resourcequantity) values (%s, %s, %s, %s) returning resourceid;"
        cursor.execute(query, (supplierid, resourcename, resourceprice, resourcequantity,))
        resourceid = cursor.fetchone()[0]
        self.conn.commit()
        return resourceid

    def delete(self, resourceid):
        cursor = self.conn.cursor()
        query = "delete from Resources where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        self.conn.commit()
        return resourceid

    def update(self, resourceid, supplierid, resourcename, resourceprice, resourcequantity):
        cursor = self.conn.cursor()
        query = "update Resources set resourcename = %s, resourceprice = %s, resourcequantity = %s where resourceid = %s and supplierid = %s;"
        cursor.execute(query, (resourcename, resourceprice, resourcequantity, resourceid, supplierid,))
        self.conn.commit()
        return resourceid




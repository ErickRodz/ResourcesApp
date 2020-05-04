import psycopg2

from config.dbconfig import pg_config


class ToolsDAO:
    def _init_(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllTools(self):
        cursor = self.conn.cursor()
        query = "select * from Tools;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getToolsById(self, toolid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Batteries where toolid = %s;"
        cursor.execute(query, (toolid,))
        result = cursor.fetchone()
        return result

    def getToolsBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Tools where supplierid = %s;"
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
        #return result

    def getToolsByName(self, toolname):
        cursor = self.conn.cursor()
        query = "select * from Tools where toolname = %s;" #doubt
        cursor.execute(query, (toolname,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getToolsByNameAndSupplier(self, toolname, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Tools where toolname = %s and supplierid = %s"
        cursor.execute(query, (toolname, supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, resourceid, toolname, toolmaterial, toolcolor, tooldescription):
        cursor = self.conn.cursor()
        query = "insert into Tools(resourceid, toolname, toolmaterial, toolcolor, tooldescription) values (%s, %s, %s, %s, %s) returning toolid;"
        cursor.execute(query, (resourceid, toolname, toolmaterial, toolcolor, tooldescription,))
        toolid = cursor.fetchone()[0]
        self.conn.commit()
        return toolid

    def delete(self, toolid):
        cursor = self.conn.cursor()
        query = "delete from Tools where toolid = %s;"
        cursor.execute(query, (toolid,))
        self.conn.commit()
        return toolid

    def update(self, toolid, toolname, toolmaterial, toolcolor, tooldescription):
        cursor = self.conn.cursor()
        query = "update Tools set toolname = %s, toolmaterial = %s, toolcolor = %s, tooldescription = %s where toolid = %s;"
        cursor.execute(query, (toolname, toolmaterial, toolcolor, tooldescription, toolid,))
        self.conn.commit()
        return toolid


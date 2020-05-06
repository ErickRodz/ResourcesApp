import psycopg2

from config.dbconfig import pg_config


class ToolsDAO:
    def _init_(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'])

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

    def getToolsByMaterial(self, toolmaterial):
        cursor = self.conn.cursor()
        query = "select * from Tools where toolmaterial = %s;"
        cursor.execute(query, (toolmaterial,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getToolsByColor(self, toolcolor):
        cursor = self.conn.cursor()
        query = "select * from Tools where toolcolor = %s;"
        cursor.execute(query, (toolcolor,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getToolsByDescription(self, tooldescription):
        cursor = self.conn.cursor()
        query = "select * from Tools where tooldescription = %s;"
        cursor.execute(query, (tooldescription,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTooldByColorAndMaterial(self, toolcolor, toolmaterial):
        cursor = self.conn.cursor()
        query = "select * from Tools where toolcolor = %s and toolmaterial = %s;"
        cursor.execute(query, (toolcolor, toolmaterial,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByToolID(self, toolid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join Tools where toolid = %s;"
        cursor.execute(query, (toolid,))
        result = cursor.fetchone()
        return result

    def getToolByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Tool where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def getToolsByName(self, toolname):
        cursor = self.conn.cursor()
        query = "select * from Tools where toolname = %s;"  # doubt
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

    def insert(self, resourceid, toolmaterial, toolcolor, tooldescription):
        cursor = self.conn.cursor()
        query = "insert into Tools(resourceid, toolname, toolmaterial, toolcolor, tooldescription) values (%s, %s, %s, %s, %s) returning toolid;"
        cursor.execute(query, (resourceid, toolmaterial, toolcolor, tooldescription,))
        toolid = cursor.fetchone()[0]
        self.conn.commit()
        return toolid

    def delete(self, toolid):
        cursor = self.conn.cursor()
        query = "delete from Tools where toolid = %s;"
        cursor.execute(query, (toolid,))
        self.conn.commit()
        return toolid

    def update(self, toolid, toolmaterial, toolcolor, tooldescription):
        cursor = self.conn.cursor()
        query = "update Tools set toolname = %s, toolmaterial = %s, toolcolor = %s, tooldescription = %s where toolid = %s;"
        cursor.execute(query, (toolmaterial, toolcolor, tooldescription, toolid,))
        self.conn.commit()
        return toolid

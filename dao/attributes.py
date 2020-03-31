from config.dbconfig import pg_config
import psycopg2

class AttributesDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllAttributes(self):
        cursor = self.conn.cursor()
        query = "select * from Attributes;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAttributeById(self, attributeid):
        cursor = self.conn.cursor()
        query = "select * from Attributes where attributeid = %s;"
        cursor.execute(query, (attributeid,))
        result = cursor.fetchone()
        return result

    #duda con el get attribute by resource id con el query, pienso que hay que hacer un join en alguna parte
    def getAttributeByResourceId(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Attributes where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def getAttributebyAttributeName(self, attributename):
        cursor = self.conn.cursor()
        query = "select * from Attributes where attributename = %s;"
        cursor.execute(query, (attributename,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAttributebyAttributeQuantity(self, attributequantity):
        cursor = self.conn.cursor()
        query = "select * from Attributes where attributequantity = %s;"
        cursor.execute(query, (attributequantity,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAttributebyAttributeNameAndResourceId(self, attributename, attributeid):
        cursor = self.conn.cursor
        query = "select * from Attributes where attributename = %s and attributeid = %s;"
        cursor.execute(query, (attributename, attributeid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, resourceid, attributename, attributequantity):
        cursor = self.conn.cursor()
        query = "insert into Attributes(resourceid, attributename, attributequantity) values(%s, %s, %s) returning attributeid;"
        cursor.execute(query, (resourceid, attributename, attributequantity,))
        attributeid = cursor.fetchone()[0]
        self.conn.commit()
        return attributeid

    def update(self, attributeid, resourceid, attributename, attributequantity):
        cursor = self.conn.cursor()
        query = 'update Attributes set attributename = %s, attributequantity = %s where attributeid = %s and resourceid = %s;'
        cursor.execute(query, (attributename, attributequantity, attributeid, resourceid,))
        self.conn.commit()
        return attributeid

    def delete(self, attributeid):
        cursor = self.conn.cursor()
        query = "delete from Attributes where attributeid = %s;"
        cursor.execute(query, (attributeid,))
        self.conn.commit()
        return attributeid

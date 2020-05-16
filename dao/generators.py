import psycopg2

from config.dbconfig import pg_config


class GeneratorsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s"%(pg_config['dbname'],pg_config['user'],pg_config['passwd'])

        self.conn = psycopg2.connect(connection_url)

    def getAllGenerators(self):
        cursor = self.conn.cursor()
        query = "select * from Generators;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getGeneratorsById(self, generatorid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Generators where generatorid = %s;"
        cursor.execute(query, (generatorid,))
        result = cursor.fetchone()
        return result

    def getGeneratorsBySupplier(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Generators where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIDByGeneratorID(self, generatorid):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join Generators where generatorqid = %s;"
        cursor.execute(query, (generatorid,))
        result = cursor.fetchone()
        return result

    def getGeneratorByResourceID(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Generators where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    #def getGeneratorsByName(self, generatorname):
        #cursor = self.conn.cursor()
        #query = "select * from Generators where generatorname = %s;" #doubt
        #cursor.execute(query, (generatorname,))
        #result = []
        #for row in cursor:
            #result.append(row)
        #eturn result

    def getGeneratorsByType(self, generatortype):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Generators where generatortype = %s"
        cursor.execute(query, (generatortype,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, generatorbrand, generatortype, generatordescription, resourceid):
        cursor = self.conn.cursor()
        query = "insert into Generators(generatorbrand, generatortype, generatordescription, resourceid) values (%s, %s, %s, %s) returning generatorid;"
        cursor.execute(query, (generatorbrand, generatortype, generatordescription, resourceid, ))
        generatorid = cursor.fetchone()[0]
        self.conn.commit()
        return generatorid

    def delete(self, generatorid):
        cursor = self.conn.cursor()
        query = "delete from Generators where generatorid = %s;"
        cursor.execute(query, (generatorid,))
        self.conn.commit()
        return generatorid

    def update(self, generatorid, generatorbrand, generatortype, generatordescription):
        cursor = self.conn.cursor()
        query = "update Tools set generatorbrand = %s, generatortype = %s, generatordescription = %s where generatorid = %s;"
        cursor.execute(query, (generatorbrand, generatortype, generatordescription, generatorid,))
        self.conn.commit()
        return generatorid


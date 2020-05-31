from config.dbconfig import pg_config
import psycopg2


class CategoriesDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllCategories(self):
        cursor = self.conn.cursor()
        query = "select * from Categories;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCategoryById(self, categoryid):
        cursor = self.conn.cursor()
        query = "select * from Categories where categoryid = %s;"
        cursor.execute(query, (categoryid,))
        result = cursor.fetchone()
        return result

    # duda con el get attribute by resource id con el query, pienso que hay que hacer un join en alguna parte
    def getCategoryByResourceId(self, resourceid):
        cursor = self.conn.cursor()
        query = "select categoryname from Categories where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def getCategoryBySupplierId(self, supplierid):
        cursor = self.conn.cursor()
        query = "select * from Categories where supplierid = %s;"
        cursor.execute(query, (supplierid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

        # 9 in the Email Part 1

    # def getCategoryNameByResourceID(self, ResourceID):
    #   cursor = self.conn.cursor()
    #  query = "select categoryname from Categories where resourceid = %s;"
    # cursor.execute(query, (ResourceID,))
    # result = cursor.fetchone()
    # return result

    def insert(self, resourceid, categoryname, supplierid):
        cursor = self.conn.cursor()
        query = "insert into Categories(categoryname,resourceid, supplierid) values(%s, %s, %s) returning categoryid;"
        cursor.execute(query, (resourceid, categoryname, supplierid,))
        categoryid = cursor.fetchone()[0]
        self.conn.commit()
        return categoryid

    def update(self, categoryid, resourceid, categoryname, supplierid, ):
        cursor = self.conn.cursor()
        query = 'update Categories set categoryname = %s where categoryid = %s and resourceid = %s and supplierid = %s;'
        cursor.execute(query, (categoryname, categoryid, resourceid, supplierid,))
        self.conn.commit()
        return categoryid

    def delete(self, categoryid):
        cursor = self.conn.cursor()
        query = "delete from Categories where categoryid = %s;"
        cursor.execute(query, (categoryid,))
        self.conn.commit()
        return categoryid

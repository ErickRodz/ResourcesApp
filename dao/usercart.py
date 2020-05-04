from config.dbconfig import pg_config
import psycopg2

class UserCartDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllCarts(self):
        cursor = self.conn.cursor()
        query = "select * from UserCart;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCartById(self, CartID):
        cursor = self.conn.cursor()
        query = "select * from UserCart; where cartid = %s;"
        cursor.execute(query, (CartID,))
        result = cursor.fetchone()
        return result

    def getCartbyUserID(self, UserID):
        cursor = self.conn.cursor()
        query = "select * from UserCart where userid = %s;"
        cursor.execute(query, (UserID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserIdByCartId(self, CartID):
        cursor = self.conn.cursor()
        query = "select userid from Users natural inner join UserCart where cartid = %s;"
        cursor.execute(query, (CartID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIdByCartId(self, CartID):
        cursor = self.conn.cursor()
        query = "select resourceid from Resources natural inner join UserCart where cartid = %s;"
        cursor.execute(query, (CartID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, UserID, ResourceID, Selection):
        cursor = self.conn.cursor()
        query = "insert into UserCart(userid, resourceid, selection) values (%s, %s,%s) returning cartid;"
        cursor.execute(query, (UserID, ResourceID, Selection))
        cartid = cursor.fetchone()[0]
        self.conn.commit()
        return cartid

    def delete(self, CartID):
        cursor = self.conn.cursor()
        query = "delete from UserCart where cartid = %s;"
        cursor.execute(query, (CartID,))
        self.conn.commit()
        return CartID

    def update(self, CartID, ResourceID, Selection):
        cursor = self.conn.cursor()
        query = "update usercart set resourceid = %s, selection = %s where cartid = %s;"
        cursor.execute(query, (ResourceID, Selection, CartID))
        self.conn.commit()
        return CartID
from config.dbconfig import pg_config
import psycopg2

class OrdersDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllOrders(self):
        cursor = self.conn.cursor()
        query = "select * from Orders;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getOrderById(self, orderid):
        cursor = self.conn.cursor()
        query = "select * from Orders where orderid = %s;"
        cursor.execute(query, (orderid,))
        result = cursor.fetchone()
        return result

    def getOrdersByUserId(self, userid):
        cursor = self.conn.cursor()
        query = "select * from Orders where userid = %s;"
        cursor.execute(query, (userid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getOrdersbyCardId(self, cardid):
        cursor = self.conn.cursor()
        query = "select * from Orders where cardid = %s;"
        cursor.execute(query, (cardid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getOrderByCartId(self, cartid):
        cursor = self.conn.cursor()
        query = "select * from Orders where cartid = %s;"
        cursor.execute(query, (cartid,))
        result = cursor.fetchone()
        return result

    def getOrdersByResourceId(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Orders where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceQuantityByResourceId(self, resourceid):
        cursor = self.conn.cursor()
        query = "select resourcequantity from Resources natural inner join Orders where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def getResourcePriceByResourceId(self, resourceid):
        cursor = self.conn.cursor()
        query = "select resourceprice from Resources natural inner join Orders where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result

    def getOrdersByCardIdAndResourceId(self, cardid, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Orders where cardid = %s & resourceid = %s;"
        cursor.execute(query, (cardid, resourceid))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getOrdersByUserIdAndResourceId(self, userid, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Orders where userid = %s & resourceid = %s;"
        cursor.execute(query, (userid, resourceid))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, totalprice, totalquantity, userid, cardid, cartid, resourceid):
        cursor = self.conn.cursor()
        query = "insert into Orders(userid, cardid, cartid, resourceid, totalprice, totalquantity) values (%s, %s, %s, %s, %s, %s) returning orderid;"
        cursor.execute(query, (userid, cardid, cartid, resourceid, totalprice, totalquantity,))
        orderid = cursor.fetchone()[0]
        self.conn.commit()
        return orderid

    def delete(self, orderid):
        cursor = self.conn.cursor()
        query = "delete from Orders where orderid = %s;"
        cursor.execute(query, (orderid,))
        self.conn.commit()
        return orderid

    def update(self, totalprice, totalquantity, orderid):
        cursor = self.conn.cursor()
        query = "update Orders set totalprice = %s, totalquantity = %s where orderid = %s;"
        cursor.execute(query, (totalprice, totalquantity, orderid,))
        self.conn.commit()
        return orderid

    def updateResourceQuantity(self, newquantity,resourceid):
        cursor = self.conn.cursor()
        query = "update Resources set resourcequantity = %s where resourceid = %s;"
        cursor.execute(query, (newquantity, resourceid,))
        self.conn.commit()
        return resourceid

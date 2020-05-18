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

    def getOrderByOrderType(self, ordertype):
        cursor = self.conn.cursor()
        query = "select * from Orders where ordertype = %s;"
        cursor.execute(query, (ordertype,))
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

    def getResourceIdByOrderId(self, orderid):
        cursor = self.conn.cursor()
        query = "select resourceid from Orders where orderid = %s;"
        cursor.execute(query, (orderid,))
        result = []
        result = cursor.fetchone()
        return result

    def getUserIdIdByOrderId(self, orderid):
        cursor = self.conn.cursor()
        query = "select userid from Orders where orderid = %s;"
        cursor.execute(query, (orderid,))
        result = []
        result = cursor.fetchone()
        return result

    def getCardIdIdByOrderId(self, orderid):
        cursor = self.conn.cursor()
        query = "select cardid from Orders where orderid = %s;"
        cursor.execute(query, (orderid,))
        result = []
        result = cursor.fetchone()
        return result

    def getCartidByOrderId(self, orderid):
        cursor = self.conn.cursor()
        query = "select cartid from Orders where orderid = %s;"
        cursor.execute(query, (orderid,))
        result = []
        result = cursor.fetchone()
        return result

    def getRequestsByOrderID(self, OrderID):
        cursor = self.conn.cursor()
        query = "select * from Orders natural inner join Resources where ordertype = 'Request' and orderid = %s;"
        cursor.execute(query, (OrderID,))
        result =[]
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
        cursor.execute(query, (cardid, resourceid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getOrdersByUserIdAndResourceId(self, userid, resourceid):
        cursor = self.conn.cursor()
        query = "select * from Orders where userid = %s & resourceid = %s;"
        cursor.execute(query, (userid, resourceid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourcesRequestByResourceName(self, resourcename):
         cursor = self.conn.cursor()
         query = "select * from Resources natural inner join Orders where resourcename = %s order by resourcename;"
         cursor.execute(query, (resourcename,))
         result = []
         for row in cursor:
             result.append(row)
         return result

    def getReceiptsFromOrdersByCartIdAndOrderType(self, cartid, ordertype):
         cursor = self.conn.cursor()
         query = "select * from Orders where cartid  = %s and ordertype = %s;"
         cursor.execute(query, (cartid, ordertype,))
         result = []
         for row in cursor:
             result.append(row)
         return result
    #6.2
    def getOrdersByUserIdAndOrderType(self, userid, ordertype):
         cursor = self.conn.cursor()
         query = "select * from Orders where userid = %s and ordertype = %s;"
         cursor.execute(query, (userid, ordertype,))
         result = []
         for row in cursor:
             result.append(row)
         return result

    def getCategoryNameByResourceId(self, resourceid):
        cursor = self.conn.cursor()
        query = "select categoryname from Categories natural inner join Orders where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = cursor.fetchone()
        return result
    #10.2
    def getResourceRequestedByName(self, resourcename):
        cursor = self.conn.cursor()
        query = "select * from Orders where resourcename = %s and ordertype = 'request' order by resourcename;"
        cursor.execute(query, (resourcename,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourcesByResourceName(self, ordertype, resourcename):
        cursor = self.conn.cursor()
        query = "select * from Resources natural inner join Orders where ordertype = %s and resourcename = %s order by resourcename;"
        cursor.execute(query, (ordertype, resourcename,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getResourceIdByResourceName(self, resourcename):
        cursor = self.conn.cursor()
        query = "select resourceid from Orders where resourcename = %s;"
        cursor.execute(query, (resourcename,))
        result = []
        result = cursor.fetchone()
        return result

    def insert(self, totalprice, totalquantity, userid, cardid, cartid, resourceid,  resourcename, ordertype):
        cursor = self.conn.cursor()
        query = "insert into Orders(totalprice, totalquantity, userid, cardid, cartid, resourceid, resourcename, ordertype) values (%s, %s, %s, %s, %s, %s, %s, %s) returning orderid;"
        cursor.execute(query, (totalprice, totalquantity, userid, cardid, cartid, resourceid, resourcename, ordertype))
        orderid = cursor.fetchone()[0]
        self.conn.commit()
        return orderid

    def delete(self, orderid):
        cursor = self.conn.cursor()
        query = "delete from Orders where orderid = %s;"
        cursor.execute(query, (orderid,))
        self.conn.commit()
        return orderid

    def update(self, totalprice, totalquantity, resourcename, orderid):
        cursor = self.conn.cursor()
        query = "update Orders set totalprice = %s, totalquantity = %s, resourcename = %s where orderid = %s;"
        cursor.execute(query, (totalprice, totalquantity, resourcename, orderid,))
        self.conn.commit()
        return orderid

    def updateResourceQuantity(self, newquantity,resourceid):
        cursor = self.conn.cursor()
        query = "update Resources set resourcequantity = %s where resourceid = %s;"
        cursor.execute(query, (newquantity, resourceid,))
        self.conn.commit()
        return resourceid
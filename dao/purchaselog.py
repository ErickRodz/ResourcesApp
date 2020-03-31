from config.dbconfig import pg_config
import psycopg2

class PurchaseLogDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)
    
    def getAllPurchaseLogs(self):
        cursor = self.conn.cursor()
        query = "select * from PurchaseLog;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPurchaseLogById(self, purchaseId):
        cursor = self.conn.cursor()
        query = "select * from PurchaseLog where purchaseId = %s;"
        cursor.execute(query, (purchaseId,))
        result = cursor.fetchone()
        return result
    
    def getPurchaseLogByUserId(self, userId):
        cursor = self.conn.cursor()
        query = "select * from PurchaseLog where userId = %s;"
        cursor.execute(query, (userId,))
        result = cursor.fetchone()
        return result

    def getPurchaseLogsByUserId(self, userId):
        cursor = self.conn.cursor()
        query = "select * from PurchaseLog where userId = %s;"
        cursor.execute(query, (userId,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPurchaseLogByResourceId(self, resourceId):
        cursor = self.conn.cursor()
        query = "select * from PurchaseLog where resourceId = %s;"
        cursor.execute(query, (resourceId,))
        result = cursor.fetchone()
        return result

    def getPurchaseLogsByResourceId(self, resourceId):
        cursor = self.conn.cursor()
        query = "select * from PurchaseLog where resourceId = %s;"
        cursor.execute(query, (resourceId,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, userId, resourceId):
        cursor = self.conn.cursor()
        query = "insert into PurchaseLog (userId, resourceId) values (%s, %s) returning purchaseId;"
        cursor.execute(query, (userId, resourceId,))
        purchaseId = cursor.fetchone()[0]
        self.conn.commit()
        return purchaseId

    def delete(self, purchaseId):
        cursor = self.conn.cursor()
        query = "delete from PurchaseLog where purchaseId = %s;"
        cursor.execute(query, (purchaseId,))
        self.conn.commit()
        return purchaseId

    def update(self, purchaseId, userId, resourceId):
        cursor = self.conn.cursor()
        query = "update PurchaseLog set userId = %s, resourceId = %s where purchaseId = %s;"
        cursor.execute(query, (userId, resourceId, purchaseId,))
        self.conn.commit()
        return purchaseId
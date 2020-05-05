from config.dbconfig import pg_config
import psycopg2


class BankDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllBanks(self):
        cursor = self.conn.cursor()
        query = "select * from Bank;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBankById(self, BankID):
        cursor = self.conn.cursor()
        query = "select * from Bank where BankID = %s;"
        cursor.execute(query, (BankID,))
        result = cursor.fetchone()
        return result

    def getBankbyCardID(self, CardID):
        cursor = self.conn.cursor()
        query = "select * from Bank where CardID = %s;"
        cursor.execute(query, (CardID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBankbyUserID(self, UserID):
        cursor = self.conn.cursor()
        query = "select * from Bank where userid = %s;"
        cursor.execute(query, (UserID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBankbyUserIDandCardID(self, UserID, CardID):
        cursor = self.conn.cursor()
        query = "select * from Bank where userid = %s & cardid = %s;"
        cursor.execute(query, (UserID, CardID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBankbyBankName(self, BankName):
        cursor = self.conn.cursor()
        query = "select * from Bank where bankname = %s;"
        cursor.execute(query, (BankName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, CardID, UserID, Bankname):
        cursor = self.conn.cursor()
        query = "insert into Bank(cardid, userid, Bankname) values (%s, %s, %s) returning bankid;"
        cursor.execute(query, (CardID, UserID, Bankname,))
        bankid = cursor.fetchone()[0]
        self.conn.commit()
        return bankid

    def delete(self, BankID):
        cursor = self.conn.cursor()
        query = "delete from Bank where BankID = %s;"
        cursor.execute(query, (BankID,))
        self.conn.commit()
        return BankID

    def update(self, CardID, UserID, Bankname, BankID):
        cursor = self.conn.cursor()
        query = "update Bank set CardID = %s, UserID = %s, Bankname = %s where bankid = %s;"
        cursor.execute(query, (CardID, UserID, Bankname, BankID,))
        self.conn.commit()
        return BankID

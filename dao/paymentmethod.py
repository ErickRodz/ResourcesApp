from config.dbconfig import pg_config
import psycopg2


class PaymentMethodDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    # Check if this works. Since this will be logically called.
    def getAllCardsWithUsers(self):
        cursor = self.conn.cursor()
        query = "select * from PaymentMethod natural inner join Users natural inner join Bank;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllCards(self):
        cursor = self.conn.cursor()
        query = "select * from PaymentMethod;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getCardbyID(self, CardID):
        cursor = self.conn.cursor()
        query = "select * from PaymentMethod; where cardid = %s;"
        cursor.execute(query, (CardID,))
        result = cursor.fetchone()
        return result

    def getCardbyBankID(self, BankID):
        cursor = self.conn.cursor()
        query = "select * from PaymentMethod; where bankid = %s;"
        cursor.execute(query, (BankID,))
        result = cursor.fetchone()
        return result

    # Verify this once since it'd be logically used in  website
    def getCardbyUserID(self, UserID):
        cursor = self.conn.cursor()
        query = "select * from PaymentMethod where userid = %s natural inner join Users;"
        cursor.execute(query, (UserID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, UserID, BankID, Cardtype, CardNumber):
        cursor = self.conn.cursor()
        query = "insert into PaymentMethod(userid, bankid, cardtype, cardnumber) values (%s, %s, %s, %s) returning cardid;"
        cursor.execute(query, (UserID, BankID, Cardtype, CardNumber,))
        cardid = cursor.fetchone()[0]
        self.conn.commit()
        return cardid

    def delete(self, CardID):
        cursor = self.conn.cursor()
        query = "delete from PaymentMethod where cardid = %s;"
        cursor.execute(query, (CardID,))
        self.conn.commit()
        return CardID

    def update(self, CardID, UserID, BankID, Cardtype, CardNumber):
        cursor = self.conn.cursor()
        query = "update PaymentMethod set userid = %s, bankid = %s, cardtype = %s, cardnumber = %s where cardid = %s;"
        cursor.execute(query, (CardID, UserID, BankID, Cardtype, CardNumber,))
        self.conn.commit()
        return CardID

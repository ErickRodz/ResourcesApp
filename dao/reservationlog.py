from config.dbconfig import pg_config
import psycopg2


class ReservationLogsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (
        pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllLogs(self):
        cursor = self.conn.cursor()
        query = "select * from ReservationLog;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getLogById(self, logid):
        cursor = self.conn.cursor()
        query = "select * from ReservationLog where reservationid = %s;"
        cursor.execute(query, (logid,))
        result = cursor.fecthone()
        return result

        # This query returns all resrvation logs from the given user id

    def getLogsByUserId(self, userid):
        cursor = self.conn.cursor()
        query = "select * from ReservationLog where userid = %s;"
        cursor.execute(query, (userid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Ths query returns all reservation logs from the given resource id 
    def getLogByResourceId(self, resourceid):
        cursor = self.conn.cursor()
        query = "select * from ReservationLog where resourceid = %s;"
        cursor.execute(query, (resourceid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, userid, resourceid):
        cursor = self.conn.cursor()
        query = "insert into ReservationLog(userid, resourceid) values(%s, %s) returning reservationid;"
        cursor.execute(query, (userid, resourceid,))
        reservationid = cursor.fecthone()[0]
        self.conn.commit()
        return reservationid

    def update(self, reservationid, userid, resourceid):
        cursor = self.conn.cursor()
        query = "update ReservationLog set userid = %s, resourceid = %s where reservationid = %s;"
        cursor.execute(query, (userid, resourceid, reservationid))
        self.conn.commit()
        return reservationid

    def delete(self, reservationid):
        cursor = self.conn.cursor()
        query = "delete from ReservationLog where reservationid = %s;"
        cursor.execute(query, (reservationid,))
        self.conn.commit()
        return reservationid

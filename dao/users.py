from config.dbconfig import pg_config
import psycopg2

class UsersDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select * from Users;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserById(self, UserID):
        cursor = self.conn.cursor()
        query = "select * from Users Where userid = %s;"
        cursor.execute(query, (UserID,))
        result = cursor.fetchone()
        return result

    def getUserbyUsername(self, UserName):
        cursor = self.conn.cursor()
        query = "select * from Users where username = %s;"
        cursor.execute(query, (UserName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserbyEmail(self, Email):
        cursor = self.conn.cursor()
        query = "select * from Users where email = %s;"
        cursor.execute(query, (Email,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserByLocation(self, ULocation):
        cursor = self.conn.cursor()
        query = "select * from Users; where ulocation = %s;"
        cursor.execute(query, (ULocation,))
        result = cursor.fetchone()
        return result

    def getUserbyUserNameandPassword(self, UserName, Password):
        cursor = self.conn.cursor()
        query = "select * from Users where username = %s & password = %s;"
        cursor.execute(query, (UserName, Password))
        result = []
        for row in cursor:
            result.append(row)
        return result



    def insert(self, UserName, Password, Email, CardID, ULocation, FirstName, LastName, DateofBirth,Gender):
        cursor = self.conn.cursor()
        query = "insert into Users( username, password, email, cardid, ulocation, firstname, lastname, dateofbirth, gender) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning userid;"
        cursor.execute(query, (UserName, Password, Email, CardID, ULocation, FirstName, LastName, DateofBirth,Gender,))
        userid = cursor.fetchone()[0]
        self.conn.commit()
        return userid

    def delete(self, UserID):
        cursor = self.conn.cursor()
        query = "delete from Users where userid = %s;"
        cursor.execute(query, (UserID,))
        self.conn.commit()
        return UserID

    def update(self, UserID, UserName, Password, Email, CardID, ULocation, FirstName, LastName, DateofBirth,Gender):
        cursor = self.conn.cursor()
        query = "update users set username = %s, password = %s, email = %s, cardid = %s, ulocation = %s, firstname = %s, lastname = %s, dateofbirth = %s, gender = %s where userid = %s;"
        cursor.execute(query, (UserName, Password, Email, CardID, ULocation, FirstName, LastName, DateofBirth,Gender, UserID,))
        self.conn.commit()
        return UserID
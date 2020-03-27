from config.dbconfig import pg_config
import psycopg2

class AdministratorsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=127.0.0.1" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllAdministrators(self):
        cursor = self.conn.cursor()
        query = "select * from Administrators;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAdministratorById(self, AdministratorID):
        cursor = self.conn.cursor()
        query = "select * from Administrators; where AdministratorID = %s;"
        cursor.execute(query, (AdministratorID,))
        result = cursor.fetchone()
        return result

    def getAdministratorbyUsername(self, UserName):
        cursor = self.conn.cursor()
        query = "select * from Administrators where UserName = %s;"
        cursor.execute(query, (UserName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAdministratorbyEmail(self, Email):
        cursor = self.conn.cursor()
        query = "select * from Administrators where email = %s;"
        cursor.execute(query, (Email,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAdministratorbyUserNameandPassword(self, UserName, Password):
        cursor = self.conn.cursor()
        query = "select * from Administrators where username = %s & password = %s;"
        cursor.execute(query, (UserName, Password))
        result = []
        for row in cursor:
            result.append(row)
        return result



    def insert(self, UserName, Password, Email, SLocation, Affiliation, FirstName, LastName, DateofBirth,Gender):
        cursor = self.conn.cursor()
        query = "insert into Administrators(username, password, email, firstname, lastname, dateofbirth, gender) values (%s, %s, %s, %s) returning administratorid;"
        cursor.execute(query, (UserName, Password, Email, SLocation, Affiliation, FirstName, LastName, DateofBirth,Gender,))
        administratorid = cursor.fetchone()[0]
        self.conn.commit()
        return administratorid

    def delete(self, AdministratorID):
        cursor = self.conn.cursor()
        query = "delete from Administrators where administratorid = %s;"
        cursor.execute(query, (AdministratorID,))
        self.conn.commit()
        return AdministratorID

    def update(self, AdministratorID, UserName, Password, Email,FirstName, LastName, DateofBirth,Gender):
        cursor = self.conn.cursor()
        query = "update suppliers set username = %s, password = %s, email = %s, firstname = %s, lastname = %s, dateofbirth = %s, gender = %s where administratorid = %s;"
        cursor.execute(query, (UserName, Password, Email, FirstName, LastName, DateofBirth,Gender, AdministratorID,))
        self.conn.commit()
        return AdministratorID
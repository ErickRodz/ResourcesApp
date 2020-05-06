from config.dbconfig import pg_config
import psycopg2

class SuppliersDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'])
        self.conn = psycopg2.connect(connection_url)

    def getAllSuppliers(self):
        cursor = self.conn.cursor()
        query = "select * from Suppliers;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierById(self, SupplierID):
        cursor = self.conn.cursor()
        query = "select * from Suppliers; where supplierid = %s;"
        cursor.execute(query, (SupplierID,))
        result = cursor.fetchone()
        return result

    def getSupplierbyUsername(self, UserName):
        cursor = self.conn.cursor()
        query = "select * from Suppliers where username = %s;"
        cursor.execute(query, (UserName,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierbyEmail(self, Email):
        cursor = self.conn.cursor()
        query = "select * from Suppliers where email = %s;"
        cursor.execute(query, (Email,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierbyLocation(self, SLocation):
        cursor = self.conn.cursor()
        query = "select * from Suppliers where slocation = %s;"
        cursor.execute(query, (SLocation,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    #def getSupplierbyAffiliation(self, Affiliation):
   #     cursor = self.conn.cursor()
    #    query = "select * from Suppliers where affiliation = %s;"
     #  result = []
       # for row in cursor:
        #    result.append(row)
        #return result

    def getSupplierbyUserNameandPassword(self, UserName, Password):
        cursor = self.conn.cursor()
        query = "select * from Suppliers where username = %s & password = %s;"
        cursor.execute(query, (UserName, Password,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getSupplierAndResourcesByCategoryName(self, categoryname):
        cursor = self.conn.cursor()
        query = "select supplierid, affiliation, resourceid, resourcename from Suppliers natural inner join Resources natural inner join Categories where categoryname = %s;"
        cursor.execute(query, (categoryname,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insert(self, UserName, Password, Email, SLocation, FirstName, LastName, DateofBirth, Gender, CategoryName):
        cursor = self.conn.cursor()
        query = "insert into Suppliers(username, password, email, slocation, firstname, lastname, dateofbirth, gender, categoryname) values (%s, %s, %s, %s, %s %s, %s, %s, %s) returning supplierid;"
        cursor.execute(query, (UserName, Password, Email, SLocation, FirstName, LastName, DateofBirth, Gender, CategoryName,))
        supplierid = cursor.fetchone()[0]
        self.conn.commit()
        return supplierid

    def delete(self, SupplierID):
        cursor = self.conn.cursor()
        query = "delete from Suppliers where supplierid = %s;"
        cursor.execute(query, (SupplierID,))
        self.conn.commit()
        return SupplierID

    def update(self, SupplierID, UserName, Password, Email, SLocation, FirstName, LastName, DateofBirth, Gender, CategoryName):
        cursor = self.conn.cursor()
        query = "update suppliers set username = %s, password = %s, email = %s, slocation = %s, firstname = %s, lastname = %s, dateofbirth = %s, gender = %s, categoryname = %s where supplierid = %s;"
        cursor.execute(query, (UserName, Password, Email, SLocation, FirstName, LastName, DateofBirth,Gender, CategoryName, SupplierID,))
        self.conn.commit()
        return SupplierID
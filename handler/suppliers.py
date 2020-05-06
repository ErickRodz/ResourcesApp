from flask import jsonify
from dao.suppliers import SuppliersDAO


class SuppliersHandler:
    def build_suppliers_dict(self, row):
        result = {}
        result['SuppliersID'] = row[0]
        result['UserName'] = row[1]
        result['Password'] = row[2]
        result['Email'] = row[3]
        result['SLocation'] = row[4]
        result['FirstName'] = row[5]
        result['LastName'] = row[6]
        result['DateofBirth'] = row[7]
        result['Gender'] = row[8]
        result['CategoryName'] = row[9]
        return result

    def build_suppliers_attributes(self, SupplierID, UserName, Password, Email, SLocation, FirstName, LastName, DateofBirth, Gender, CategoryName):
        result = {}
        result['SupplierID'] = SupplierID
        result['UserName'] = UserName
        result['Password'] = Password
        result['Email'] = Email
        result['SLocation'] = SLocation
        result['FirstName'] = FirstName
        result['LastName'] = LastName
        result ['DateofBirth'] = DateofBirth
        result ['Gender'] = Gender
        result ['CategoryName'] = CategoryName
        return result

    def getAllSuppliers(self):
        dao = SuppliersDAO()
        suppliers_list = dao.getAllSuppliers()
        result_list = []
        for row in suppliers_list:
            result = self.build_suppliers_dict(row)
            result_list.append(result)
        return jsonify(Suppliers=result_list)

    def getSupplierById(self, SupplierID):
        dao = SuppliersDAO()
        row = dao.getSupplierById(SupplierID)
        if not row:
            return jsonify(Error = "Supplier Not Found"), 404
        else:
            suppliers = self.build_suppliers_dict(row)
            return jsonify(Suppliers = suppliers)

    def searchSuppliers(self, args):
        username = args.get("Username")
        password = args.get("Password")
        email = args.get("Email")
        slocation = args.get("SLocation")
        firstname = args.get("FirstName")
        lastname = args.get("LastName")
        dateofbirth = args.get("DateofBirth")
        gender = args.get("Gender")
        categoryname = args.get("CategoryName")
        dao = SuppliersDAO()

        suppliers_list = []
        if (len(args) == 2) and username and password:
            suppliers_list = dao.getSupplierbyUserNameandPassword(username, password)
        elif (len(args) == 1) and username:
            suppliers_list = dao.getSupplierbyUsername(username)
        elif (len(args) == 1) and email:
            suppliers_list = dao.getSupplierrByEmail(email)
        elif(len(args) == 1) and slocation:
            suppliers_list = dao.getSupplierbyLocation(slocation)
        elif(len(args) ==1) and categoryname:
            suppliers_list = dao.getSupplierAndResourcesByCategoryName(categoryname)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in suppliers_list:
            result = self.build_suppliers_dict(row)
            result_list.append(result)
        return jsonify(Suppliers=result_list)

    def insertSupplier(self, form):
        print("form: ", form)
        if len(form) != 9:
            return jsonify(Error = "Malformed post request"), 400
        else:
            username = form['UserName']
            password = form['Password']
            email = form['Email']
            slocation = form['SLocation']
            firstname = form['FirstName']
            lastname = form['LastName']
            dateofbirth = form['DateofBirth']
            gender = form['Gender']
            categoryname = form['CategoryName']
            if  username and password and email and slocation and firstname and lastname and dateofbirth and gender and categoryname:
                dao = SuppliersDAO()
                supplierid = dao.insert(username, password, email, slocation, firstname, lastname, dateofbirth,gender, categoryname)
                result = self.build_suppliers_attributes(supplierid, username, password, email, slocation, firstname, lastname, dateofbirth,gender, categoryname)
                return jsonify(Suppliers=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertSupplierJson(self, json):
        username = json['UserName']
        password = json['Password']
        email = json['Email']
        slocation = json['SLocation']
        firstname = json['FirstName']
        lastname = json['LastName']
        dateofbirth = json['DateofBirth']
        gender = json['Gender']
        categoryname = json['CategoryName']
        if  username and password and email and slocation and firstname and lastname and dateofbirth and gender and categoryname:
            dao = SuppliersDAO()
            supplierid = dao.insert(username, password, email, slocation, firstname, lastname, dateofbirth,gender, categoryname)
            result = self.build_suppliers_attributes(supplierid, username, password, email, slocation, firstname, lastname, dateofbirth,gender,categoryname)
            return jsonify(Suppliers=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteSupplier(self,supplierid):
        dao = SuppliersDAO()
        if not dao.getSupplierById(supplierid):
            return jsonify(Error = "Supplier not found."), 404
        else:
            dao.delete(supplierid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateSupplier(self, supplierid, form):
        dao = SuppliersDAO()
        if not dao.getSupplierById(supplierid):
            return jsonify(Error = "Supplier not found."), 404
        else:
            if len(form) != 11:
                return jsonify(Error="Malformed update request"), 400
            else:
                username = form['UserName']
                password = form['Password']
                email = form['Email']
                slocation = form['SLocation']
                affiliation = form['affiliation']
                firstname = form['FirstName']
                lastname = form['LastName']
                dateofbirth = form['DateofBirth']
                gender = form['Gender']
                categoryid = form['CategoryID']
                categoryname = form['CategoryName']
                if username and password and email and slocation and affiliation and firstname and lastname and dateofbirth and gender and categoryid and categoryname:
                    dao.update(username, password, email, slocation, affiliation, firstname, lastname, dateofbirth, gender, categoryid, categoryname)
                    result = self.build_suppliers_attributes(username, password, email, slocation, affiliation, firstname, lastname, dateofbirth, gender, categoryid, categoryname)
                    return jsonify(Suppliers=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def updateSupplierJson(self, supplierid, json):
        dao = SuppliersDAO()
        if not dao.getSupplierById(supplierid):
            return jsonify(Error="Admin not found."), 404
        else:
            username = json['UserName']
            password = json['Password']
            email = json['Email']
            slocation = json['SLocation']
            affiliation = json['affiliation']
            firstname = json['FirstName']
            lastname = json['LastName']
            dateofbirth = json['DateofBirth']
            gender = json['Gender']
            categoryid = json['CategoryID']
            categoryname = json['CategoryName']
            if username and password and email and slocation and affiliation and firstname and lastname and dateofbirth and gender and categoryid and categoryname:
                dao.update(supplierid, username, password, email, slocation, affiliation, firstname, lastname, dateofbirth, gender, categoryid, categoryname)
                result = self.build_suppliers_attributes(supplierid,username, password, email, slocation, affiliation, firstname, lastname, dateofbirth, gender, categoryid, categoryname)
                return jsonify(Administrators=result), 200
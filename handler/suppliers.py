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
        result['Affiliation'] = row[5]
        result['FirstName'] = row[6]
        result['LastName'] = row[7]
        result['DateofBirth'] = row[8]
        result['Gender'] = row[9]
        return result

    def build_suppliers_attributes(self, SupplierID, UserName, Password, Email, SLocation, Affiliation, FirstName, LastName, DateofBirth, Gender):
        result = {}
        result['SupplierID'] = SupplierID
        result['UserName'] = UserName
        result['Password'] = Password
        result['Email'] = Email
        result['SLocation'] = SLocation
        result['Affiliation'] = Affiliation
        result['FirstName'] = FirstName
        result['LastName'] = LastName
        result ['DateofBirth'] = DateofBirth
        result ['Gender'] = Gender
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
        affiliation = args.get("Affiliation")
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
        elif(len(args) == 1) and affiliation:
            suppliers_list = dao.getSupplierbyAffiliation(affiliation)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in suppliers_list:
            result = self.build_suppliers_dict(row)
            result_list.append(result)
        return jsonify(Suppliers=result_list)

    def insertSupplier(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            username = form['UserName']
            password = form['Password']
            email = form['Email']
            slocation = form['SLocation']
            affiliation = form['Affiliation']
            firstname = form['FirstName']
            lastname = form['LastName']
            dateofbirth = form['DateofBirth']
            gender = form['Gender']
            if  username and password and email and slocation and affiliation and firstname and lastname and dateofbirth and gender:
                dao = SuppliersDAO()
                supplierid = dao.insert(username, password, email, slocation, affiliation, firstname, lastname, dateofbirth,gender)
                result = self.build_users_attributes(supplierid, username, password, email, slocation, affiliation, firstname, lastname, dateofbirth,gender)
                return jsonify(Suppliers=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertSupplierJson(self, json):
        username = json['UserName']
        password = json['Password']
        email = json['Email']
        slocation = json['SLocation']
        affiliation = json['Affiliation']
        firstname = json['FirstName']
        lastname = json['LastName']
        dateofbirth = json['DateofBirth']
        gender = json['Gender']
        if  username and password and email and slocation and affiliation and firstname and lastname and dateofbirth and gender:
            dao = SuppliersDAO()
            supplierid = dao.insert(username, password, email, slocation, affiliation, firstname, lastname, dateofbirth,gender)
            result = self.build_suppliers_attributes(username, password, email, slocation, affiliation, firstname, lastname, dateofbirth,gender)
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
            if len(form) != 4:
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
                if username and password and email and slocation and affiliation and firstname and lastname and dateofbirth and gender:
                    dao.update(username, password, email, slocation, affiliation, firstname, lastname, dateofbirth, gender)
                    result = self.build_suppliers_attributes(username, password, email, slocation, affiliation, firstname, lastname, dateofbirth, gender)
                    return jsonify(Suppliers=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
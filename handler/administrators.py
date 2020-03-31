from flask import jsonify
from dao.administrators import AdministratorsDAO


class AdministratorsHandler:
    def build_administrators_dict(self, row):
        result = {}
        result['AdminID'] = row[0]
        result['UserName'] = row[1]
        result['Password'] = row[2]
        result['Email'] = row[3]
        result['FirstName'] = row[4]
        result['LastName'] = row[5]
        result['DateofBirth'] = row[6]
        result['Gender'] = row[7]
        return result

    def build_administrators_attributes(self, AdministratorID, UserName, Password, Email, FirstName, LastName, DateofBirth, Gender):
        result = {}
        result['AdminID'] = AdministratorID
        result['UserName'] = UserName
        result['Password'] = Password
        result['Email'] = Email
        result['FirstName'] = FirstName
        result['LastName'] = LastName
        result ['DateofBirth'] = DateofBirth
        result ['Gender'] = Gender
        return result

    def getAllAdministrators(self):
        dao = AdministratorsDAO()
        admin_list = dao.getAllAdministrators()
        result_list = []
        for row in admin_list:
            result = self.build_administrators_dict(row)
            result_list.append(result)
        return jsonify(Administrators=result_list)

    def getAdministratorById(self, AdministratorID):
        dao = AdministratorsDAO()
        row = dao.getAdministratorById(AdministratorID)
        if not row:
            return jsonify(Error = "Administrator Not Found"), 404
        else:
            administrators = self.build_administrators_dict(row)
            return jsonify(Administrators = administrators)

    def searchAdministrators(self, args):
        username = args.get("Username")
        password = args.get("Password")
        email = args.get("Email")
        dao = AdministratorsDAO()
        administrators_list = []
        if (len(args) == 2) and username and password:
            administrators_list = dao.getAdministratorbyUserNameandPassword(username, password)
        elif (len(args) == 1) and username:
            administrators_list = dao.getAdministratorbyUsername(username)
        elif (len(args) == 1) and email:
            administrators_list = dao.getAdministratorByEmail(email)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in administrators_list:
            result = self.build_administrators_dict(row)
            result_list.append(result)
        return jsonify(Administrators = result_list)

    def insertAdministrator(self, form):
        print("form: ", form)
        if len(form) != 7:
            return jsonify(Error = "Malformed post request"), 400
        else:
            username = form['UserName']
            password = form['Password']
            email = form['Email']
            firstname = form['FirstName']
            lastname = form['LastName']
            dateofbirth = form['DateofBirth']
            gender = form['Gender']
            if username and password and email and firstname and lastname and dateofbirth and gender:
                dao = AdministratorsDAO()
                administratorid = dao.insert(username, password, email, firstname, lastname, dateofbirth, gender)
                result = self.build_administrators_attributes(administratorid, username, password, email, firstname, lastname, dateofbirth,gender)
                return jsonify(Administrators=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertAdministratorJson(self, json):
        username = json['UserName']
        password = json['Password']
        email = json['Email']
        firstname = json['FirstName']
        lastname = json['LastName']
        dateofbirth = json['DateofBirth']
        gender = json['Gender']
        if username and password and email and firstname and lastname and dateofbirth and gender:
            dao = AdministratorsDAO()
            administratorid = dao.insert(username, password, email, firstname, lastname, dateofbirth, gender)
            result = self.build_administrators_attributes(administratorid, username, password, email, firstname, lastname, dateofbirth, gender)
            return jsonify(Administrators=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteAdministrator(self, administratorid):
        dao = AdministratorsDAO()
        if not dao.getAdministratorById(administratorid):
            return jsonify(Error = "Admin not found."), 404
        else:
            dao.delete(administratorid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateAdministrator(self, administratorid, form):
        dao = AdministratorsDAO()
        if not dao.getAdministratorById(administratorid):
            return jsonify(Error = "Admin not found."), 404
        else:
            if len(form) != 7:
                return jsonify(Error="Malformed update request"), 400
            else:
                username = form['UserName']
                password = form['Password']
                email = form['Email']
                firstname = form['FirstName']
                lastname = form['LastName']
                dateofbirth = form['DateofBirth']
                gender = form['Gender']
                if username and password and email and firstname and lastname and dateofbirth and gender:
                    dao.update(username, password, email, firstname, lastname, dateofbirth, gender)
                    result = self.build_administrators_attributes(username, password, email, firstname, lastname, dateofbirth, gender)
                    return jsonify(Administrators=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def updateAdministratorJson(self, adminid, json):
        dao = AdministratorsDAO()
        if not dao.getAdministratorById(adminid):
            return jsonify(Error="Admin not found."), 404
        else:
            username = json['UserName']
            password = json['Password']
            email = json['Email']
            firstname = json['FirstName']
            lastname = json['LastName']
            dateofbirth = json['DateofBirth']
            gender = json['Gender']
            if username and password and email and firstname and lastname and dateofbirth and gender:
                dao.update(adminid, username, password, email, firstname, lastname, dateofbirth, gender)
                result = self.build_administrators_attributes(adminid, username, password, email, firstname, lastname, dateofbirth, gender)
                return jsonify(Administrators=result), 200

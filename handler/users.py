from flask import jsonify
from dao.users import UsersDAO


class UsersHandler:
    def build_users_dict(self, row):
        result = {}
        result['UserID'] = row[0]
        result['UserName'] = row[1]
        result['Password'] = row[2]
        result['Email'] = row[3]
        result['PaymentMethod'] = row[4]
        result['ULocation'] = row[5]
        result['FirstName'] = row[6]
        result['LastName'] = row[7]
        result['DateofBirth'] = row[8]
        result['Gender'] = row[9]
        return result

    def build_users_attributes(self, UserID, UserName, Password, Email, PaymentMethod, ULocation, FirstName, LastName, DateofBirth, Gender):
        result = {}
        result['UserID'] = UserID
        result['UserName'] = UserName
        result['Password'] = Password
        result['Email'] = Email
        result['PaymentMethod'] = PaymentMethod
        result['ULocation'] = ULocation
        result['FirstName'] = FirstName
        result['LastName'] = LastName
        result ['DateofBirth'] = DateofBirth
        result ['Gender'] = Gender
        return result

    def getAllUsers(self):
        dao = UsersDAO()
        users_list = dao.getAllUsers()
        result_list = []
        for row in users_list:
            result = self.build_users_dict(row)
            result_list.append(result)
        return jsonify(Users=result_list)

    def getUserById(self, UserID):
        dao = UsersDAO()
        row = dao.getUserById(UserID)
        if not row:
            return jsonify(Error = "User Not Found"), 404
        else:
            users = self.build_users_dict(row)
            return jsonify(Users = users)

    def getUserByLocation(self, ULocation):
        dao = UsersDAO()
        row = dao.getUserById(ULocation)
        if not row:
            return jsonify(Error="User Not Found"), 404
        else:
            users = self.build_users_dict(row)
            return jsonify(Users=users)

    def searchUsers(self, args):
        username = args.get("Username")
        password = args.get("Password")
        email = args.get("Email")
        ulocation = args.get("ULocation")
        dao = UsersDAO()
        users_list = []
        if (len(args) == 2) and username and password:
            users_list = dao.getUserbyUserNameandPassword(username, password)
        elif (len(args) == 1) and username:
            users_list = dao.getUserbyUsername(username)
        elif (len(args) == 1) and email:
            users_list = dao.getUserByEmail(email)
        elif (len(args) == 1) and ulocation:
            users_list = dao.getUserByLocation(ulocation)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in users_list:
            result = self.build_users_dict(row)
            result_list.append(result)
        return jsonify(Users=result_list)

    def insertUser(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error = "Malformed post request"), 400
        else:
            username = form['UserName']
            password = form['Password']
            email = form['Email']
            firstname = form['FirstName']
            lastname = form['LastName']
            dateofbirth = form['DateofBirth']
            gender = form['Gender']
            if  username and password and email and firstname and lastname and dateofbirth and gender:
                dao = UsersDAO()
                userid = dao.insert(username, password, email, firstname, lastname, dateofbirth,gender)
                result = self.build_users_attributes(userid, username, password, email, firstname, lastname, dateofbirth,gender)
                return jsonify(Users=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertUserJson(self, json):
        username = json['UserName']
        password = json['Password']
        email = json['Email']
        firstname = json['FirstName']
        lastname = json['LastName']
        dateofbirth = json['DateofBirth']
        gender = json['Gender']
        if  username and password and email and firstname and lastname and dateofbirth and gender:
            dao = UsersDAO()
            userid = dao.insert(username, password, email, firstname, lastname, dateofbirth,gender)
            result = self.build_users_attributes(username, password, email, firstname, lastname, dateofbirth,gender)
            return jsonify(Users=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteUser(self, userid):
        dao = UsersDAO()
        if not dao.getUserById(userid):
            return jsonify(Error = "User not found."), 404
        else:
            dao.delete(userid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateUser(self, userid, form):
        dao = UsersDAO()
        if not dao.getUserById(userid):
            return jsonify(Error = "User not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request"), 400
            else:
                username = form['UserName']
                password = form['Password']
                email = form['Email']
                paymentmethod = form['PaymentMethod']
                ulocation = form['ULocation']
                firstname = form['FirstName']
                lastname = form['LastName']
                dateofbirth = form['DateofBirth']
                gender = form['Gender']
                if username and password and email and paymentmethod and ulocation and firstname and lastname and dateofbirth and gender:
                    dao.update(username, password, email, paymentmethod, ulocation, firstname, lastname, dateofbirth, gender)
                    result = self.build_users_attributes(username, password, email, paymentmethod, ulocation, firstname, lastname, dateofbirth, gender)
                    return jsonify(Users=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
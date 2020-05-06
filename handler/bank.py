from flask import jsonify
from dao.bank import BankDAO


class BankHandler:
    def build_bank_dict(self, row):
        result = {}
        result['BankID'] = row[0]
        result['CardID'] = row[1]
        result['UserID'] = row[2]
        result['BankName'] = row[3]
        return result

    def build_bank_attributes(self, BankID, CardID, UserID, BankName):
        result = {}
        result['BankID'] = BankID
        result['CardID'] = CardID
        result['UserID'] = UserID
        result['BankName'] = BankName
        return result

    def getAllBanks(self):
        dao = BankDAO()
        bank_list = dao.getAllBanks()
        result_list = []
        for row in bank_list:
            result = self.build_bank_dict(row)
            result_list.append(result)
        return jsonify(Banks=result_list)

    def getBankById(self, BankID):
        dao = BankDAO()
        row = dao.getBankById(BankID)
        if not row:
            return jsonify(Error = "Bank Not Found"), 404
        else:
            banks = self.build_bank_dict(row)
            return jsonify(Banks = banks)


    def searchBanks(self, args):
        cardid = args.get("CardID")
        userid = args.get("UserID")
        bankname = args.get("BankName")
        dao = BankDAO()
        bank_list = []
        if (len(args) == 2) and userid and cardid:
            bank_list = dao.getBankbyUserIDandCardID(userid, cardid)
        elif (len(args) == 1) and bankname:
            bank_list = dao.getBankbyBankName(bankname)
        elif (len(args) == 1) and userid:
            bank_list = dao.getBankbyUserID(userid)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in bank_list:
            result = self.build_bank_dict(row)
            result_list.append(result)
        return jsonify(Banks = result_list)

    def insertBank(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error = "Malformed post request"), 400
        else:
            cardid = form['CardID']
            userid = form['UserID']
            bankname = form['BankName']
            if cardid and userid and bankname:
                dao = BankDAO()
                bankid = dao.insert(cardid, userid, bankname)
                result = self.build_bank_attributes(bankid, cardid, userid, bankname)
                return jsonify(Bank=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertBankJson(self, json):
        cardid = json['CardID']
        userid = json['UserID']
        bankname = json['BankName']
        if cardid and userid and bankname:
            dao = BankDAO()
            bankid = dao.insert(cardid, userid, bankname)
            result = self.build_bank_attributes(bankid, cardid, userid, bankname)
            return jsonify(Banks=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteBank(self, bankid):
        dao = BankDAO()
        if not dao.getBankById(bankid):
            return jsonify(Error = "Bank not found."), 404
        else:
            dao.delete(bankid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateBank(self, bankid, form):
        dao = BankDAO()
        if not dao.getBankById(bankid):
            return jsonify(Error = "Bank not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request"), 400
            else:
                cardid = form['CardID']
                userid = form['UserID']
                bankname = form['BankName']
                if cardid and userid and bankname:
                    dao.update(cardid, userid, bankname)
                    result = self.build_bank_attributes(cardid, userid, bankname)
                    return jsonify(Banks=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def updateBankJson(self, bankid, json):
        dao = BankDAO()
        if not dao.getBankById(bankid):
            return jsonify(Error="Bank not found."), 404
        else:
            cardid = json['CardID']
            userid = json['UserID']
            bankname = json['BankName']
            if cardid and userid and bankname:
                dao.update(bankid, cardid, userid, bankname)
                result = self.build_bank_attributes(bankid, cardid, userid, bankname)
                return jsonify(Banks=result), 200

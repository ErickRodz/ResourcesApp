from flask import jsonify
from dao.paymentmethod import PaymentMethodDAO


class PaymentMethodHandler:
    def build_paymentmethod_dict(self, row):
        result = {}
        result['CardID'] = row[0]
        result['UserID'] = row[1]
        result['BankID'] = row[2]
        result['CardType'] = row[3]
        result['CardNumber'] = row[4]
        return result

    def build_paymentmethod_attributes(self, CardID, UserID, BankID, CardType, CardNumber):
        result = {}
        result['CardID'] = CardID
        result['UserID'] = UserID
        result['BankID'] = BankID
        result['CardType'] = CardType
        result['CardNumber'] = CardNumber
        return result

    def getAllCards(self):
        dao = PaymentMethodDAO()
        card_list = dao.getAllCards()
        result_list = []
        for row in card_list:
            result = self.build_paymentmethod_dict(row)
            result_list.append(result)
        return jsonify(Cards=result_list)

    def getAllCardsWithUsers(self):
        dao = PaymentMethodDAO()
        card_list = dao.getAllCardsWithUsers()
        result_list = []
        for row in card_list:
            result = self.build_paymentmethod_dict(row)
            result_list.append(result)
        return jsonify(Cards=result_list)

    def getCardById(self, CardID):
        dao = PaymentMethodDAO()
        row = dao.getCardbyID(CardID)
        if not row:
            return jsonify(Error = "Card Not Found"), 404
        else:
            cards = self.build_paymentmethod_dict(row)
            return jsonify(Cards = cards)

    def getCardByUserId(self, UserID):
        dao = PaymentMethodDAO()
        row = dao.getCardbyUserID(UserID)
        if not row:
            return jsonify(Error="Card Not Found"), 404
        else:
            cards = self.build_paymentmethod_dict(row)
            return jsonify(Cards=cards)


    def searchCards(self, args):
        cardid = args.get("CardID")
        userid = args.get("UserID")
        bankid = args.get("BankID")
        cardtype = args.get("CardType")
        cardnumber = args.get("CardNumber")
        dao = PaymentMethodDAO()
        cards_list = []
        if (len(args) == 1) and cardid:
            cards_list = dao.getCardbyID(cardid)
        elif (len(args) == 1) and userid:
            cards_list = dao.getCardbyUserID(userid)
        elif (len(args) == 1) and bankid:
            cards_list = dao.getCardbyBankID(bankid)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in cards_list:
            result = self.build_paymentmethod_dict(row)
            result_list.append(result)
        return jsonify(Cards=cards_list)

    def insertCard(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error = "Malformed post request"), 400
        else:
            userid = form['UserID']
            bankid = form['ResourceID']
            cardnumber = form['CardNumber']
            if userid and bankid and cardnumber:
                dao = PaymentMethodDAO()
                cardid = dao.insert(userid, bankid, cardnumber)
                result = self.build_paymentmethod_attributes(userid, bankid, cardnumber)
                return jsonify(Cards=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertCardJson(self, json):
        userid = json['UserID']
        bankid = json['ResourceID']
        cardtype = json['CardType']
        cardnumber = json['CardNumber']
        if userid and bankid and cardtype and cardnumber:
            dao = PaymentMethodDAO()
            cardid = dao.insert(userid, bankid, cardtype, cardnumber)
            result = self.build_paymentmethod_attributes(cardid, userid, bankid, cardtype, cardnumber)
            return jsonify(Cards=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteCard(self, cardid):
        dao = PaymentMethodDAO()
        if not dao.getCardbyID(cardid):
            return jsonify(Error = "Card not found."), 404
        else:
            dao.delete(cardid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateCard(self, cardid, form):
        dao = PaymentMethodDAO()
        if not dao.getCardbyID(cardid):
            return jsonify(Error = "Card not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request"), 400
            else:
                userid = form['UserID']
                bankid = form['BankID']
                cardnumber = form['BankNumber']
                if userid and bankid and cardnumber:
                    dao.update(cardid, userid, bankid, cardnumber)
                    result = self.build_paymentmethod_attributes(cardid, userid, bankid, cardnumber)
                    return jsonify(Cards=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def updateCardJson(self, cardid, json):
        dao = PaymentMethodDAO()
        if not dao.getCardbyID(cardid):
            return jsonify(Error="Card not found."), 404
        else:
            userid = json['UserID']
            bankid = json['BankID']
            cardtype = json['CardType']
            cardnumber = json['BankNumber']
            if userid and bankid and cardtype and cardnumber:
                dao.update(cardid, userid, bankid, cardtype, cardnumber)
                result = self.build_paymentmethod_attributes(cardid, userid, bankid, cardtype, cardnumber)
                return jsonify(Cards=result), 200
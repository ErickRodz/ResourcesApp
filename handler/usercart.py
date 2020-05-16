from flask import jsonify
from dao.usercart import UserCartDAO


class UserCartHandler:
    def build_usercart_dict(self, row):
        result = {}
        result['CartID'] = row[0]
        result['UserID'] = row[1]
        result['ResourceID'] = row[2]
        result['Selection'] = row[3]
        return result

    def build_usercart_attributes(self, CartID, UserID, ResourceID, Selection):
        result = {}
        result['CartID'] = CartID
        result['UserID'] = UserID
        result['ResourceID'] = ResourceID
        result['Selection'] = Selection
        return result

    def getAllCarts(self):
        dao = UserCartDAO()
        cart_list = dao.getAllCarts()
        result_list = []
        for row in cart_list:
            result = self.build_usercart_dict(row)
            result_list.append(result)
        return jsonify(Carts=result_list)

    def getCartById(self, CartID):
        dao = UserCartDAO()
        row = dao.getCartById(CartID)
        if not row:
            return jsonify(Error = "Cart Not Found"), 404
        else:
            carts = self.build_usercart_dict(row)
            return jsonify(Carts = carts)

    def getCartByUserId(self, UserID):
        dao = UserCartDAO()
        row = dao.getCartByUserId(UserID)
        if not row:
            return jsonify(Error="Cart Not Found"), 404
        else:
            carts = self.build_usercart_dict(row)
            return jsonify(Carts=carts)

    def getResourcesByCartId(self, CartID):
        dao = UserCartDAO()
        row = dao.getResourcesByCartId(CartID)
        if not row:
            return jsonify(Error="Cart not found"), 404
        else:
            carts = self.build_usercart_dict(row)
            return jsonify(Carts=carts)


    def searchUserCarts(self, args):
        cartid = args.get("CartID")
        userid = args.get("UserID")
        dao = UserCartDAO()
        carts_list = []
        if (len(args) == 1) and cartid:
            carts_list = dao.getCartbyID(cartid)
        elif (len(args) == 1) and userid:
            carts_list = dao.getCartbyUserID(userid)
        else:
            return jsonify(Error = "Malformed query string"), 400
        result_list = []
        for row in carts_list:
            result = self.build_usercart_dict(row)
            result_list.append(result)
        return jsonify(Carts=carts_list)

    def insertCart(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error = "Malformed post request"), 400
        else:
            userid = form['UserID']
            resourceid = form['ResourceID']
            selection = form['Selection']
            if userid and resourceid and selection:
                dao = UserCartDAO()
                cartid = dao.insert(userid, resourceid, selection)
                result = self.build_usercart_attributes(cartid, userid, resourceid, selection)
                return jsonify(Carts=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def insertCartJson(self, json):
        userid = json['UserID']
        resourceid = json['ResourceID']
        selection = json['Selection']
        if userid and resourceid and selection:
            dao = UserCartDAO()
            cartid = dao.insert(userid, resourceid, selection)
            result = self.build_usercart_attributes(cartid, userid, resourceid, selection)
            return jsonify(Carts=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteCart(self, cartid):
        dao = UserCartDAO()
        if not dao.getCartById(cartid):
            return jsonify(Error = "Cart not found."), 404
        else:
            dao.delete(cartid)
            return jsonify(DeleteStatus = "OK"), 200

    def updateUCart(self, cartid, form):
        dao = UserCartDAO()
        if not dao.getCartById(cartid):
            return jsonify(Error = "Cart not found."), 404
        else:
            if len(form) != 2:
                return jsonify(Error="Malformed update request"), 400
            else:
                resourceid = form['ResourceID']
                selection = form['Selection']
                if selection and resourceid:
                    dao.update(cartid, resourceid, selection)
                    userid = dao.getUserIdByCartId(cartid)
                    result = self.build_usercart_attributes(cartid, userid, resourceid, selection)
                    return jsonify(Carts=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def updateCartJson(self, cartid, json):
        dao = UserCartDAO()
        if not dao.getCartById(cartid):
            return jsonify(Error="Admin not found."), 404
        else:
            resourceid = json['ResourceID']
            selection = json['Selection']
            if selection and resourceid:
                dao.update(cartid, resourceid, selection)
                userid = dao.getUserIdByCartId(cartid)
                result = self.build_usercart_attributes(cartid, userid, resourceid)
                return jsonify(Carts=result), 200
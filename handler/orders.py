from flask import jsonify
from dao.orders import OrdersDAO


class OrdersHandler:
    def build_orders_dict(self, row):
        result = {}
        result['orderid'] = row[0]
        result['userid'] = row[1]
        result['cardid'] = row[2]
        result['cartid'] = row[3]
        result['resourceid'] = row[4]
        result['totalprice'] = row[5]
        result['totalquantity'] = row[6]
        result['resourcename'] = row[7]
        return result

    def build_orders_attributes(self, orderid, userid, cardid, cartid, resourceid, totalprice, totalquantity, resourcename):
        result = {}
        result['orderid'] = orderid
        result['userid'] = userid
        result['cardid'] = cardid
        result['cartid'] = cartid
        result['resourceid'] = resourceid
        result['totalprice'] = totalprice
        result['totalquantity'] = totalquantity
        result['resourcename'] = resourcename
        return result

    def getAllOrders(self):
        dao = OrdersDAO()
        orders_list = dao.getAllOrders()
        result_list = []

        for row in orders_list:
            result = self.build_orders_dict(row)
            result_list.append(result)

        return jsonify(Orders=result_list)

    def getOrdersByID(self, orderid):
        dao = OrdersDAO()
        row = dao.getOrderById(orderid)
        if not row:
            return jsonify(Error="Order Not Found "), 404
        else:
            order = self.build_orders_dict(row)
            return jsonify(Order=order)

    def getRequestedResourcesByResourceName(self, resorcename):
        dao = OrdersDAO()
        requests_list = dao.getResourcesRequestByResourceName(resorcename)
        result_list = []
        for row in requests_list:
            result = self.build_orders_dict(row)
            result_list.append(result)

        return jsonify(Orders=result_list)

    def searchOrders(self, args):
        userid = args.get('userid')
        cardid = args.get('cardid')
        cartid = args.get('cartid')
        resourceid = args.get('resourceid')
        dao = OrdersDAO()
        orders_list = []
        if (len(args) == 2) and userid and resourceid:
            orders_list = dao.getOrdersByUserIdAndResourceId(userid, resourceid)
        elif (len(args) == 2) and cardid and resourceid:
            orders_list = dao.getOrdersByCardIdAndResourceId(cardid, resourceid)
        elif (len(args) == 1) and userid:
            orders_list = dao.getOrdersByUserId(userid)
        elif (len(args) == 1) and cardid:
            orders_list = dao.getOrdersbyCardId(cardid)
        elif (len(args) == 1) and cartid:
            orders_list = dao.getOrderByCartId(cartid)
        elif (len(args) == 1) and resourceid:
            orders_list = dao.getOrdersByResourceId(resourceid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in orders_list:
            result = self.build_orders_dict(row)
            result_list.append(result)
        return jsonify(Orders=result_list)

    def insertOrders(self, form):
        if len(form) != 5 :
            return jsonify(Error="Malformed post request")
        resourceid = form['resourceid']
        userid = form['userid']
        cardid = form['cardid']
        cartid = form['cartid']
        totalquantity = form['totalquantity']
        if resourceid and userid and cardid and cartid and totalquantity:
            dao = OrdersDAO()
            resourcequantity = dao.getResourceQuantityByResourceId(resourceid)
            if totalquantity>resourcequantity:
                return jsonify(Error="Inserted quantity exceeds the resources current stock")
            else:
                resourceprice = dao.getResourcePriceByResourceId(resourceid)
                totalprice = totalquantity*resourceprice
                orderid = dao.insert(userid, cardid, cartid, resourceid, totalprice, totalprice)
                result = self.build_orders_attributes(orderid, userid, cardid, cartid,
                                                    resourceid, totalprice, totalquantity)
                return jsonify(Order=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertOrderJson(self, json):
        resourceid = json['resourceid']
        userid = json['userid']
        cardid = json['cardid']
        cartid = json['cartid']
        totalquantity = json['totalquantity']
        if resourceid and userid and cardid and cartid and totalquantity:
            dao = OrdersDAO()
            resourcequantity = dao.getResourceQuantityByResourceId(resourceid)
            if totalquantity > resourcequantity:
                return jsonify(Error="Inserted quantity exceeds the resources current stock")
            else:
                resourceprice = dao.getResourcePriceByResourceId(resourceid)
                totalprice = totalquantity * resourceprice
                orderid = dao.insert(userid, cardid, cartid, resourceid, totalprice, totalprice)
                result = self.build_orders_attributes(orderid, userid, cardid, cartid,
                                                      resourceid, totalprice, totalquantity)
                return jsonify(Order=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteOrder(self, orderid):
        dao = OrdersDAO()
        if not dao.getOrderById(orderid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(orderid)
            return jsonify(DeleteStatus="OK"), 200

    def updateOrder(self, orderid, resourceid, form):
        dao = OrdersDAO()
        if not dao.getOrderById(orderid):
            return jsonify(Error="Order not found."), 404
        else:
            if len(form) != 2 or resourceid != dao.getResourceIdByOrderId(orderid):
                return jsonify(Error="Malformed update request")
            else:

                totalquantity = form['totalquantity']
                resourcename = form['resourcename']
                if  totalquantity and resourcename:
                    resourceprice = dao.getResourcePriceByResourceId(resourceid)
                    totalprice = totalquantity * resourceprice
                    dao.update(totalprice, totalquantity, resourcename, orderid)
                    userid = dao.getUserIdIdByOrderId(orderid)
                    cardid = dao.getCardIdIdByOrderId(orderid)
                    cartid = dao.getCartidByOrderId(orderid)
                    result = self.build_orders_attributes(orderid, userid, cardid, cartid,
                                                            resourceid, totalprice, totalquantity, resourcename)
                    return jsonify(Order=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateOrderJson(self, orderid, resourceid, json):
        dao = OrdersDAO()
        if not dao.getOrderById(orderid):
            return jsonify(Error="Order not found."), 404
        elif resourceid != dao.getResourceIdByOrderId(orderid):
            return jsonify(Error="Malformed update request")

        else:

            totalquantity = json['totalquantity']
            resourcename = json['resourcename']
            if totalquantity and resourcename:
                resourceprice = dao.getResourcePriceByResourceId(resourceid)
                totalprice = totalquantity * resourceprice
                dao.update(totalprice, totalquantity, resourcename, orderid)
                userid = dao.getUserIdIdByOrderId(orderid)
                cardid = dao.getCardIdIdByOrderId(orderid)
                cartid = dao.getCartidByOrderId(orderid)
                result = self.build_orders_attributes(orderid, userid, cardid, cartid,
                                                      resourceid, totalprice, totalquantity, resourcename)
                return jsonify(Order=result), 200
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400











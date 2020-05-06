from flask import jsonify
from dao.orders import OrdersDAO


class OrdersHandler:
    def build_orders_dict(self, row):
        result = {}
        result['orderid'] = row[0]
        result['totalprice'] = row[1]
        result['totalquantity'] = row[2]
        result['userid'] = row[3]
        result['cardid'] = row[4]
        result['cartid'] = row[5]
        result['resourceid'] = row[6]
        result['resourcename'] = row[7]
        result['ordertype'] = row[8]
        return result

    def build_orders_attributes(self, orderid, totalprice, totalquantity, userid, cardid, cartid, resourceid, resourcename, ordertype):
        result = {}
        result['orderid'] = orderid
        result['totalprice'] = totalprice
        result['totalquantity'] = totalquantity
        result['userid'] = userid
        result['cardid'] = cardid
        result['cartid'] = cartid
        result['resourceid'] = resourceid
        result['resourcename'] = resourcename
        result['ordertype'] = ordertype
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

    def getOrdersByOrderType(self, ordertype):
        dao = OrdersDAO()
        request_list = dao.getOrderByOrderType(ordertype)
        result_list = []
        for row in request_list:
            result = self.build_orders_dict(row)
            result_list.append(result)

        return jsonify(Orders=result_list)

    def getRequestByOrderID(self, orderid):
        dao = OrdersDAO()
        request_list = dao.getRequestsByOrderID(orderid)
        result_list = []
        for row in request_list:
            result = self.build_orders_dict(row)
            result_list.append(result)

        return jsonify(Orders=result_list)

    def getRequestedResourcesByResourceName(self, resorcename):
        dao = OrdersDAO()
        requests_list = dao.getResourcesRequestByResourceName(resorcename)
        result_list = []
        for row in requests_list:
            result = self.build_orders_dict(row)
            result_list.append(result)

        return jsonify(Orders=result_list)

    def getReciptsByCartIdAndOrderType(self, cartid, ordertype):
        dao = OrdersDAO()
        requests_list = dao.getReceiptsFromOrdersByCartIdAndOrderType(cartid, ordertype)
        result_list = []
        for row in requests_list:
            result = self.build_orders_dict(row)
            result_list.append(result)

        return jsonify(Orders=result_list)

    def getReciptsByUserIdAndOrderType(self, userid, ordertype):
        dao = OrdersDAO()
        requests_list = dao.getReceiptsFromOrdersByUserIdAndOrderType(userid, ordertype)
        result_list = []
        for row in requests_list:
            result = self.build_orders_dict(row)
            result_list.append(result)

        return jsonify(Orders=result_list)

    def getResourcesOrderedByCategory(self, ordertype, resourcename):
        dao = OrdersDAO()
        resourceid = dao.getResourceIdByResourceName(resourcename)
        categoryname = dao.getCategoryNameByResourceId(resourceid)
        requests_list = dao.getResourcesByOrderType(ordertype, categoryname)
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
        ordertype = args.get('ordertype')
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
        if len(form) != 8 :
            return jsonify(Error="Malformed post request")
        totalprice = form['totalprice']
        totalquantity = form['totalquantity']
        userid = form['userid']
        cardid = form['cardid']
        cartid = form['cartid']
        resourceid = form['resourceid']
        resourcename = form['resourcename']
        ordertype = form['ordertype']
        if resourceid and userid and cardid and cartid and totalquantity and ordertype and totalprice:
            dao = OrdersDAO()
            resourcequantity = dao.getResourceQuantityByResourceId(resourceid)
            if totalquantity>resourcequantity:
                return jsonify(Error="Inserted quantity exceeds the resources current stock")
            elif ordertype == 'Request':
                totalquantity = 0
                totalprice = 0
                orderid = dao.insert(totalprice, totalquantity, userid, cardid, cartid, resourceid, resourcename, ordertype)
                result = self.build_orders_attributes(orderid, totalprice, totalquantity, userid, cardid, cartid,
                                                      resourceid, resourcename, ordertype)
                return jsonify(Order=result), 201
            elif ordertype == 'Reservation':
                totalprice = 0
                orderid = dao.insert(totalprice, totalquantity,userid, cardid, cartid, resourceid, resourcename, ordertype)
                result = self.build_orders_attributes(orderid, totalprice, totalquantity,userid, cardid, cartid, resourceid, resourcename, ordertype)
                newquantity = resourcequantity - totalquantity
                dao.updateResourceQuantity(newquantity, resourceid)
                return jsonify(Order=result), 201
            else:
                resourceprice = dao.getResourcePriceByResourceId(resourceid)
                totalprice = totalquantity*resourceprice
                orderid = dao.insert(totalprice, totalquantity,userid, cardid, cartid, resourceid, resourcename, ordertype)
                result = self.build_orders_attributes(orderid, totalprice, totalquantity,userid, cardid, cartid, resourceid, resourcename, ordertype)
                newquantity = resourcequantity - totalquantity
                dao.updateResourceQuantity(newquantity, resourceid)
                return jsonify(Order=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertOrderJson(self, json):
        totalprice = json['totalprice']
        totalquantity = json['totalquantity']
        userid = json['userid']
        cardid = json['cardid']
        cartid = json['cartid']
        resourceid = json['resourceid']
        resourcename = json['resourcename']
        ordertype = json['ordertype']
        if resourceid and userid and cardid and cartid and totalquantity and ordertype and totalprice:
            dao = OrdersDAO()
            resourcequantity = dao.getResourceQuantityByResourceId(resourceid)
            if totalquantity > resourcequantity:
                return jsonify(Error="Inserted quantity exceeds the resources current stock")
            elif ordertype == 'Request':
                totalquantity = 0
                totalprice = 0
                orderid = dao.insert(totalprice, totalquantity, userid, cardid, cartid, resourceid, resourcename,
                                     ordertype)
                result = self.build_orders_attributes(orderid, totalprice, totalquantity, userid, cardid, cartid,
                                                      resourceid, resourcename, ordertype)
                return jsonify(Order=result), 201
            elif ordertype == 'Reservation':
                totalprice = 0
                orderid = dao.insert(totalprice, totalquantity, userid, cardid, cartid, resourceid, resourcename,
                                     ordertype)
                result = self.build_orders_attributes(orderid, totalprice, totalquantity, userid, cardid, cartid,
                                                      resourceid, resourcename, ordertype)
                newquantity = resourcequantity - totalquantity
                dao.updateResourceQuantity(newquantity, resourceid)
                return jsonify(Order=result), 201
            else:
                resourceprice = dao.getResourcePriceByResourceId(resourceid)
                totalprice = totalquantity * resourceprice
                orderid = dao.insert(totalprice, totalquantity, userid, cardid, cartid, resourceid, resourcename,
                                     ordertype)
                result = self.build_orders_attributes(orderid, totalprice, totalquantity, userid, cardid, cartid,
                                                      resourceid, resourcename, ordertype)
                newquantity = resourcequantity - totalquantity
                dao.updateResourceQuantity(newquantity, resourceid)
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











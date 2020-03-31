from flask import jsonify
from dao.purchaselog import PurchaseLogDAO


class PurchaseLogHandler:
    def build_users_dict(self, row):
        result = {}
        result['purchaseId'] = row[0]
        result['userId'] = row[1]
        result['resourceId'] = row[2]
        return result
    
    def build_users_attributes(self, purchaseId, userId, resourceId):
        result = {}
        result['purchaseId'] = purchaseId
        result['userId'] = userId
        result['resourceId'] = resourceId
        return result
    
    def getAllPurchaseLogs(self):
        dao = PurchaseLogDAO()
        purchase_list = dao.getAllPurchaseLogs()
        result_list = []
        for row in purchase_list:
            result = self.build_users_dict(row)
            result_list.append(result)
        return jsonify(PurchaseLog = result_list)

    def getPurchaseLogById(self, purchaseId):
        dao = PurchaseLogDAO()
        row = dao.getPurchaseLogById(purchaseId)
        if not row:
            return jsonify(Error = "Purchase id not found"), 404
        else:
            purchaseLog = self.build_users_dict(row)
            return jsonify(PurchaseLog = purchaseLog)

    def getPurchaseLogsByUserId(self, userId):
        dao = PurchaseLogDAO()
        purchase_list = dao.getPurchaseLogsByUserId(userId)
        result_list = []
        for row in purchase_list:
            result = self.build_users_dict(row)
            result_list.append(result)
        return result_list

    def getPurchaseLogsByResourceId(self, resourceId):
        dao = PurchaseLogDAO()
        purchase_list = dao.getPurchaseLogsByResourceId(resourceId)
        result_list = []
        for row in purchase_list:
            result = self.build_users_dict(row)
            result_list.append(result)
        return result_list
    
    def insertPurchaseLog(self, form):
        if len(form) != 2:
            return jsonify(Error = "Malformed post request"), 400
        else:
            userId = form['userId']
            resourceId = form['resourceId']
            if userId and resourceId:
                dao = PurchaseLogDAO()
                purchaseId = dao.insert(userId, resourceId)
                result = self.build_users_attributes(purchaseId, userId, resourceId)
                return jsonify(PurchaseLog = result), 201
            else:
                return jsonify(Error = "Unexpected attributes in post request"), 404
    
    def insertPurchaseLogJson(self, json):
        userId = json['userId']
        resourceId = json['resourceId']
        if userId and resourceId:
            dao = PurchaseLogDAO()
            purchaseId = dao.insert(userId, resourceId)
            result = self.build_users_attributes(purchaseId, userId, resourceId)
            return jsonify(PurchaseLog = result)

    def deletePurchaseLog(self, purchaseId):
        dao = PurchaseLogDAO()
        if not dao.getPurchaseLogById(purchaseId):
            return jsonify(Error = "Purchase id not found"), 404
        else:
            dao.delete(purchaseId)
            return jsonify(DeleteStatus = "OK"), 200
    
    def updatePurchaseLogJson(self, purchaseId, json):
        dao = PurchaseLogDAO()
        if not dao.getPurchaseLogById(purchaseId):
            return jsonify(Error = "Purchase id not found"), 404
        else:
            userId = json['userId']
            resourceId = json['resourceId']
            if userId and resourceId:
                dao.update(purchaseId, userId, resourceId)
                result = self.build_users_attributes(purchaseId, userId, resourceId)
                return jsonify(PurchaseLog = result), 200
            else:
                return jsonify(Error = "Unexpected attributes in put request"), 404
    
    def updatePurchaseLog(self, purchaseId, form):
        dao = PurchaseLogDAO()
        if not dao.getPurchaseLogById(purchaseId):
            return jsonify(Error = "Purchase id not found"), 404
        else:
            userId = form[0]
            resourceId = form[1]
            if userId and resourceId:
                dao.update(purchaseId, userId, resourceId)
                result = self.build_users_attributes(purchaseId, userId, resourceId)
                return jsonify(PurchaseLog = result), 200
            else:
                return jsonify(Error = "Unexpected attributes in put request"), 404

from flask import jsonify
from dao.cannedfood import CannedFoodDAO


class CannedFoodHandler:
    def build_cannedfood_dict(self, row):
        result = {}
        result['CFoodID'] = row[0]
        result['CFoodServing'] = row[1]
        result['CFoodDescription'] = row[2]
        result['ResourceID'] = row[3]
        return result

    def build_cannedfood_attributes(self, cfoodid, cfoodserving, cfooddescription, resourceid,):
        result = {}
        result['CFoodID'] = cfoodid
        result['CFoodServing'] = cfoodserving
        result['CFoodDescription'] = cfooddescription
        result['ResourceID'] = resourceid
        return result

    def getAllCannedFood(self):
        dao = CannedFoodDAO()
        cannedfood_list = dao.getAllCannedFood()
        result_list = []
        for row in cannedfood_list:
            result = self.build_cannedfood_dict(row)
            result_list.append(result)
        return jsonify(CannedFood=cannedfood_list)

    def getCannedFoodByID(self, cfoodid):
        dao = CannedFoodDAO()
        row = dao.getCannedFoodById(cfoodid)
        if not row:
            return jsonify(Error="Canned Food Not Found "), 404
        else:
            cfood = self.build_cannedfood_dict(row)
            return jsonify(CFood=cfood)

    def searchCannedFood(self, args):
        supplierid = args.get("supplierid")
        dao = CannedFoodDAO()
        cannedfood_list = []
        if (len(args) == 1) and supplierid:
            cannedfood_list = dao.getCannedFoodBySupplier(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in cannedfood_list:
            result = self.build_cannedfood_dict(row)
            result_list.append(result)
        return jsonify(CannedFood=result_list)
    
    def getCFoodByResourceID(self, resourceid):
        dao = CannedFoodDAO()
        row = dao.getCFoodByResourceID(resourceid)
        if not row:
            return jsonify(Error="CannedFood Not Found "), 404
        else:
            CannedFood = self.build_cannedfood_dict(row)
            return jsonify(CannedFood=CannedFood)

    def getResourceIDByCFoodID(self, CannedFoodid):
        dao = CannedFoodDAO()
        row = dao.getResourceIDByCFoodID(CannedFoodid)
        if not row:
            return jsonify(Error="CannedFood Not Found "), 404
        else:
            CannedFood = self.build_cannedfood_dict(row)
            return jsonify(CannedFood=CannedFood)


    def insertCFood(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error="Malformed post request")
        cfoodserving = form['CFoodServing']
        cfooddescription = form['CFoodDescription']
        resourceid = form['ResourceID']
        if cfoodserving and cfooddescription and resourceid:
            dao = CannedFoodDAO()
            cfoodid = dao.insert(cfoodserving, cfooddescription, resourceid,)
            result = self.build_cannedfood_attributes(cfoodid, cfoodserving, cfooddescription, resourceid, )
            return jsonify(cfood=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertCFoodJson(self, json):
        cfoodserving = json['CFoodServing']
        cfooddescription = json['CFoodDescription']
        resourceid = json['ResourceID']
        if cfoodserving and cfooddescription and resourceid:
            dao = CannedFoodDAO()
            cfoodid = dao.insert(cfoodserving, cfooddescription, resourceid)
            result = self.build_cannedfood_attributes(cfoodid, cfoodserving, cfooddescription, resourceid)
            return jsonify(cfood=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteCFood(self, cfoodid):
        dao = CannedFoodDAO()
        if not dao.getCannedFoodById(cfoodid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(cfoodid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, cfoodid, form):
        dao = CannedFoodDAO()
        if not dao.getCannedFoodById(cfoodid):
            return jsonify(Error="Canned Food not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request")
            else:
                cfoodserving = form['CFoodServing']
                cfooddescription = form['CFoodDescription']
                if cfoodserving and cfooddescription:
                    dao.update(cfoodid, cfoodserving, cfooddescription)
                    resourceid = dao.getResourceIDByCFoodID(cfoodid)
                    result = self.build_cannedfood_attributes(cfoodid, cfoodserving, cfooddescription, resourceid)
                    return jsonify(CFood=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, cfoodid, json):
        dao = CannedFoodDAO()
        if not dao.getCannedFoodById(cfoodid):
            return jsonify(Error="Baby Food not found."), 404
        else:
            cfoodserving = json['CFoodServing']
            cfooddescription = json['CFoodDescription']
            if cfoodserving and cfooddescription:
                dao.update(cfoodid, cfoodserving, cfooddescription)
                resourceid = dao.getResourceIDByCFoodID(cfoodid)
                result = self.build_cannedfood_attributes(cfoodid, cfoodserving, cfooddescription, resourceid,)
                return jsonify(cfood=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400







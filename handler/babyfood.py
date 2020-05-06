from flask import jsonify
from dao.babyfood import BabyFoodDAO


class BabyFoodHandler:
    def build_babyfood_dict(self, row):
        result = {}
        result['bfoodid'] = row[0]
        result['bfoodflavor'] = row[1]
        result['bfooddescription'] = row[2]
        result['resourceid'] = row[3]
        return result

    def build_babyfood_attributes(self, bfoodid, bfoodflavor, bfooddescription, resourceid,):
        result = {}
        result['bfoodid'] = bfoodid
        result['bfoodflavor'] = bfoodflavor
        result['bfooddescription'] = bfooddescription
        result['resourceid'] = resourceid
        return result

    def getAllBabyFood(self):
        dao = BabyFoodDAO()
        babyfood_list = dao.getAllBabyFood()
        result_list = []
        for row in babyfood_list:
            result = self.build_babyfood_dict(row)
            result_list.append(result)
        return jsonify(babyfood=babyfood_list)

    def getBabyFoodByID(self, bfoodid):
        dao = BabyFoodDAO()
        row = dao.getBabyFoodById(bfoodid)
        if not row:
            return jsonify(Error="BabyFood Not Found "), 404
        else:
            bfood = self.build_babyfood_dict(row)
            return jsonify(BFood=bfood)

    def getBabyFoodByResourceID(self, resourceid):
        dao = BabyFoodDAO()
        row = dao.getBFoodByResourceID(resourceid)
        if not row:
            return jsonify(Error="BabyFood Not Found "), 404
        else:
            bfood = self.build_babyfood_dict(row)
            return jsonify(BFood=bfood)

    def getResourceIDByBabyFoodID(self, bfoodid):
        dao = BabyFoodDAO()
        row = dao.getResourceIDByBFoodID(bfoodid)
        if not row:
            return jsonify(Error="BabyFood Not Found "), 404
        else:
            bfood = self.build_babyfood_dict(row)
            return jsonify(BFood=bfood)


    def searchBabyFood(self, args):
        supplierid = args.get("supplierid")
        dao = BabyFoodDAO()
        babyfood_list = []
        if (len(args) == 1) and supplierid:
            babyfood_list = dao.getBabyFoodBySupplier(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in babyfood_list:
            result = self.build_babyfood_dict(row)
            result_list.append(result)
        return jsonify(babyfood=result_list)

    def insertBFood(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request")
        bfoodflavor = form['BFoodFlavor']
        bfooddescription = form['BFoodDescription']
        resourceid = form['ResourceID']
        if bfoodflavor and bfooddescription and resourceid:
            dao = BabyFoodDAO()
            bfoodid = dao.insert(bfoodflavor, bfooddescription, resourceid,)
            result = self.build_babyfood_attributes(bfoodid, bfoodflavor, bfooddescription, resourceid, )
            return jsonify(bfood=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertbfoodJson(self, json):
        bfoodflavor = json['BfoodFlavor']
        bfooddescription = json['BFoodDescription']
        resourceid = json['ResourceID']
        if bfoodflavor and bfooddescription and resourceid:
            dao = BabyFoodDAO()
            bfoodid = dao.insert(bfoodflavor, bfooddescription, resourceid, )
            result = self.build_babyfood_attributes(bfoodid, bfoodflavor, bfooddescription, resourceid, )
            return jsonify(bfood=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteBFood(self, bfoodid):
        dao = BabyFoodDAO()
        if not dao.getBabyFoodById(bfoodid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(bfoodid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, bfoodid, form):
        dao = BabyFoodDAO()
        if not dao.getBabyFoodById(bfoodid):
            return jsonify(Error="Baby Food not found."), 404
        else:
            if len(form) != 2:
                return jsonify(Error="Malformed update request")
            else:
                bfoodflavor = form['BFoodFlavor']
                bfooddescription = form['BFoodDescription']
                if bfoodflavor and bfooddescription:
                    dao.update(bfoodid, bfoodflavor, bfooddescription)
                    resourceid = dao.getResourceIDByBFoodID(bfoodid)
                    result = self.build_babyfood_attributes(bfoodid, bfoodflavor, bfooddescription, resourceid)
                    return jsonify(bfood=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, bfoodid, json):
        dao = BabyFoodDAO()
        if not dao.getBabyFoodById(bfoodid):
            return jsonify(Error="Baby Food not found."), 404
        else:
            bfoodflavor = json['BFoodFlavor']
            bfooddescription = json['BFoodDescription']
            if bfoodflavor and bfooddescription:
                dao.update(bfoodid, bfoodflavor, bfooddescription)
                resourceid = dao.getResourceIDByBFoodID(bfoodid)
                result = self.build_babyfood_attributes(bfoodid, bfoodflavor, bfooddescription, resourceid)
                return jsonify(bfood=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400







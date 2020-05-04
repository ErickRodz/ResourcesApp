from flask import jsonify
from dao.dryfood import DryFoodDAO


class ResourceHandler:
    def build_dryfood_dict(self, row):
        result = {}
        result['DFoodID'] = row[0]
        result['DFoodServing'] = row[1]
        result['DFoodDescription'] = row[2]
        result['ResourceID'] = row[3]
        return result

    def build_dryfood_attributes(self, dfoodid, dfoodserving, dfooddescription, resourceid,):
        result = {}
        result['DFoodID'] = dfoodid
        result['DFoodServing'] = dfoodserving
        result['DFoodDescription'] = dfooddescription
        result['ResourceID'] = resourceid
        return result

    def getAllDryFood(self):
        dao = DryFoodDAO()
        dryfood_list = dao.getAllDryFood()
        result_list = []
        for row in dryfood_list:
            result = self.build_dryfood_dict(row)
            result_list.append(result)
        return jsonify(dryfood=dryfood_list)

    def getDryFoodByID(self, dfoodid):
        dao = DryFoodDAO()
        row = dao.getDryFoodById(dfoodid)
        if not row:
            return jsonify(Error="Dry Food Not Found "), 404
        else:
            dfood = self.build_dryfood_dict(row)
            return jsonify(dfood=dfood)

    def searchDryFood(self, args):
        supplierid = args.get("supplierid")
        dao = DryFoodDAO()
        dryfood_list = []
        if (len(args) == 1) and supplierid:
            dryfood_list = dao.getDryFoodBySupplier(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in dryfood_list:
            result = self.build_dryfood_dict(row)
            result_list.append(result)
        return jsonify(dryfood=result_list)

    def insertDFood(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error="Malformed post request")
        dfoodserving = form['DFoodServing']
        dfooddescription = form['DFoodDescription']
        resourceid = form['ResourceID']
        if dfoodserving and dfooddescription and resourceid:
            dao = DryFoodDAO()
            dfoodid = dao.insert(dfoodserving, dfooddescription, resourceid,)
            result = self.build_dryfood_attributes(dfoodid, dfoodserving, dfooddescription, resourceid, )
            return jsonify(dfood=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertDFoodJson(self, json):
        dfoodserving = json['DFoodServing']
        dfooddescription = json['DFoodDescription']
        resourceid = json['ResourceID']
        if dfoodserving and dfooddescription and resourceid:
            dao = DryFoodDAO()
            dfoodid = dao.insert(dfoodserving, dfooddescription, resourceid, )
            result = self.build_dryfood_attributes(dfoodid, dfoodserving, dfooddescription, resourceid, )
            return jsonify(dfood=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteDFood(self, dfoodid):
        dao = DryFoodDAO()
        if not dao.getDryFoodById(dfoodid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(dfoodid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, dfoodid, form):
        dao = DryFoodDAO()
        if not dao.getDryFoodById(dfoodid):
            return jsonify(Error="Canned Food not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request")
            else:
                dfoodserving = form['DFoodServing']
                dfooddescription = form['DFoodDescription']
                if dfoodserving and dfooddescription:
                    dao.update(dfoodid, dfoodserving, dfooddescription)
                    resourceid = dao.getResourceIDByDFoodID(dfoodid)
                    result = self.build_dryfood_attributes(dfoodid, dfoodserving, dfooddescription, resourceid)
                    return jsonify(dfood=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, dfoodid, json):
        dao = DryFoodDAO()
        if not dao.getdryfoodById(dfoodid):
            return jsonify(Error="Baby Food not found."), 404
        else:
            dfoodserving = json['DFoodServing']
            dfooddescription = json['DFoodDescription']
            if dfoodserving and dfooddescription:
                dao.update(dfoodid, dfoodserving, dfooddescription)
                resourceid = dao.getResourceIDByDFoodID(dfoodid)
                result = self.build_dryfood_attributes(dfoodid, dfoodserving, dfooddescription, resourceid)
                return jsonify(dfood=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400







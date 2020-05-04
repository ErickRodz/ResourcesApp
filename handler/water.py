from flask import jsonify
from dao.water import WaterDAO

class ResourceHandler:
    def build_water_dict(self, row):
        result = {}
        result['waterid'] = row[0]
        result['resourceid'] = row[1]
        result['watersize'] = row[2]
        result['waterdescription'] = row[3]
        return result
    
    def build_water_attributes(self, waterid, resourceid, watersize, waterdescription):
        result = {}
        result['waterid'] = waterid
        result['resourceid'] = resourceid
        result['watersize'] = watersize
        result['waterdescription'] = waterdescription
        return result

    def getAllWater(self):
        dao = WaterDAO()
        water_list = dao.getAllWater()
        result_list = []
        for row in water_list:
            result = self.build_water_dict(row)
            result_list.append(result)
        return jsonify(Water=result_list)
    
    def getWaterByID(self, waterid):
        dao = WaterDAO()
        row = dao.getWaterById(waterid)
        if not row:
            return jsonify(Error="Water Not Found "), 404
        else:
            water = self.build_water_dict(row)
            return jsonify(Water=water)

    def searchWater(self, args):
        watersize = args.get("watersize")
        supplierid = args.get("supplierid")
        dao = WaterDAO()
        water_list = []
        if (len(args) == 2) and watersize and supplierid:
            water_list = dao.getWaterBySupplierAndSize(supplierid, watersize)
        elif (len(args) == 1) and supplierid:
            water_list = dao.getWaterBySupplier(supplierid)
        elif (len(args) == 1) and watersize:
            water_list = dao.getWaterBySize(watersize)
        else:
            return jsonify(Error="Malformed query string"), 404
        result_list =[]
        for row in water_list:
            result = self.build_water_dict(row)
            result_list.append(row)
        return jsonify(Water=result_list)

    def insertWater(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error="Malformed post request")
        resourceid = form['resourceid']
        watersize = form['watersize']
        waterdescription = form['waterdescription']
        if resourceid and watersize and waterdescription:
            dao = WaterDAO()
            waterid = dao.insert(resourceid, watersize, waterdescription)
            result = self.build_water_attributes(waterid, resourceid, watersize, waterdescription)
            return jsonify(Water=result)
        else:
            return jsonify(Error="Unexpected attributes in post request")
    
    def deleteWater(self, waterid):
        dao = WaterDAO()    
        if not dao.getWaterById(waterid):
            return jsonify(Error="Resource not found"), 404
        else:
            dao.delete(waterid)
            return jsonify(DeleteStatus="OK"), 200
    
    def updateResource(self, waterid, form):
        dao = WaterDAO()
        if not dao.getWaterById(waterid):
            return jsonify(Error="Resource not found"), 404
        else:
            if (len(form) != 2):
                return jsonify(Error="Malformed update request")
            else:
                watersize = form['watersize']
                waterdescription = form['waterdescription']
                if watersize and waterdescription:
                    dao.update(waterid, watersize, waterdescription)
                    resourceid = dao.getResourceIDByWaterID(waterid)
                    result = self.build_water_attributes(waterid, resourceid, watersize, waterdescription)
                    return jsonify(Water=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 404 

    def updateResourceJson(self, waterid, json):
        dao = WaterDAO()
        if not dao.getWaterById(waterid):
            return jsonify(Error="Resource not found"), 404
        else:
            watersize = json['watersize']
            waterdescription = json['waterdescription']
            if watersize and waterdescription:
                dao.update(waterid, watersize, waterdescription)
                resourceid = dao.getResourceIDByWaterID(waterid)
                result = self.build_water_attributes(waterid, resourceid, watersize, waterdescription)
                return jsonify(Water=result), 200
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400
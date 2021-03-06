from flask import jsonify
from dao.heavyequipment import HeavyEquipmentDAO


class HeavyEquipmentHandler:
    def build_heavyequipment_dict(self, row):
        result = {}
        result['HeavyEqID'] = row[0]
        result['HeavyEqBrand'] = row[1]
        result['HeavyEqDescription'] = row[2]
        result['ResourceID'] = row[3]
        return result

    def build_heavyequipment_attributes(self, HeavyEquipmentid, HeavyEquipmentbrand, HeavyEquipmentdescription, resourceid):
        result = {}
        result['HeavyEqID'] = HeavyEquipmentid
        result['HeavyEqBrand'] = HeavyEquipmentbrand
        result['HeavyEqDescription'] = HeavyEquipmentdescription
        result['ResourceID'] = resourceid
        return result

    def build_heavydetails_dict(self, row):
        result = {}
        result['ResourceID'] = row[0]
        result['ResourceName'] = row[1]
        result['ResourcePrice'] = row[2]
        result['ResourceQuantity'] = row[3]
        result['SupplierID'] = row[4]
        result['HeavyEqID'] = row[5]
        result['HeavyEqBrand'] = row[6]
        result['HeavyEqDescription'] = row[7]
        return result

    def getAllHeavyEquipment(self):
        dao = HeavyEquipmentDAO()
        HeavyEquipment_list = dao.getAllHeavyEquipment()
        result_list = []
        for row in HeavyEquipment_list:
            result = self.build_heavyequipment_dict(row)
            result_list.append(result)

        return jsonify(HeavyEquipment=HeavyEquipment_list)

    def getHeavyEquipmentByID(self, HeavyEquipmentid):
        dao = HeavyEquipmentDAO()
        row = dao.getHeavyEquipmentById(HeavyEquipmentid)
        if not row:
            return jsonify(Error="HeavyEquipment Not Found "), 404
        else:
            HeavyEquipment = self.build_heavyequipment_dict(row)
            return jsonify(HeavyEquipment=HeavyEquipment)

    def getHeavyEquipmentByResourceID(self, resourceid):
        dao = HeavyEquipmentDAO()
        row = dao.getHeavyEqByResourceID(resourceid)
        if not row:
            return jsonify(Error="HeavyEquipment Not Found "), 404
        else:
            HeavyEquipment = self.build_heavydetails_dict(row)
            return jsonify(HeavyEquipment=HeavyEquipment)

    def getResourceIDByHeavyEquipmentID(self, HeavyEquipmentid):
        dao = HeavyEquipmentDAO()
        row = dao.getResourceIDByHeavyEqID(HeavyEquipmentid)
        if not row:
            return jsonify(Error="HeavyEquipment Not Found "), 404
        else:
            HeavyEquipment = self.build_heavyequipment_dict(row)
            return jsonify(HeavyEquipment=HeavyEquipment)

    def searchHeavyEquipment(self, args):
        supplierid = args.get("supplierid")
        dao = HeavyEquipmentDAO()
        HeavyEquipment_list = []
        if (len(args) == 1) and supplierid:
            HeavyEquipment_list = dao.getHeavyEquipmentBySupplier(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in HeavyEquipment_list:
            result = self.build_heavyequipment_dict(row)
            result_list.append(result)
        return jsonify(HeavyEquipment=result_list)

    def insertHeavyEquipment(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error="Malformed post request")
        HeavyEquipmentbrand = form['HeavyEquipmentBrand']
        HeavyEquipmentdescription = form['HeavyEquipmentDescription']
        resourceid = form['ResourceID']
        if HeavyEquipmentbrand and HeavyEquipmentdescription and resourceid:
            dao = HeavyEquipmentDAO()
            HeavyEquipmentid = dao.insert(HeavyEquipmentbrand, HeavyEquipmentdescription, resourceid,)
            result = self.build_heavyequipment_attributes(HeavyEquipmentid, HeavyEquipmentbrand, HeavyEquipmentdescription, resourceid, )
            return jsonify(HeavyEquipment=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertHeavyEquipmentJson(self, json):
        HeavyEquipmentbrand = json['HeavyEqBrand']
        HeavyEquipmentdescription = json['HeavyEqDescription']
        resourceid = json['ResourceID']
        if HeavyEquipmentbrand and HeavyEquipmentdescription and resourceid:
            dao = HeavyEquipmentDAO()
            HeavyEquipmentid = dao.insert(HeavyEquipmentbrand, HeavyEquipmentdescription, resourceid)
            result = self.build_heavyequipment_attributes(HeavyEquipmentid, HeavyEquipmentbrand, HeavyEquipmentdescription, resourceid)
            return jsonify(HeavyEquipment=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteHeavyEquipment(self, HeavyEquipmentid):
        dao = HeavyEquipmentDAO()
        if not dao.getHeavyEquipmentById(HeavyEquipmentid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(HeavyEquipmentid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, HeavyEquipmentid, form):
        dao = HeavyEquipmentDAO()
        if not dao.getHeavyEquipmentById(HeavyEquipmentid):
            return jsonify(Error="HeavyEquipment not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request")
            else:
                HeavyEquipmentbrand = form['HeavyEquipmentbrand']
                HeavyEquipmentdescription = form['HeavyEquipmentdescription']
                if  HeavyEquipmentbrand and HeavyEquipmentdescription:
                    dao.update(HeavyEquipmentid, HeavyEquipmentbrand, HeavyEquipmentdescription)
                    resourceid = dao.getResourceIDByHeavyEqID(HeavyEquipmentid)
                    result = self.build_heavyequipment_attributes(HeavyEquipmentid, HeavyEquipmentbrand, HeavyEquipmentdescription, resourceid)
                    return jsonify(HeavyEquipment=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, HeavyEquipmentid, json):
        dao = HeavyEquipmentDAO()
        if not dao.getHeavyEquipmentById(HeavyEquipmentid):
            return jsonify(Error="HeavyEquipment not found."), 404
        else:
            HeavyEquipmentbrand = json['HeavyEquipmentbrand']
            HeavyEquipmentdescription = json['HeavyEquipmentdescription']
            if HeavyEquipmentbrand and HeavyEquipmentdescription:
                dao.update(HeavyEquipmentid, HeavyEquipmentbrand, HeavyEquipmentdescription)
                resourceid = dao.getResourceIDByHeavyEqID(HeavyEquipmentid)
                result = self.build_heavyequipment_attributes(HeavyEquipmentid, HeavyEquipmentbrand,
                                                              HeavyEquipmentdescription, resourceid)
                return jsonify(HeavyEquipment=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400







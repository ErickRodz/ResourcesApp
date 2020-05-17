from flask import jsonify
from dao.batteries import BatteriesDAO


class BatteriesHandler:
    def build_batteries_dict(self, row):
        result = {}
        result['BatteryID'] = row[0]
        result['BatteryBrand'] = row[1]
        result['BatteryType'] = row[2]
        result['BatteryDescription'] = row[3]
        result['ResourceID'] = row[4]
        return result

    def build_batteries_attributes(self, batteryid, batterybrand, batterytype, batterydescription, resourceid,):
        result = {}
        result['BatteryID'] = batteryid
        result['BatteryBrand'] = batterybrand
        result['BatteryType'] = batterytype
        result['BatteryDescription'] = batterydescription
        result['ResourceID'] = resourceid
        return result

    def build_batteriesdetails_dict(self, row):
        result = {}
        result['ResourceID'] = row[0]
        result['ResourceName'] = row[1]
        result['ResourcePrice'] = row[2]
        result['ResourceQuantity'] = row[3]
        result['SupplierID'] = row[4]
        result['BatteryID'] = row[5]
        result['BatteryBrand'] = row[6]
        result['BatteryType'] = row[7]
        result['BatteryDescription'] = row[8]
        return result

    def getAllBatteries(self):
        dao = BatteriesDAO()
        batteries_list = dao.getAllBatteries()
        result_list = []
        for row in batteries_list:
            result = self.build_batteries_dict(row)
            result_list.append(result)

        return jsonify(Batteries=batteries_list)

    def getBatteriesByID(self, batteryid):
        dao = BatteriesDAO()
        row = dao.getBatteriesById(batteryid)
        if not row:
            return jsonify(Error="Battery Not Found "), 404
        else:
            battery = self.build_batteries_dict(row)
            return jsonify(Battery=battery)

    def searchBatteries(self, args):
        supplierid = args.get("supplierid")
        dao = BatteriesDAO()
        batteries_list = []
        if (len(args) == 1) and supplierid:
            batteries_list = dao.getBatteriesBySupplier(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in batteries_list:
            result = self.build_batteries_dict(row)
            result_list.append(result)
        return jsonify(Batteries=result_list)
    
    def getBatteriesByResourceID(self, resourceid):
        dao = BatteriesDAO()
        row = dao.getBatteryByResourceID(resourceid)
        if not row:
            return jsonify(Error="Battery Not Found "), 404
        else:
            Battery = self.build_batteriesdetails_dict(row)
            return jsonify(Battery=Battery)

    def getResourceIDByBatteryID(self, Batteryid):
        dao = BatteriesDAO()
        row = dao.getResourceIDByBatteryID(Batteryid)
        if not row:
            return jsonify(Error="Battery Not Found "), 404
        else:
            Battery = self.build_batteries_dict(row)
            return jsonify(Battery=Battery)

    def insertBattery(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request")
        batterybrand = form['batterybrand']
        batterytype = form['batterytype']
        batterydescription = form['batterydescription']
        resourceid = form['resourceid']
        if batterybrand and batterytype and batterydescription and resourceid:
            dao = BatteriesDAO()
            batteryid = dao.insert(batterybrand, batterytype, batterydescription, resourceid,)
            result = self.build_batteries_attributes(batteryid, batterybrand, batterytype, batterydescription, resourceid, )
            return jsonify(Battery=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertBatteryJson(self, json):
        batterybrand = json['BatteryBrand']
        batterytype = json['BatteryType']
        batterydescription = json['BatteryDescription']
        resourceid = json['ResourceID']
        if batterybrand and batterytype and batterydescription and resourceid:
            dao = BatteriesDAO()
            batteryid = dao.insert(batterybrand, batterytype, batterydescription, resourceid)
            result = self.build_batteries_attributes(batteryid, batterybrand, batterytype, batterydescription, resourceid)
            return jsonify(Battery=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteBattery(self, batteryid):
        dao = BatteriesDAO()
        if not dao.getBatteriesById(batteryid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(batteryid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, batteryid, form):
        dao = BatteriesDAO()
        if not dao.getBatteriesById(batteryid):
            return jsonify(Error="Battery not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request")
            else:
                batterybrand = form['batterybrand']
                batterytype = form['batterytype']
                batterydescription = form['batterydescription']
                if  batterybrand and batterytype and batterydescription:
                    dao.update(batteryid, batterybrand, batterytype, batterydescription)
                    resourceid = dao.getResourceIDByBatteryID(batteryid)
                    result = self.build_batteries_attributes(batteryid, batterybrand,batterytype, batterydescription, resourceid)
                    return jsonify(Battery=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, batteryid, json):
        dao = BatteriesDAO()
        if not dao.getBatteriesById(batteryid):
            return jsonify(Error="Battery not found."), 404
        else:
            batterybrand = json['batterybrand']
            batterytype = json['batterytype']
            batterydescription = json['batterydescription']
            if batterybrand and batterytype and batterydescription:
                dao.update(batteryid, batterybrand, batterytype, batterydescription)
                resourceid = dao.getResourceIDByBatteryID(batteryid)
                result = self.build_batteries_attributes(batteryid, resourceid, batterybrand, batterytype, batterydescription)
                return jsonify(Battery=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400







from flask import jsonify
from dao.fuel import FuelDAO


class FuelHandler:
    def build_fuel_dict(self, row):
        result = {}
        result['FuelID'] = row[0]
        result['FuelType'] = row[1]
        result['FuelOctenage'] = row[2]
        result['FuelDescription'] = row[3]
        result['ResourceID'] = row[4]
        return result

    def build_fuel_attributes(self, Fuelid, Fueltype, Fueloctenage, Fueldescription,  resourceid,):
        result = {}
        result['FuelID'] = Fuelid
        result['Fueltype'] = Fueltype
        result['FuelOctenage'] = Fueloctenage
        result['FuelDescription'] = Fueldescription
        result['ResourceID'] = resourceid
        return result

    def build_fueldetails_dict(self, row):
        result = {}
        result['ResourceID'] = row[0]
        result['ResourceName'] = row[1]
        result['ResourcePrice'] = row[2]
        result['ResourceQuantity'] = row[3]
        result['SupplierID'] = row[4]
        result['FuelID'] = row[5]
        result['FuelType'] = row[6]
        result['FuelOctenage'] = row[7]
        result['FuelDescription'] = row[8]
        return result

    def getAllFuel(self):
        dao = FuelDAO()
        Fuel_list = dao.getAllFuel()
        result_list = []
        for row in Fuel_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)

        return jsonify(Fuel=Fuel_list)

    def getFuelByID(self, Fuelid):
        dao = FuelDAO()
        row = dao.getFuelById(Fuelid)
        if not row:
            return jsonify(Error="Fuel Not Found "), 404
        else:
            Fuel = self.build_fuel_dict(row)
            return jsonify(Fuel=Fuel)

    def getFuelByResourceID(self, resourceid):
        dao = FuelDAO()
        row = dao.getFuelByResourceID(resourceid)
        if not row:
            return jsonify(Error="Fuel Not Found "), 404
        else:
            Fuel = self.build_fueldetails_dict(row)
            return jsonify(Fuel=Fuel)

    def getResourceIDByFuelID(self, Fuelid):
        dao = FuelDAO()
        row = dao.getResourceIDByFuelID(Fuelid)
        if not row:
            return jsonify(Error="Fuel Not Found "), 404
        else:
            Fuel = self.build_fuel_dict(row)
            return jsonify(Fuel=Fuel)


    def searchFuel(self, args):
        supplierid = args.get("supplierid")
        dao = FuelDAO()
        Fuel_list = []
        if (len(args) == 1) and supplierid:
            Fuel_list = dao.getFuelBySupplier(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in Fuel_list:
            result = self.build_fuel_dict(row)
            result_list.append(result)
        return jsonify(Fuel=result_list)

    def insertFuel(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request")
        Fueltype = form['FuelType']
        Fueloctenage = form['FuelOctenage']
        Fueldescription = form['Fueldescription']
        resourceid = form['resourceid']
        if Fueltype and Fueloctenage and Fueldescription and resourceid:
            dao = FuelDAO()
            Fuelid = dao.insert(Fueltype, Fueloctenage, Fueldescription, resourceid,)
            result = self.build_fuel_attributes(Fuelid, Fueltype, Fueloctenage, Fueldescription, resourceid, )
            return jsonify(Fuel=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertFuelJson(self, json):
        Fueltype = json['FuelType']
        Fueloctenage = json['FuelOctenage']
        Fueldescription = json['FuelDescription']
        resourceid = json['ResourceID']
        if Fueltype and Fueloctenage and Fueldescription and resourceid:
            dao = FuelDAO()
            Fuelid = dao.insert(Fueltype, Fueloctenage, Fueldescription, resourceid)
            result = self.build_fuel_attributes(Fuelid, Fueltype, Fueloctenage, Fueldescription, resourceid)
            return jsonify(Fuel=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteFuel(self, Fuelid):
        dao = FuelDAO()
        if not dao.getFuelById(Fuelid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(Fuelid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, Fuelid, form):
        dao = FuelDAO()
        if not dao.getFuelById(Fuelid):
            return jsonify(Error="Fuel not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request")
            else:
                Fueltype = form['FuelType']
                Fueloctenage = form['FuelOctenage']
                Fueldescription = form['FuelDescription']
                if Fueltype and Fueloctenage and Fueldescription:
                    dao.update(Fuelid, Fueltype, Fueloctenage, Fueldescription)
                    resourceid = dao.getResourceIDByFuelID(Fuelid)
                    result = self.build_fuel_attributes(Fuelid, Fueltype, Fueloctenage, Fueldescription, resourceid)
                    return jsonify(Fuel=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, Fuelid, json):
        dao = FuelDAO()
        if not dao.getFuelById(Fuelid):
            return jsonify(Error="Fuel not found."), 404
        else:
            Fueltype = json['FuelType']
            Fueloctenage = json['FuelOctenage']
            Fueldescription = json['FuelDescription']
            if Fueltype and Fueloctenage and Fueldescription:
                dao.update(Fuelid, Fueltype, Fueloctenage, Fueldescription)
                resourceid = dao.getResourceIDByFuelID(Fuelid)
                result = self.build_fuel_attributes(Fuelid, Fueltype, Fueloctenage, Fueldescription, resourceid)
                return jsonify(Fuel=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400







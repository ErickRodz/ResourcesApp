from flask import jsonify
from dao.fuel import FuelDAO


class ResourceHandler:
    def build_fuel_dict(self, row):
        result = {}
        result['Fuelid'] = row[0]
        result['Fueltype'] = row[1]
        result['Fueloctenage'] = row[2]
        result['Fueldescription'] = row[3]
        result['resourceid'] = row[4]
        return result

    def build_fuel_attributes(self, Fuelid, Fueltype, Fueloctenage, Fueldescription,  resourceid,):
        result = {}
        result['FuelID'] = Fuelid
        result['Fueltype'] = Fueltype
        result['FuelOctenage'] = Fueloctenage
        result['FuelDescription'] = Fueldescription
        result['ResourceID'] = resourceid
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
        Fueldescription = json['Fueldescription']
        resourceid = json['resourceid']
        if Fueltype and Fueloctenage and Fueldescription and resourceid:
            dao = FuelDAO()
            Fuelid = dao.insert(Fueltype, Fueloctenage, Fueldescription, resourceid, )
            result = self.build_fuel_attributes(Fuelid, Fueltype, Fueloctenage, Fueldescription, resourceid, )
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







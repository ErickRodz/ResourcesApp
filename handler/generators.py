from flask import jsonify
from dao.generators import GeneratorsDAO


class GeneratorsHandler:
    def build_generators_dict(self, row):
        result = {}
        result['GeneratorID'] = row[0]
        result['GeneratorBrand'] = row[1]
        result['GeneratorType'] = row[2]
        result['GeneratorDescription'] = row[3]
        result['ResourceID'] = row[4]
        return result

    def build_generators_attributes(self, GeneratorID, GeneratorBrand, GeneratorType, GeneratorDescription, ResourceID):
        result = {}
        result['GeneratorID'] = GeneratorID
        result['GeneratorBrand'] = GeneratorBrand
        result['GeneratorType'] = GeneratorType
        result['GeneratorDescription'] = GeneratorDescription
        result['ResourceID'] = ResourceID
        return result

    def build_generatorsdetails_dict(self, row):
        result = {}
        result['ResourceID'] = row[0]
        result['ResourceName'] = row[1]
        result['ResourcePrice'] = row[2]
        result['ResourceQuantity'] = row[3]
        result['SupplierID'] = row[4]
        result['GeneratorID'] = row[5]
        result['GeneratorBrand'] = row[6]
        result['GeneratorType'] = row[7]
        result['GeneratorDescription'] = row[8]
        return result

    def getAllGenerators(self):
        dao = GeneratorsDAO()
        generators_list = dao.getAllGenerators()
        result_list = []
        for row in generators_list:
            result = self.build_generators_dict(row)
            result_list.append(result)
        return jsonify(Generators=generators_list)

    def getGeneratorsByID(self, generatorid):
        dao = GeneratorsDAO()
        row = dao.getGeneratorsById(generatorid)
        if not row:
            return jsonify(Error="Generator Not Found "), 404
        else:
            generator = self.build_generators_dict(row)
            return jsonify(Generator=generator)

    def getGeneratorsByResourceID(self, resourceid):
        dao = GeneratorsDAO()
        row = dao.getGeneratorByResourceID(resourceid)
        if not row:
            return jsonify(Error="Generators Not Found "), 404
        else:
            Generators = self.build_generatorsdetails_dict(row)
            return jsonify(Generators=Generators)

    def getResourceIDByGeneratorsID(self, Generatorsid):
        dao = GeneratorsDAO()
        row = dao.getResourceIDByGeneratorID(Generatorsid)
        if not row:
            return jsonify(Error="Generators Not Found "), 404
        else:
            Generators = self.build_generators_dict(row)
            return jsonify(Generators=Generators)

    def searchGenerators(self, args):
        supplierid = args.get("SupplierID")
        generatortype = args.get("GeneratorType")
        dao = GeneratorsDAO()
        generators_list = []
        if (len(args) == 1) and supplierid:
            generators_list = dao.getGeneratorsBySupplier(supplierid)
        elif (len(args) == 1) and generatortype:
            generators_list= dao.getGeneratorsByType(generatortype)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in generators_list:
            result = self.build_generators_dict(row)
            result_list.append(result)
        return jsonify(Generators=result_list)

    def insertGenerators(self, form):
        print("form: ", form)
        if len(form) != 4 :
            return jsonify(Error="Malformed post request")
        generatorbrand = form['generatorbrand']
        generatortype = form['generatortype']
        generatordescription = form['generatordescription']
        resourceid = form['resourceid']
        if generatorbrand and generatortype and generatordescription and resourceid:
            dao = GeneratorsDAO()
            generatorid = dao.insert(generatorbrand, generatortype, generatordescription, resourceid)
            result = self.build_generators_attributes(generatorid, generatorbrand, generatortype, generatordescription, resourceid,)
            return jsonify(Generators=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertGeneratorJson(self, json):
        generatorbrand = json['GeneratorBrand']
        generatortype = json['GeneratorType']
        generatordescription = json['GeneratorDescription']
        resourceid = json['ResourceID']
        if generatorbrand and generatortype and generatordescription and resourceid:
            dao = GeneratorsDAO()
            generatorid = dao.insert(generatorbrand, generatortype, generatordescription, resourceid)
            result = self.build_generators_attributes(generatorid, generatorbrand, generatortype, generatordescription, resourceid)
            return jsonify(Generator=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteGenerator(self, Generatorid):
        dao = GeneratorsDAO()
        if not dao.getGeneratorsById(Generatorid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(Generatorid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, Generatorid, form):
        dao = GeneratorsDAO()
        if not dao.getBatteriesById(Generatorid):
            return jsonify(Error="Generator not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request")
            else:
                generatorbrand = form['generatorbrand']
                generatortype = form['generatortype']
                generatordescription = form['generatordescription']
                resourceid = form['resourceid']
                if generatorbrand and generatortype and generatordescription and resourceid:
                    dao.update(Generatorid, generatorbrand, generatortype, generatordescription, resourceid)
                    resourceid = dao.getResourceIDByGeneratorID(Generatorid)
                    result = self.build_generators_attributes(Generatorid, generatorbrand, generatortype, generatordescription, resourceid)
                    return jsonify(Generator=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, Generatorid, json):
        dao = GeneratorsDAO()
        if not dao.getGeneratorsById(Generatorid):
            return jsonify(Error="Generator not found."), 404

        else:
            generatorbrand = json['generatorbrand']
            generatortype = json['generatortype']
            generatordescription = json['generatordescription']
            resourceid = json['resourceid']
            if generatorbrand and generatortype and generatordescription and resourceid:
                dao.update(Generatorid, generatorbrand, generatortype, generatordescription, resourceid)
                resourceid = dao.getResourceIDByGeneratorID(Generatorid)
                result = self.build_generators_attributes(Generatorid, generatorbrand, generatortype, generatordescription, resourceid)
                return jsonify(Generator=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400







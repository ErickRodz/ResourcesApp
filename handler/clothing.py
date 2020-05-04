from flask import jsonify
from dao.clothing import ClothingDAO


class ResourceHandler:
    def build_clothing_dict(self, row):
        result = {}
        result['Clothingid'] = row[0]
        result['Clothingbrand'] = row[1]
        result['ClothingSize'] = row[2]
        result['ClothingFabric'] = row[3]
        result['Clothingdescription'] = row[4]
        result['resourceid'] = row[5]
        return result

    def build_clothing_attributes(self, Clothingid, Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, resourceid,):
        result = {}
        result['ClothingID'] = Clothingid
        result['ClothingBrand'] = Clothingbrand
        result['ClothingSize'] = Clothingsize
        result['ClothingFabric'] = Clothingfabric
        result['ClothingDescription'] = Clothingdescription
        result['ResourceID'] = resourceid
        return result

    def getAllClothing(self):
        dao = ClothingDAO()
        Clothing_list = dao.getAllClothing()
        result_list = []
        for row in Clothing_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)

        return jsonify(Clothing=Clothing_list)

    def getClothingByID(self, Clothingid):
        dao = ClothingDAO()
        row = dao.getClothingById(Clothingid)
        if not row:
            return jsonify(Error="Clothing Not Found "), 404
        else:
            Clothing = self.build_clothing_dict(row)
            return jsonify(Clothing=Clothing)

    def searchClothing(self, args):
        supplierid = args.get("supplierid")
        dao = ClothingDAO()
        Clothing_list = []
        if (len(args) == 1) and supplierid:
            Clothing_list = dao.getClothingBySupplier(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in Clothing_list:
            result = self.build_clothing_dict(row)
            result_list.append(result)
        return jsonify(Clothing=result_list)

    def insertClothing(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request")
        Clothingbrand = form['ClothingBrand']
        Clothingsize = form['ClothingSize']
        Clothingfabric = form["ClothingFabric"]
        Clothingdescription = form['ClothingDescription']
        resourceid = form['resourceid']
        if Clothingbrand and Clothingsize and Clothingfabric and Clothingdescription and resourceid:
            dao = ClothingDAO()
            Clothingid = dao.insert(Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, resourceid,)
            result = self.build_clothing_attributes(Clothingid, Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, resourceid,)
            return jsonify(Clothing=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertClothingJson(self, json):
        Clothingbrand = json['ClothingBrand']
        Clothingsize = json['ClothingSize']
        Clothingfabric = json["ClothingFabric"]
        Clothingdescription = json['ClothingDescription']
        resourceid = json['resourceid']
        if Clothingbrand and Clothingsize and Clothingfabric and Clothingdescription and resourceid:
            dao = ClothingDAO()
            Clothingid = dao.insert(Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, resourceid, )
            result = self.build_clothing_attributes(Clothingid, Clothingbrand, Clothingsize, Clothingfabric,
                                                    Clothingdescription, resourceid, )
            return jsonify(Clothing=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")


    def deleteClothing(self, Clothingid):
        dao = ClothingDAO()
        if not dao.getClothingById(Clothingid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(Clothingid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, Clothingid, form):
        dao = ClothingDAO()
        if not dao.getClothingById(Clothingid):
            return jsonify(Error="Clothing not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request")
            else:
                Clothingbrand = form['ClothingBrand']
                Clothingsize = form['ClothingSize']
                Clothingfabric = form["ClothingFabric"]
                Clothingdescription = form['ClothingDescription']
                resourceid = form['resourceid']
                if Clothingbrand and Clothingsize and Clothingfabric and Clothingdescription and resourceid:
                    dao.update(Clothingid, Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription)
                    resourceid = dao.getResourceIDByClothingID(Clothingid)
                    result = self.build_clothing_attributes(Clothingid, Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription, resourceid)
                    return jsonify(Clothing=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, Clothingid, json):
        dao = ClothingDAO()
        if not dao.getClothingById(Clothingid):
            return jsonify(Error="Clothing not found."), 404
        else:
            Clothingbrand = json['ClothingBrand']
            Clothingsize = json['ClothingSize']
            Clothingfabric = json["ClothingFabric"]
            Clothingdescription = json['ClothingDescription']
            resourceid = json['resourceid']
            if Clothingbrand and Clothingsize and Clothingfabric and Clothingdescription and resourceid:
                dao.update(Clothingid, Clothingbrand, Clothingsize, Clothingfabric, Clothingdescription)
                resourceid = dao.getResourceIDByClothingID(Clothingid)
                result = self.build_clothing_attributes(Clothingid, Clothingbrand, Clothingsize, Clothingfabric,
                                                        Clothingdescription, resourceid)
                return jsonify(Clothing=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400







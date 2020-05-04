from flask import jsonify
from dao.parts import PartsDAO


class ResourceHandler:
    def build_parts_dict(self, row):
        result = {}
        result['PartsID'] = row[0]
        result['PartsMaterial'] = row[1]
        result['PartsColor'] = row[2]
        result['PartsDescription'] = row[3]
        result['ResourceID'] = row[4]
        return result

    def build_parts_attributes(self, PartsID, PartsMaterial, PartsColor, PartsDescription, resourceid):
        result = {}
        result['PartsID'] = PartsID
        result['PartsMaterial'] = PartsMaterial
        result['PartsColor'] = PartsColor
        result['PartsDescription'] = PartsDescription
        result['resourceid'] = resourceid
        return result

    def getAllParts(self):
        dao = PartsDAO()
        Parts_list = dao.getAllParts()
        result_list = []
        for row in Parts_list:
            result = self.build_parts_dict(row)
            result_list.append(result)
        return jsonify(Parts=Parts_list)

    def getPartsByID(self, Partsid):
        dao = PartsDAO()
        row = dao.getPartsById(Partsid)
        if not row:
            return jsonify(Error="Parts Not Found "), 404
        else:
            Parts = self.build_parts_dict(row)
            return jsonify(Parts=Parts)

    def searchParts(self, args):
        supplierid = args.get("supplierid")
        dao = PartsDAO()
        Parts_list = []
        if (len(args) == 1) and supplierid:
            Parts_list = dao.getPartsBySupplier(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in Parts_list:
            result = self.build_parts_dict(row)
            result_list.append(result)
        return jsonify(Parts=result_list)

    def insertParts(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request")
        Partsmaterial = form['PartsMaterial']
        Partscolor = form['PartsColor']
        Partsdescription = form['PartsDescription']
        resourceid = form['ResourceID']
        if Partsmaterial and Partscolor and Partsdescription and resourceid:
            dao = PartsDAO()
            Partsid = dao.insert(Partsmaterial, Partscolor, Partsdescription, resourceid,)
            result = self.build_parts_attributes(Partsmaterial, Partscolor, Partsdescription, resourceid,)
            return jsonify(Parts=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertPartsJson(self, json):
        Partsmaterial = json['PartsMaterial']
        Partscolor = json['PartsColor']
        Partsdescription = json['PartsDescription']
        resourceid = json['ResourceID']
        if Partsmaterial and Partscolor and Partsdescription and resourceid:
            dao = PartsDAO()
            Partsid = dao.insert(Partsmaterial, Partscolor, Partsdescription, resourceid, )
            result = self.build_parts_attributes(Partsmaterial, Partscolor, Partsdescription, resourceid, )
            return jsonify(Parts=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteParts(self, Partsid):
        dao = PartsDAO()
        if not dao.getPartsById(Partsid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(Partsid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, Partsid, form):
        dao = PartsDAO()
        if not dao.getPartsById(Partsid):
            return jsonify(Error="Parts not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request")
            else:
                Partsmaterial = form['PartsMaterial']
                Partscolor = form['PartsColor']
                Partsdescription = form['PartsDescription']
                if  Partsmaterial and Partscolor and Partsdescription:
                    dao.update(Partsid, Partsmaterial, Partscolor, Partsdescription)
                    resourceid = dao.getResourceIDByPartsID(Partsid)
                    result = self.build_parts_attributes(Partsid, Partsmaterial, Partscolor, Partsdescription, resourceid)
                    return jsonify(Parts=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400


    def updateResourceJson(self, Partsid, json):
        dao = PartsDAO()
        if not dao.getPartsById(Partsid):
            return jsonify(Error="Parts not found."), 404
        else:
            Partsmaterial = json['PartsMaterial']
            Partscolor = json['PartsColor']
            Partsdescription = json['PartsDescription']
            if Partsmaterial and Partscolor and Partsdescription:
                dao.update(Partsid, Partsmaterial, Partscolor, Partsdescription)
                resourceid = dao.getResourceIDByPartsID(Partsid)
                result = self.build_parts_attributes(Partsid, Partsmaterial, Partscolor, Partsdescription, resourceid)
                return jsonify(Parts=result), 400
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400








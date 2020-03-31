from flask import jsonify
from dao.attributes import AttributesDAO


class AttributeHandler:
    def build_attribute_dict(self, row):
        result = {}
        result['attributeid'] = row[0]
        result['resourceid'] = row[1]
        result['attributename'] = row[2]
        result['attributequantity'] = row[3]
        return result

    def build_attribute_attributes(self, attributeid, resourceid, attributename, attributequantity):
        result = {}
        result['attributeid'] = attributeid
        result['resourceid'] = resourceid
        result['attributeename'] = attributename
        result['attributequantity'] = attributequantity
        return result

    def getAllResources(self):
        dao = AttributesDAO()
        attributes_list = dao.getAllAttributes()
        result_list = []
        for row in attributes_list:
            result = self.build_attribute_dict(row)
            result_list.append(result)
        return jsonify(Attributes=result_list)

    def getAttributeByID(self, attributeid):
        dao = AttributesDAO
        row = dao.getAttributeById(attributeid)
        if not row:
            return jsonify(Error="Attribute Not Found "), 404
        else:
            attribute = self.build_attribute_dict(row)
            return jsonify(Attribute=attribute)

    def getAttributeByResourceID(self, resourceid):
        dao = AttributesDAO
        row = dao.getAttributeByResourceId(resourceid)
        if not row:
            return jsonify(Error="Attribute Not Found "), 404
        else:
            attribute = self.build_attribute_dict(row)
            return jsonify(Attribute=attribute)

    def searchAttributes(self, args):
        attributename = args.get("attributename")
        resourceid = args.get("resourceid")
        dao = AttributesDAO()
        resources_list = []
        if (len(args) == 2) and attributename and resourceid:
            resources_list = dao.getAttributebyAttributeNameAndResourceId(attributename, resourceid)
        elif (len(args) == 1) and attributename:
            resources_list = dao.getAttributebyAttributeName(attributename)
        elif (len(args) == 1) and resourceid:
            resources_list = dao.getAttributeByResourceId(resourceid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in resources_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Attributes=result_list)

    def insertAttribute(self, form):
        print("form: ", form)
        if len(form) != 3:
            return jsonify(Error="Malformed post request")
        resourceid = form['resourceid']
        attributename = form['attributename']
        attributequantity = form['attributequantity']
        if attributename and attributequantity and resourceid:
            dao = AttributesDAO()
            attributeid = dao.insert(resourceid, attributename, attributequantity)
            # resourceid = dao.getSupplierByResourceID(resourceid) #duda
            result = self.build_resource_attributes(attributeid, resourceid, attributename,
                                                    attributequantity)
            return jsonify(Attribute=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertAttributeJson(self, json):
        resourceid = json['resourceid']
        attributename = json['attributename']
        attributequantity = json['attributequantity']
        if  attributequantity and attributename and resourceid:
            dao = AttributesDAO()
            attributeid = dao.insert(resourceid, attributename, attributequantity)
            # resourceid = dao.getSupplierByResourceID(resourceid) #duda
            result = self.build_attribute_attributes(attributeid, resourceid, attributename,
                                                    attributequantity)
            return jsonify(Attribute=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteAttribute(self, attributeid):
        dao = AttributesDAO()
        if not dao.getAttributeById(attributeid):
            return jsonify(Error="Attribute not found."), 404
        else:
            dao.delete(attributeid)
            return jsonify(DeleteStatus="OK"), 200

    def updateAttribute(self, attributeid, form):
        dao = AttributesDAO()
        if not dao.getAttributeById(attributeid):
            return jsonify(Error="Attribute not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request")
            else:
                resourceid = form['resourceid']
                attributename = form['attributename']
                attributequantity = form['attributequantity']
                if resourceid and attributename and attributequantity:
                    dao.update(resourceid, resourceid, attributename, attributequantity)
                    result = self.build_resource_attributes(attributeid, resourceid, attributename,
                                                            attributequantity)
                    return jsonify(Resource=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400







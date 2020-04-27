from flask import jsonify
from dao.resources import ResourcesDAO


class ResourceHandler:
    def build_resource_dict(self, row):
        result = {}
        result['resourceid'] = row[0]
        result['supplierid'] = row[1]
        result['resourcename'] = row[2]
        result['resourceprice'] = row[3]
        result['resourcequantity'] = row[4]
        return result

    def build_resource_attributes(self, resourceid, supplierid, resourcename, resourceprice, resourcequantity):
        result = {}
        result['resourceid'] = resourceid
        result['supplierid'] = supplierid
        result['resourcename'] = resourcename
        result['resourceprice'] = resourceprice
        result['resourcequantity'] = resourcequantity
        return result

    def getAllResources(self):
        dao = ResourcesDAO()
        resources_list = dao.getAllResources()
        result_list = []
        for row in resources_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resources=result_list)

    def getResourceByID(self, resourceid):
        dao = ResourcesDAO
        row = dao.getResourceById(resourceid)
        if not row:
            return jsonify(Error="Resource Not Found "), 404
        else:
            resource = self.build_resource_dict(row)
            return jsonify(Resource=resource)

    def searchResources(self, args):
        resourcename = args.get("resourcename")
        supplierid = args.get("supplierid")
        attributename = args.get("attributename")
        dao = ResourcesDAO()
        resources_list = []
        if (len(args) == 2) and resourcename and supplierid:
            resources_list = dao.getResourcesByNameAndSupplier(resourcename, supplierid)
        elif (len(args) == 1) and resourcename:
            resources_list = dao.getResourcesByName(resourcename)
        elif (len(args) == 1) and supplierid:
            resources_list = dao.getResourcesBySupplier(supplierid)
        elif (len(args) == 1) and attributename:
            resources_list= dao.getResourcesByAttributeName(attributename)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in resources_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resources=result_list)

    def insertResource(self, form):
        print("form: ", form)
        if len(form) != 4:
            return jsonify(Error="Malformed post request")
        supplierid = form['supplierid']
        resourcename = form['resourcename']
        resourceprice = form['resourceprice']
        resourcequantity = form['resourcequantity']
        if resourcename and resourceprice and resourcequantity and supplierid:
            dao = ResourcesDAO()
            resourceid = dao.insert(supplierid, resourcename, resourceprice, resourcequantity)
            # supplierid = dao.getSupplierByResourceID(resourceid) #duda
            result = self.build_resource_attributes(resourceid, supplierid, resourcename, resourceprice,
                                                    resourcequantity)
            return jsonify(Resource=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertResourceJson(self, json):
        supplierid = json['supplierid']
        resourcename = json['resourcename']
        resourceprice = json['resourceprice']
        resourcequantity = json['resourcequantity']
        if resourceprice and resourcequantity and resourcename and supplierid:
            dao = ResourcesDAO()
            resourceid = dao.insert(supplierid, resourcename, resourceprice, resourcequantity)
            # supplierid = dao.getSupplierByResourceID(resourceid) #duda
            result = self.build_resource_attributes(resourceid, supplierid, resourcename, resourceprice,
                                                    resourcequantity)
            return jsonify(Resources=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteResource(self, resourceid):
        dao = ResourcesDAO()
        if not dao.getResourceById(resourceid):
            return jsonify(Error="Resource not found."), 404
        else:
            dao.delete(resourceid)
            return jsonify(DeleteStatus="OK"), 200

    def updateResource(self, resourceid, form):
        dao = ResourcesDAO()
        if not dao.getResourceById(resourceid):
            return jsonify(Error="Resource not found."), 404
        else:
            if len(form) != 4:
                return jsonify(Error="Malformed update request")
            else:
                supplierid = form['supplierid']
                resourcename = form['resourcename']
                resourceprice = form['resourceprice']
                resourcequantity = form['resourcequantity']
                if supplierid and resourcename and resourceprice and resourcequantity:
                    dao.update(resourceid, supplierid, resourcename, resourceprice, resourcequantity)
                    result = self.build_resource_attributes(resourceid, supplierid, resourcename, resourceprice,
                                                            resourcequantity)
                    return jsonify(Resource=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400







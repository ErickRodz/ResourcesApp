from flask import jsonify
from dao.resources import ResourcesDAO


class ResourceHandler:
    def build_resource_dict(self, row):
        result = {}
        result['ResourceID'] = row[0]
        result['ResourceName'] = row[1]
        result['ResourcePrice'] = row[2]
        result['ResourceQuantity'] = row[3]
        result['SupplierID'] = row[4]
        return result

    def build_resource_attributes(self, resourceid, resourcename, resourceprice, resourcequantity, supplierid):
        result = {}
        result['ResourceID'] = resourceid
        result['ResourceName'] = resourcename
        result['ResourcePrice'] = resourceprice
        result['ResourceQuantity'] = resourcequantity
        result['SupplierID'] = supplierid
        return result

    def build_resourcecatname_dict(self, row):
        result = {}
        result['ResourceID'] = row[0]
        result['SupplierID'] = row[1]
        result['ResourceName'] = row[2]
        result['ResourcePrice'] = row[3]
        result['ResourceQuantity'] = row[4]
        result['CategoryID'] = row[5]
        result['CategoryName'] = row[6]
        return result

    def getAllResources(self):
        dao = ResourcesDAO()
        resources_list = dao.getAllResources()
        result_list = []
        # resources_list = [0,0,'papel de toilet', 5, 10]
        for row in resources_list:
            result = self.build_resource_dict(row)
            result_list.append(result)

        return jsonify(Resources=result_list)

    def getAllResourcesAvailableOrderByResourceName(self):
        dao = ResourcesDAO()
        resources_list = dao.getResourcesAvailableOrderByResourceName()
        result_list = []
        for row in resources_list:
            result = self.build_resource_dict(row)
            result_list.append(result)

        return jsonify(Resources=result_list)

    def getAllResourcesAvailable(self):
        dao = ResourcesDAO()
        resources_list = dao.getResourcesAvailable()
        result_list = []
        for row in resources_list:
            result = self.build_resource_dict(row)
            result_list.append(result)

        return jsonify(Resources=result_list)

    def getResourceAvailabilityById(self, resourceid):
        dao = ResourcesDAO()
        row = dao.getResourceAvailabilityById(resourceid)
        if not row:
            return jsonify(Error="Resource Not Found "), 404
        else:
            resource = self.build_resource_dict(row)
            return jsonify(Resource=resource)

    def getResourceAvailableByCatName(self, categoryname):
        dao = ResourcesDAO()
        resources_list = dao.getResourceAvailableByCatName(categoryname)
        if not resources_list:
            return jsonify(Error="Resource Not Found "), 404
        else:
            result_list = []
            for row in resources_list:
                result = self.build_resourcecatname_dict(row)
                result_list.append(result)
            return jsonify(Resources=result_list)

    def getResourceRequestedByName(self, resourcename):
        dao = ResourcesDAO()
        resources_list = dao.getResourceRequestedByName(resourcename)
        if not resources_list:
            return jsonify(Error="Resource Not Found "), 404
        else:
            result_list = []
            for row in resources_list:
                result = self.build_resource_dict(row)
                result_list.append(result)
            return jsonify(Resources=result_list)

    def getResourceByCategoryName(self, categoryname):
        dao = ResourcesDAO()
        row = dao.getResourcesByCategoryName(categoryname)
        if not row:
            return jsonify(Error="Resource Not Found "), 404
        else:
            resource = self.build_resource_dict(row)
            return jsonify(Resource=resource)

    def getResourceByID(self, resourceid):
        dao = ResourcesDAO()
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
            resources_list = dao.getResourcesByAttributeName(attributename)
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
        resourcename = form['resourcename']
        resourceprice = form['resourceprice']
        resourcequantity = form['resourcequantity']
        supplierid = form['supplierid']
        if resourcename and resourceprice and resourcequantity and supplierid:
            dao = ResourcesDAO()
            resourceid = dao.insert(resourcename, resourceprice, resourcequantity, supplierid)
            # supplierid = dao.getSupplierByResourceID(resourceid) #duda
            result = self.build_resource_attributes(resourceid, resourcename, resourceprice,
                                                    resourcequantity, supplierid)
            return jsonify(Resource=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertResourceJson(self, json):
        resourcename = json['ResourceName']
        resourceprice = json['ResourcePrice']
        resourcequantity = json['ResourceQuantity']
        supplierid = json['SupplierID']
        if resourcename and resourceprice and resourcequantity and supplierid:
            dao = ResourcesDAO()
            resourceid = dao.insert(resourcename, resourceprice, resourcequantity, supplierid)
            result = self.build_resource_attributes(resourceid, resourcename, resourceprice,
                                                    resourcequantity, supplierid)
            return jsonify(Resource=result), 201
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
                resourcename = form['resourcename']
                resourceprice = form['resourceprice']
                resourcequantity = form['resourcequantity']
                supplierid = form['supplierid']
                if resourcename and resourceprice and resourcequantity and supplierid:
                    dao.update(resourceid, resourcename, resourceprice, resourcequantity, supplierid)
                    result = self.build_resource_attributes(resourceid, resourcename, resourceprice,
                                                            resourcequantity, supplierid)
                    return jsonify(Resource=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

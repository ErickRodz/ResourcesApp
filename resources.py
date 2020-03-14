from flask import jsonify
from dao.resources import ResourcesDAO

class ResourceHandler:
    def build_resource_dict(self, row):
        result ={}
        result['resourceid'] = row[0]
        result['resourcename'] = row[1]
        result['resourcetype'] = row[2]
        result['resourcevendor'] = row[3]
        result['resourcelocation'] = row[4]
        result['resourceprice'] = row[5]
        return result

    def build_resource_attributes(self, resourceid, resourcename, resourcetype, resourcevendor, resourcelocation, resourceprice):
        result = {}
        result['resourceid'] = resourceid
        result['resourcename'] = resourcename
        result['resourcetype'] = resourcetype
        result['resourcevendor'] = resourcevendor
        result['resourcelocation'] = resourcelocation
        result['resourceprice'] = resourceprice
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
            return jsonify(Error = "Resource Not Found ") , 404
        else:
            resource = self.build_resource_dict(row)
            return jsonify(Resource=resource)

    def searchResources(self, args):
        #resourcename = args.get("resourcename") #dudoso
        resourcetype = args.get("resourcetype")
        resourcevendor = args.get("resourcevendor")
        dao = ResourcesDAO()
        resources_list = []
        if(len(args) ==2) and resourcetype and resourcevendor:
            resources_list = dao.getResourcesByTypeAndVendor( resourcetype, resourcevendor)
        elif(len(args)==1) and resourcetype:
            resources_list = dao.getResourcesByType(resourcetype)
        elif(len(args)==1) and resourcevendor:
            resources_list = dao.getResourcesByVendor(resourcevendor)
        else:
            return jsonify(Error = "Malformed query string"),400
        result_list =[]
        for row in resources_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resources = result_list)

    def insertResource(self, form):
        print("form: ", form)
        if len(form) !=5:
            return jsonify(Error = "Malformed post request")
        resourcename = form['resourcename']
        resourceprice = form['resourceprice']
        resourcetype = form['resourcetype']
        resourcevendor = form['resurcevendor']
        if resourcevendor and resourceprice and resourcetype and resourcename :
            dao = ResourcesDAO()
            resourceid = dao.insert(resourcename, resourcetype, resourcevendor, resourceprice)
            result = self.build_resource_attributes(resourceid, resourcename, resourcetype, resourcevendor, resourceprice)
            return jsonify(Resource=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def insertResourceJson(self, json):
        resourcename = json['resourcename']
        resourceprice = json['resourceprice']
        resourcetype = json['resourcetype']
        resourcevendor = json['resourcevendor']
        if resourcetype and resourceprice and resourcevendor and resourcename:
            dao = ResourcesDAO()
            resourceid = dao.insert(resourcename, resourcetype, resourcevendor, resourceprice)
            result = self.build_resource_attributes(resourceid, resourcename, resourcetype, resourcevendor, resourceprice)
            return jsonify(Resources=result),201
        else:
            return jsonify(Error = "Unexpected attributes in post request")
        





from flask import jsonify
from dao.ice import IceDAO


class IceHandler:
    def build_ice_dict(self, row):
        result = {}
        result['IceID'] = row[0]
        result['IceSize'] = row[1]
        result['IceDescription'] = row[2]
        result['ResourceID'] = row[3]
        return result
    
    def build_ice_attributes(self, iceid, icesize, icedescription, resourceid):
        result = {}
        result['IceID'] = iceid
        result['Iceize'] = icesize
        result['IceDescription'] = icedescription
        result['ResourceID'] = resourceid
        return result
    
    def getAllIce(self):
        dao = IceDAO()
        ice_list = dao.getAllIce()
        result_list = []
        for row in ice_list:
            result = self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Ice=result_list)
    
    def getIceByID(self, iceid):
        dao = IceDAO()
        row = dao.getIceById(iceid)
        if not row:
            return jsonify(Error="Ice not found"), 404
        else:
            ice = self.build_ice_dict(row)
            return ice
        
    def getIceByResourceID(self, resourceid):
        dao = IceDAO()
        row = dao.getIceByResourceID(resourceid)
        if not row:
            return jsonify(Error="Ice Not Found "), 404
        else:
            Ice = self.build_ice_dict(row)
            return jsonify(Ice=Ice)

    def getResourceIDByIceID(self, Iceid):
        dao = IceDAO()
        row = dao.getResourceIDByIceID(Iceid)
        if not row:
            return jsonify(Error="Ice Not Found "), 404
        else:
            Ice = self.build_ice_dict(row)
            return jsonify(Ice=Ice)

        
    def searchIce(self, args):
        icesize = args.get('icesize')
        icedescription = args.get('icedescription')
        dao = IceDAO()
        ice_list = []
        if icesize:
            ice_list = dao.getIceBySize(icesize)
        elif icedescription:
            ice_list = dao.getIceByDescription(icedescription)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in ice_list:
            result= self.build_ice_dict(row)
            result_list.append(result)
        return jsonify(Ice=result_list)

    def insertIce(self, form):
        if (len(form) != 3):
            return jsonify(Error="Malformed post request"), 404
        else:
            resourceid = form['resourceid']
            icesize = form['icesize']
            icedescription = form['icedescription']
            if resourceid and icesize and icedescription:
                dao = IceDAO()
                iceid = dao.insert(resourceid, icesize, icedescription)
                result = self.build_ice_attributes(iceid, resourceid, icesize, icedescription)
                return jsonify(Ice=result)
            else:
                return jsonify(Error="Unexpected attributes in post request"), 404

    def insertIceJson(self, json):
        icesize = json['IceSize']
        icedescription = json['IceDescription']
        resourceid = json['ResourceID']
        if resourceid and icesize and icedescription:
            dao = IceDAO()
            iceid = dao.insert(icesize, icedescription, resourceid)
            result = self.build_ice_attributes(iceid, icesize, icedescription, resourceid)
            return jsonify(Ice=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")
    
    def deleteIce(self, iceid):
        dao = IceDAO()
        if not dao.getIceById(iceid):
            return jsonify("Error ice not found")
        else:
            dao.delete(iceid)
            return jsonify(DeleteStatus="OK")
    
    def update(self, iceid, form):
        dao = IceDAO()
        if not dao.getIceById(iceid):
            return jsonify(Error="Ice not found"), 404
        else:
            icesize = form['icesize']
            icedescription = form['icedescription']
            if icesize and icedescription:
                dao.update(iceid, icesize, icedescription)
    
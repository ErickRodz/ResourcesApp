from flask import jsonify
from dao.medicalequipment import MedicalEquipmentDAO


class MedicalEquipmentHandler:
    def build_medicalequipment_dict(self, row):
        result = {}
        result['MedEqID'] = row[0]
        result['MedEqBrand'] = row[1]
        result['MedEqDescription'] = row[2]
        result['ResourceID'] = row[3]
        return result
    
    def build_medicalequipment_attributes(self, medeqid, medeqbrand, medeqdescription, resourceid):
        result = {}
        result['MedEqID'] = medeqid
        result['MedEqBrand'] = medeqbrand
        result['MedEqDescription'] = medeqdescription
        result['ResourceID'] = resourceid
        return result

    def build_medicaldetails_dict(self, row):
        result = {}
        result['ResourceID'] = row[0]
        result['ResourceName'] = row[1]
        result['ResourcePrice'] = row[2]
        result['ResourceQuantity'] = row[3]
        result['SupplierID'] = row[4]
        result['MedEqID'] = row[5]
        result['MedEqBrand'] = row[6]
        result['MedEqDescription'] = row[7]
        return result
    
    def getAllMedicalEquipment(self):
        dao = MedicalEquipmentDAO()
        medeq_list = dao.getAllMedicalEquipment()
        result_list = []
        for row in medeq_list:
            result = self.build_medicalequipment_dict(row)
            result_list.append(result)
        return jsonify(MedEq=result_list)
    
    def getMedicalEquipmentByID(self, medeqid):
        dao = MedicalEquipmentDAO()
        row = dao.getMedicalEquipmentById(medeqid)
        if not row:
            return jsonify(Error="Medical equipment not found"), 404
        else:
            medeq = self.build_medicalequipment_dict(row)
            return jsonify(MedEq=medeq)
        
    def getMedicalEquipmentByResourceID(self, resourceid):
        dao = MedicalEquipmentDAO()
        row = dao.getMedEqByResourceID(resourceid)
        if not row:
            return jsonify(Error="MedicalEq Not Found "), 404
        else:
            MedicalEq = self.build_medicaldetails_dict(row)
            return jsonify(MedicalEq=MedicalEq)

    def getResourceIDByMedicalEqID(self, MedicalEqid):
        dao = MedicalEquipmentDAO()
        row = dao.getResourceIDByMedEqID(MedicalEqid)
        if not row:
            return jsonify(Error="MedicalEq Not Found "), 404
        else:
            MedicalEq = self.build_medicalequipment_dict(row)
            return jsonify(MedicalEq=MedicalEq)

    
    def searchMedicalEquipment(self, args):
        # resourceid = args.get('resourceid')
        medeqbrand = args.get('medeqbrand')
        medeqdescription = args.get('meddescription')
        dao = MedicalEquipmentDAO()
        medeq_list = []
        if (len(args) == 1) and medeqbrand:
            medeq_list = dao.getMedicalEquipmentByBrand(medeqbrand)
        elif (len(args) == 1) and medeqdescription:
            medeq_list = dao.getMedicalEquipmentByDescription(medeqdescription)
        else:
            return jsonify(Error="Malformed query string"), 404
        result_list = []
        for row in medeq_list:
            result = self.build_medicalequipment_dict(row)
            result_list.append(result)
        return jsonify(MedEq=result_list)
    
    def insertMedicalEquipment(self, form):
        if (len(form) != 3):
            return jsonify(Error="Malformed post request"), 404
        resourceid = form['resourceid']
        medeqbrand = form['medeqbrand']
        medeqdescription = form['medeqdescription']
        if resourceid and medeqbrand and medeqdescription:
            dao = MedicalEquipmentDAO()
            medeqid = dao.insert(resourceid, medeqbrand, medeqdescription)
            result = self.build_medicalequipment_attributes(medeqid, resourceid, medeqbrand, medeqdescription)
            return jsonify(MedEq=result)
        else:
            return jsonify(Error="Unexpected attributes in post request"), 404

    def insertMedicalEquipmentJson(self, json):
        medeqbrand = json['MedEqBrand']
        medeqdescription = json['MedEqDescription']
        resourceid = json['ResourceID']
        if resourceid and medeqbrand and medeqdescription:
            dao = MedicalEquipmentDAO()
            medeqid = dao.insert(medeqbrand, medeqdescription, resourceid)
            result = self.build_medicalequipment_attributes(medeqid, medeqbrand, medeqdescription, resourceid)
            return jsonify(Medication=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400
    
    def deleteMedicalEquipment(self, medeqid):
        dao = MedicalEquipmentDAO()
        if not dao.getMedicalEquipmentById(medeqid):
            return jsonify(Error="Medical Equipment not found"), 404
        else:
            dao.delete(medeqid)
            return jsonify(DeleteStatus="OK"), 200
    
    def updateMedicalEquipment(self, medeqid, form):
        dao = MedicalEquipmentDAO()
        if not dao.getMedicalEquipmentById(medeqid):
            return jsonify(Error="Medical Equipment not found"), 404
        else:
            resourceid = form['resourceid']
            medeqbrand = form['medeqbrand']
            medeqdescription = form['medeqdescription']
            if resourceid and medeqbrand and medeqdescription:
                dao.update(medeqid, medeqbrand, medeqdescription)
                result = self.build_medicalequipment_attributes(medeqid, resourceid, medeqbrand, medeqdescription)
                return jsonify(MedEq=resourceid), 200
            else:
                return jsonify(Error="Unexpected attributes in put reqquest"), 404
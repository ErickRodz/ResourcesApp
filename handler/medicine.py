from flask import jsonify
from dao.medicine import MedicineDAO


class MedicineHandler:
    def build_medicine_dict(self, row):
        result = {}
        result['medid'] = row[0]
        result['meddose'] = row[1]
        result['meddescription'] = row[2]
        result['resourceid'] = row[3]
        return result

    def build_medicine_attributes(self, medid, meddose, meddescription, resourceid):
        result = {}
        result['medid'] = medid
        result['meddose'] = meddose
        result['meddescription'] = meddescription
        result['resourceid'] = resourceid
        return result

    def getAllMedicine(self):
        dao = MedicineDAO()
        medicine_list = dao.getAllMedicine()
        result_list = []
        for row in medicine_list:
            result = self.build_medicine_dict(row)
            result_list.append(result)
        return jsonify(Medicine=result_list)
    
    def getMedicineByID(self, medid):
        dao = MedicineDAO()
        row = dao.getMedicineById(medid)
        if not row:
            return jsonify(Error="Medicine nnot found"), 404
        else:
            medicine = self.build_medicine_dict(row)
            return jsonify(Medicine=medicine)
        
    def getMedicineByResourceID(self, resourceid):
        dao = MedicineDAO()
        row = dao.getMedicineByResourceID(resourceid)
        if not row:
            return jsonify(Error="Medicine Not Found "), 404
        else:
            Medicine = self.build_medicine_dict(row)
            return jsonify(Medicine=Medicine)

    def getResourceIDByMedicineID(self, Medicineid):
        dao = MedicineDAO()
        row = dao.getResourceIDByMedicineID(Medicineid)
        if not row:
            return jsonify(Error="Medicine Not Found "), 404
        else:
            Medicine = self.build_medicine_dict(row)
            return jsonify(Medicine=Medicine)
    
    def searchMedecine(self, args):
        meddose = args.get('meddose')
        meddescription = args.get('meddescription')
        dao = MedicineDAO()
        medicine_list = []
        if (len(args) == 1) and meddose:
            medicine_list = dao.getMedicineByDose(meddose)
        elif (len(args) == 1) and meddescription:
            medicine_list = dao.getMedicineByDescription(meddescription)
        else:
            return jsonify(Error="Malformed query string"), 404
        result_list = []
        for row in medicine_list:
            result = self.build_medicine_dict(row)
            result_list.append(result)
        return jsonify(Medicine=result_list)

    def insertMedicine(self, form):
        if (len(form) != 3):
            return jsonify(Error="Malformed post request"), 404
        resourceid = form['resourceid']
        meddose = form['meddose']
        meddescription = form['meddescription']
        if resourceid and meddose and meddescription:
            dao = MedicineDAO()
            medid = dao.insert(resourceid, meddose, meddescription)
            result = self.build_medicine_attributes(medid, resourceid, meddose, meddescription)
            return jsonify(Medicine=result)
        else:
            return jsonify(Error="Unepected attributes in post request"), 404
    
    def deleteMedicine(self, medid):
        dao = MedicineDAO()
        if not dao.getMedicineById(medid):
            return jsonify(Error="Medicine not found"), 404
        else:
            dao.delete(medid)
            return jsonify(DeleteStatus="OK"), 200
    
    def updateMedicine(self, medid, form):
        dao = MedicineDAO()
        if not dao.getMedicineById(medid):
            return jsonify(Error="Medicine not found"), 404
        else:
            resourceid = form['resourceid']
            meddose = form['meddose']
            meddescription = form['meddescription']
            if meddose and meddescription:
                dao.update(medid, meddose, meddescription)
                result = self.build_medicine_attributes(medid, resourceid, meddose, meddescription)
                return jsonify(Medicine=result)
            else:
                return jsonify(Error="Unepected attributes in put request"), 404
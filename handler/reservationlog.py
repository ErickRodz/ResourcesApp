from flask import jsonify
from dao.reservationlog import ReservationLogsDAO


class ReservationLogHandler:
    def build_reservationlog_dict(self, row):
        result = {}
        result['reservationid'] = row[0]
        result['userid'] = row[1]
        result['resourceid'] = row[2]
        return result

    def build_reservationlog_attributes(self, reservationid, userid, resourceid):
        result = {}
        result['reservationid'] = reservationid
        result['userid'] = userid
        result['resourceid'] = resourceid
        return result

    def getAllReservationLogs(self):
        dao = ReservationLogsDAO()
        reservationlog_list = dao.getAllLogs()
        result_list = []
        for row in result_list:
            result = self.build_reservationlog_dict(row)
            result_list.append(result)
        return jsonify(ReservationLog=result_list)
    
    def getReservationLogById(self, reservationid):
        dao = ReservationLogsDAO()
        row = dao.getReservationLogById(reservationid)
        if not row:
            return jsonify(Error = "Reservation log not found"), 404
        else:
            reservationlog = self.build_reservationlog_dict(row)
            return jsonify(ReservationLog=reservationlog)

    def getReservationLogByUserId(self, userid):
        dao = ReservationLogsDAO()
        row = dao.getReservationLogByUserId(userid)
        if not row:
            return jsonify(Error = "User id not found"), 404
        else:
            reservationlog = self.build_reservationlog_dict(row)
            return jsonify(ReservationLog = reservationlog)

    def getReservationLogByResourceId(self, resourceid):
        dao = ReservationLogsDAO()
        row = dao.getReservationLogByResourceId(resourceid)
        if not row:
            return jsonify(Error = "Resorce id not found"), 404
        else:
            reservationlogs = self.build_reservationlog_dict(row)
            return jsonify(ReservationLog = reservationlogs)

    def searchReservationLog(self, args):
        userid = args.get("userid")
        resourceid = args.get("resourceid")
        dao = ReservationLogsDAO()
        reservationlog_list = []
        if (len(args) == 2 and userid and resourceid):
            reservationlog_list = dao.getReservationByUserIdAndResourceId(userid, resourceid)
        if (len(args) == 1 and userid):
            reservationlog_list = dao.getReservationLogByUserId(userid)
        elif (len(args) == 1 and resourceid):
            reservationlog_list = dao.getReservationLogByResourceId(resourceid)
        else:
            return jsonify(Error = "Malformed query string"), 404
        result_list = []
        for row in reservationlog_list:
            result = self.build_reservationlog_dict(row)
            result_list.append(result)
        return jsonify(ReservationLog = result_list)

    def insertReservationLog(self, form):
        print("form: ", form)
        if len(form) != 2:
            return jsonify(Error = "Malformed post request"), 404
        else:
            userid = form["UserID"]
            resourceid = form["ResourceID"]
            if userid and resourceid:
                dao = ReservationLogsDAO()
                reservationlogid = dao.insert(userid, resourceid)
                result = self.build_reservationlog_attributes(reservationlogid, userid, resourceid)
                return jsonify(ReservationLog = result), 201
            else:
                return jsonify(Error = "Unexpected attributes in post request")
    
    def insertReservationLogJson(self, json):
        userid = json["UserID"]
        resourceid = json["ResourceID"]
        if userid and resourceid:
            dao = ReservationLogsDAO()
            reservationid = dao.insert(userid, resourceid)
            result = self.build_reservationlog_attributes(reservationid, userid, resourceid)
        else:
            return jsonify(Error = "Unexpected attributes in post request"), 404
    
    def deleteReservationlog(self, reservationid):
        dao = ReservationLogsDAO()
        if not dao.getReservationLogById(reservationid):
            return jsonify(Error = "Reservation id not found")
        else:
            dao.delete(reservationid)
            return jsonify(DeleteStatus= "OK"), 200

    def updateReservationLog(self, reservationid, form):
        dao = ReservationLogsDAO()
        if not dao.getReservationLogById(reservationid):
            return jsonify(Error = "User not found."), 404
        else:
            if len(form) != 2:
                return jsonify(Error="Malformed update request"), 400
            else:
                userid = form["UserID"]
                resourceid = form["ResourceID"]
                if userid and resourceid:
                    dao.update(userid, resourceid)
                    result = self.build_rservationlogs_attributes(userid, resourceid)
                    return jsonify(ReservationLog=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
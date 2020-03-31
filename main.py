from flask import Flask, jsonify, request
from handler.resources import ResourceHandler
from handler.suppliers import SuppliersHandler
from handler.users import UsersHandler
from handler.administrators import AdministratorsHandler
from flask_cors import CORS, cross_origin

# Activate
app = Flask(__name__)

# Apply CORS to this app
CORS(app)


@app.route('/')
def greeting():
    return 'Hello, welcome to our Sales App!'


@app.route('/ProyectoDB/users', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        #No poseido por Satanas. At least, for now.
        #Commented the working stuff for phase 1
       # print("REQUEST: ", request.json)
       # return UsersHandler().insertUserJson(request.json)
        return 'Accessing Users POST Method'
    else:
        if not request.args:
            #return UsersHandler().getAllUsers()
            return 'Accessing GET All Users Method'
        else:
            #return UsersHandler().searchUsers(request.args)
            return 'Accessing Search Users Method'


@app.route('/ProyectoDB/users/<int:userid>', methods=['GET', 'PUT', 'DELETE'])
def getUserById(userid):
    if request.method == 'GET':
       # return UsersHandler().getUserById(userid)
       return 'Accessing the GET Users By Id Method'
    elif request.method == 'PUT':
       # return UsersHandler().updateUser(userid, request.form)
        return 'Accessing the PUT Method in Users'
    elif request.method == 'DELETE':
       # return UsersHandler().deleteUser(userid)
        return 'Accessing the DELETE Method in Users'
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/ProyectoDB/suppliers', methods=['GET', 'POST'])
def getAllSuppliers():
    if request.method == 'POST':
        #return SuppliersHandler().insertSupplierJson(request.json)
        return 'Accessing the POST Suppliers Method '
    else :
        if not request.args:
            #return SuppliersHandler().getAllSuppliers()
            return 'Accessing the GET all Suppliers Method'
        else:
            return SuppliersHandler().searchSuppliers(request.args)

@app.route('/ProyectoDB/suppliers/<int:supplierid>',
           methods=['GET', 'PUT', 'DELETE'])
def getSupplierById(supplierid):
    if request.method == 'GET':
        #return SuppliersHandler().getSupplierById(supplierid)
        return 'Accessing the GET Suppliers by Id Method'
    elif request.method == 'PUT':
        #pass
        return 'Accessing the PUT Suppliers Method'
    elif request.method == 'DELETE':
        #pass
        return 'Accessing the DELETE Suppliers Method'
    else:
        return jsonify(Error = "Method not allowed"), 405


@app.route('/ProyectoDB/administrator', methods=['GET', 'POST'])
def getAllAdministrators():
        if request.method == 'POST':
            # No poseido por Satanas. At least, for now.
            # Testing still neccesarry
            print("REQUEST: ", request.json)
            #return AdministratorsHandler().insertAdministratorJson(request.json)
            return 'Accessing the PUT Administrators Method'
        else:
            if not request.args:
                #return AdministratorsHandler().getAllAdministrators()
                return 'Accessing the GET all administrators Method'
            else:
                return AdministratorsHandler().searchAdministrators(request.args)

@app.route('/ProyectoDB/administrator/<int:administratorid>', methods=['GET', 'PUT', 'DELETE'])
def getAdministratorsbyId(administratorid):
        if request.method == 'GET':
            #return AdministratorsHandler().getAdministratorById(administratorid)
            return 'Accessing the GET Administrators by Id Method'
        elif request.method == 'PUT':
            #return AdministratorsHandler().updateAdministrator(administratorid, request.form)
            return 'Accessing the PUT Administrators Method'
        elif request.method == 'DELETE':
            #return AdministratorsHandler().deleteAdministrator(administratorid)
            return 'Accessing the DELETE Administrators Method'
        else:
            return jsonify(Error="Method not allowed."), 405


@app.route('/ProyectoDB/resources', methods=['GET', 'POST'])
def getAllResources():
    if request.method == 'POST':
        # cambie a request.json pq el form no estaba bregando
        # parece q estaba poseido por satanas ...
        # DEBUG a ver q trae el json q manda el cliente con la nueva pieza
        print("REQUEST: ", request.json)
        #return ResourceHandler().insertResourceJson(request.json)
        return 'Accessing Resources POST Method'
    else:
        if not request.args:
            #return ResourceHandler().getAllResources()
            return 'Accessing GET all Resources Method'
        else:
            #return ResourceHandler().searchResources(request.args)
            return 'Accesing Search Resources Method'

@app.route('/ProyectoDB/resources/<int:resourceid>', methods=['GET', 'PUT', 'DELETE'])
def getResourceById(resourceid):
    if request.method == 'GET':
       # return ResourceHandler().getResourceByID(resourceid)
         return 'Accessing the GET Resources by Id Method'
    elif request.method == 'PUT':
        #return ResourceHandler().updateResource(resourceid, request.form)
        return 'Accesing the PUT Method in Resources'
    elif request.method == 'DELETE':
        #return ResourceHandler().deletResource(resourceid)
        return 'Accesing the DELETE Resources Method'

    else:

        return jsonify(Error="Method not allowed."), 405

@app.route('/ProyectoDB/usercart', methods=['GET', 'POST'])
def getAllCarts():
    if request.method == 'POST':
        #No poseido por Satanas. At least, for now.
        #Commented the working stuff for phase 1
       # print("REQUEST: ", request.json)
       # return UsersHandler().insertUserJson(request.json)
        return 'Accessing Userscart POST Method'
    else:
        if not request.args:
            #return UsersHandler().getAllUsers()
            return 'Accessing GET All Carts Method'
        else:
            #return UsersHandler().searchUsers(request.args)
            return 'Accessing Search Carts Method'


@app.route('/ProyectoDB/usercart/<int:cartid>', methods=['GET', 'PUT', 'DELETE'])
def getCartById(cartid):
    if request.method == 'GET':
       # return UsersHandler().getUserById(userid)
       return 'Accessing the GET Cart By Id Method'
    elif request.method == 'PUT':
       # return UsersHandler().updateUser(userid, request.form)
        return 'Accessing the PUT Method in Carts'
    elif request.method == 'DELETE':
       # return UsersHandler().deleteUser(userid)
        return 'Accessing the DELETE Method in Carts'
    else:
        return jsonify(Error="Method not allowed."), 405
#Must make a new class or method that searches the Carts by UserID for obvious reasons.


@app.route('/ProyectoDB/attributes/<int:attributeid>', methods=['GET', 'PUT','DELETE'])
def getAttributesById(attributeid):
    if request.method == 'GET':
        #return AttributeHandler().getAttributeByID(attributeid)
        return 'Accessing the GET Attributes by Id Method'
    elif request.method == 'PUT':
        #return AttributeHandler().updateAttribute(attributeid, request.form)
        return 'Accessing the PUT Attributes Method'
    elif request.method == 'DELETE':
        #return AttributeHandler().deleteAttribute(attributeid)
        return 'Accessing the DELETE Attributes Method'

@app.route('/ProyectoDB/attributes', methods=['GET', 'POST'])
def getAllAttributes():
        if request.method == 'POST':
            # No poseido por Satanas. At least, for now.
            # Testing still neccesarry
            print("REQUEST: ", request.json)
            #return AttributeHandler().insertAttributeJson(request.json)
            return 'Accessing the POST Attributes Method'
        else:
            if not request.args:
                #pass
                 return 'Accessing the GET all Attributes Method'
            else:
                #return AttributeHandler().searchAttributes(request.args)
                 return 'Accessing the Search Attributes Method'


@app.route('/ProyectoDB/reservationlog', methods=['GET', 'POST'])
def getAllReservations():
    if request.method == 'POST':
        #No poseido por Satanas. At least, for now.
        #Commented the working stuff for phase 1
       # print("REQUEST: ", request.json)
       # return ReservationLogHandler().insertReservationLogJson(request.json)
        return 'Accessing ReservationLog POST Method'
    else:
        if not request.args:
            #return ReservationLogHandler().getAllReservationLogs()
            return 'Accessing GET All ReservationLog Method'
        else:
            #return ReservationLogHandler().searchReservationLogs(request.args)
            return 'Accessing Search ReservationLog Method'


@app.route('/ProyectoDB/reservationlog/<int:reservationid>', methods=['GET', 'PUT', 'DELETE'])
def getReservationById(reservationid):
    if request.method == 'GET':
       # return ReservationLogHandler().getReservationLogById(reservationid)
       return 'Accessing the GET ReservationLog By Id Method'
    elif request.method == 'PUT':
       # return ReservationLogHandler().updateReservationLog(reservationid, request.form)
        return 'Accessing the PUT Method in ReservationLog'
    elif request.method == 'DELETE':
       # return ReservationLogHandler().deleteReservation(userid)
        return 'Accessing the DELETE Method in ReservationLog'
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/ProyectoDB/purchaselog', methods=['GET', 'POST'])
def getAllPurchases():
    if request.method == 'POST':
        #No poseido por Satanas. At least, for now.
        #Commented the working stuff for phase 1
       # print("REQUEST: ", request.json)
       # return ReservationLogHandler().insertReservationLogJson(request.json)
        return 'Accessing PurchaseLog POST Method'
    else:
        if not request.args:
            #return ReservationLogHandler().getAllReservationLogs()
            return 'Accessing GET All PurchaseLog Method'
        else:
            #return ReservationLogHandler().searchReservationLogs(request.args)
            return 'Accessing Search PurchaseLog Method'


@app.route('/ProyectoDB/purchaselog/<int:purchaseid>', methods=['GET', 'PUT', 'DELETE'])
def getPurchaseById(purchaseid):
    if request.method == 'GET':
       # return PurchaseLogHandler().getPurchaseLogById(purchaseid)
       return 'Accessing the GET PurchaseLog By Id Method'
    elif request.method == 'PUT':
       # return PurchaseLogHandler().updatePurchaseLog(purchaseid, request.form)
        return 'Accessing the PUT Method in PurchaseLog'
    elif request.method == 'DELETE':
       # return PurchaseLogHandler().deletePurchase(purchaseid)
        return 'Accessing the DELETE Method in PurchaseLog'
    else:
        return jsonify(Error="Method not allowed."), 405
#Must make a new class or method that searches the Carts by UserID for obvious reasons.


if __name__ == "__main__":
    app.run()

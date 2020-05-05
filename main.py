from flask import Flask, jsonify, request

from handler.resources import ResourceHandler
from handler.suppliers import SuppliersHandler
from handler.usercart import UserCartHandler
from handler.users import UsersHandler
from handler.administrators import AdministratorsHandler
from handler.paymentmethod import PaymentMethodHandler
from handler.bank import BankHandler
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
        print("REQUEST: ", request.json)
        return UsersHandler().insertUserJson(request.json)
    else:
        if not request.args:
            return UsersHandler().getAllUsers()
        else:
            return UsersHandler().searchUsers(request.args)


@app.route('/ProyectoDB/users/<int:userid>', methods=['GET', 'PUT', 'DELETE'])
def getUserById(userid):
    if request.method == 'GET':
        return UsersHandler().getUserById(userid)
    elif request.method == 'PUT':
        return UsersHandler().updateUserJson(userid, request.json)
    elif request.method == 'DELETE':
        return UsersHandler().deleteUser(userid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/ProyectoDB/suppliers', methods=['GET', 'POST'])
def getAllSuppliers():
    if request.method == 'POST':
        return SuppliersHandler().insertSupplierJson(request.json)
    else:
        if not request.args:
            return SuppliersHandler().getAllSuppliers()
        else:
            return SuppliersHandler().searchSuppliers(request.args)


@app.route('/ProyectoDB/suppliers/<int:supplierid>',
           methods=['GET', 'PUT', 'DELETE'])
def getSupplierById(supplierid):
    if request.method == 'GET':
         return SuppliersHandler().getSupplierById(supplierid)
    elif request.method == 'PUT':
         pass
    elif request.method == 'DELETE':
         pass
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/ProyectoDB/administrator', methods=['GET', 'POST'])
def getAllAdministrators():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return AdministratorsHandler().insertAdministratorJson(request.json)
    else:
        if not request.args:
            return AdministratorsHandler().getAllAdministrators()
        else:
            return AdministratorsHandler().searchAdministrators(request.args)


@app.route('/ProyectoDB/administrator/<int:administratorid>', methods=['GET', 'PUT', 'DELETE'])
def getAdministratorsbyId(administratorid):
    if request.method == 'GET':
        return AdministratorsHandler().getAdministratorById(administratorid)
    elif request.method == 'PUT':
        return AdministratorsHandler().updateAdministratorJson(administratorid, request.json)
    elif request.method == 'DELETE':
        return AdministratorsHandler().deleteAdministrator(administratorid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/ProyectoDB/resources', methods=['GET', 'POST'])
def getAllResources():
    if request.method == 'POST':
        # cambie a request.json pq el form no estaba bregando
        # parece q estaba poseido por satanas ...
        # DEBUG a ver q trae el json q manda el cliente con la nueva pieza
        print("REQUEST: ", request.json)
        return ResourceHandler().insertResourceJson(request.json)
    else:
        if not request.args:
            return ResourceHandler().getAllResources()
        else:
            return ResourceHandler().searchResources(request.args)


@app.route('/ProyectoDB/resources/<int:resourceid>', methods=['GET', 'PUT', 'DELETE'])
def getResourceById(resourceid):
    if request.method == 'GET':
        return ResourceHandler().getResourceByID(resourceid)
    elif request.method == 'PUT':
        return ResourceHandler().updateResource(resourceid, request.form)
    elif request.method == 'DELETE':
        return ResourceHandler().deletResource(resourceid)

    else:

        return jsonify(Error="Method not allowed."), 405


@app.route('/ProyectoDB/usercart', methods=['GET', 'POST'])
def getAllCarts():
    if request.method == 'POST':
        # No poseido por Satanas. At least, for now.
        # Commented the working stuff for phase 1
        print("REQUEST: ", request.json)
        return UserCartHandler().insertCartJson(request.json)
    else:
        if not request.args:
            return UserCartHandler().getAllCarts()
        else:
            return UserCartHandler().searchUserCarts(request.args)


@app.route('/ProyectoDB/usercart/<int:cartid>', methods=['GET', 'PUT', 'DELETE'])
def getCartById(cartid):
    if request.method == 'GET':
        return UserCartHandler().getCartById(cartid)
    elif request.method == 'PUT':
        return UserCartHandler().updateCartJson(cartid, request.json)
    elif request.method == 'DELETE':
        return UserCartHandler().deleteCart(cartid)
    else:
        return jsonify(Error="Method not allowed."), 405


# Must make a new class or method that searches the Carts by UserID for obvious reasons.

@app.route('/ProyectoDB/bank', methods=['GET', 'POST'])
def getAllBanks():
    if request.method == 'POST':
        # No poseido por Satanas. At least, for now.
        # Commented the working stuff for phase 1
        print("REQUEST: ", request.json)
        return BankHandler().insertBankJson(request.json)
    else:
        if not request.args:
            return BankHandler().getAllBanks()
        else:
            return BankHandler().searchBanks(request.args)

@app.route('/ProyectoDB/payment', methods=['GET', 'POST'])
def getAllPaymentMethods():
    if request.method == 'POST':
        # No poseido por Satanas. At least, for now.
        # Commented the working stuff for phase 1
        print("REQUEST: ", request.json)
        return PaymentMethodHandler().insertCardJson(request.json)
    else:
        if not request.args:
            return PaymentMethodHandler().getAllCards()
        else:
            return PaymentMethodHandler().searchCards(request.args)



# Must make a new class or method that searches the Carts by UserID for obvious reasons.


if __name__ == "__main__":
    app.run()

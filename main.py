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
        #Testing still neccesarry
        print("REQUEST: ", request.json)
        return UsersHandler().insertUsersJson(request.json)
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
        return UsersHandler().updateUser(userid, request.form)
    elif request.method == 'DELETE':
        return UsersHandler().deleteUser(userid)
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
        return ResourceHandler().getResourceById(resourceid)
    elif request.method == 'PUT':
        return ResourceHandler().updateResource(resourceid, request.form)
    elif request.method == 'DELETE':
        return ResourceHandler().deletResource(resourceid)
    else:

        return jsonify(Error="Method not allowed."), 405

@app.route('/ProyectoDB/suppliers', methods=['GET', 'POST'])
def getAllSuppliers():
    if request.method == 'POST':
        return SuppliersHandler().insertSupplier(request.form)
    else :
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
        return jsonify(Error = "Method not allowed"), 405
@app.route('/ProyectoDB/administrators', methods=['GET', 'POST'])
def getAllAdministrators():
        if request.method == 'POST':
            # No poseido por Satanas. At least, for now.
            # Testing still neccesarry
            print("REQUEST: ", request.json)
            return AdministratorsHandler().insertSuppliersJson(request.json)
        else:
            if not request.args:
                return AdministratorsHandler().getAllAdministrators()
            else:
                return AdministratorsHandler().searchAdministrators(request.args)

@app.route('/ProyectoDB/administrators/<int:administratorid>', methods=['GET', 'PUT', 'DELETE'])
def getAdministratorsbyId(administratorid):
        if request.method == 'GET':
            return AdministratorsHandler().getAdministratorById(administratorid)
        elif request.method == 'PUT':
            return AdministratorsHandler().updateAdministrator(administratorid, request.form)
        elif request.method == 'DELETE':
            return AdministratorsHandler().deleteAdministrator(administratorid)
        else:
            return jsonify(Error="Method not allowed."), 405
#@app.route('/ProyectoDB/suppliers/<int:suplierid>/parts')
#def getPartsBySuplierId(sid):
#    return ResourceHandler().getResources(sid)
if __name__  == "__main__":
    app.run()
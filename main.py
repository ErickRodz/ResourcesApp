from flask import Flask, jsonify, request

from handler.resources import ResourceHandler
from handler.suppliers import SuppliersHandler
from handler.usercart import UserCartHandler
from handler.users import UsersHandler
from handler.administrators import AdministratorsHandler
from handler.paymentmethod import PaymentMethodHandler
from handler.bank import BankHandler
from handler.orders import OrdersHandler
from handler.babyfood import BabyFoodHandler
from handler.batteries import BatteriesHandler
from handler.cannedfood import CannedFoodHandler
from handler.categories import CategoriesHandler
from handler.clothing import ClothingHandler
from handler.dryfood import DryFoodHandler
from handler.fuel import FuelHandler
from handler.generators import GeneratorsHandler
from handler.heavyequipment import HeavyEquipmentHandler
from handler.ice import IceHandler
from handler.medicalequipment import MedicalEquipmentHandler
from handler.medicine import MedicineHandler
from handler.parts import PartsHandler
from handler.tools import ToolsHandler
from handler.water import WaterHandler
from flask_cors import CORS, cross_origin

# Activate
app = Flask(__name__)

# Apply CORS to this app
CORS(app)


@app.route('/')
def greeting():
    return 'Hello, welcome to our Sales App!'


# 1
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


# 3
@app.route('/ProyectoDB/suppliers', methods=['GET', 'POST'])
def getAllSuppliers():
    if request.method == 'POST':
        return SuppliersHandler().insertSupplierJson(request.json)
    else:
        if not request.args:
            return SuppliersHandler().getAllSuppliers()
        else:
            return SuppliersHandler().searchSuppliers(request.args)


@app.route('/ProyectoDB/suppliers/<int:supplierid>',methods=['GET', 'PUT', 'DELETE'])
def getSupplierById(supplierid):
    if request.method == 'GET':
        return SuppliersHandler().getSupplierById(supplierid)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        return jsonify(Error="Method not allowed"), 405


# 1
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

@app.route('/ProyectoDB/category', methods=['GET', 'POST'])
def getAllCategories():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return CategoriesHandler().insertCategoriesJson(request.json)
    else:
        if not request.args:
            return CategoriesHandler().getAllCategories()
        else:
            return CategoriesHandler().searchCategories(request.args)

@app.route('/ProyectoDB/cannedfood', methods=['GET', 'POST'])
def getAllCFood():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return CannedFoodHandler().insertCFoodJson(request.json)
    else:
        if not request.args:
            return CannedFoodHandler().getAllCannedFood()
        else:
            return CannedFoodHandler().searchCannedFood(request.args)

@app.route('/ProyectoDB/babyfood', methods=['GET', 'POST'])
def getAllBFood():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return BabyFoodHandler().insertbfoodJson(request.json)
    else:
        if not request.args:
            return BabyFoodHandler().getAllBabyFood()
        else:
            return BabyFoodHandler().searchBabyFood(request.args)

@app.route('/ProyectoDB/dryfood', methods=['GET', 'POST'])
def getAllDFood():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return DryFoodHandler().insertDFoodJson(request.json)
    else:
        if not request.args:
            return DryFoodHandler().getAllDryFood()
        else:
            return DryFoodHandler().searchDryFood(request.args)

@app.route('/ProyectoDB/water', methods=['GET', 'POST'])
def getAllWater():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return WaterHandler().insertWaterJson(request.json)
    else:
        if not request.args:
            return WaterHandler().getAllWater()
        else:
            return WaterHandler().searchWater(request.args)

@app.route('/ProyectoDB/batteries', methods=['GET', 'POST'])
def getAllBatteries():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return BatteriesHandler().insertBatteryJson(request.json)
    else:
        if not request.args:
            return BatteriesHandler().getAllBatteries()
        else:
            return BatteriesHandler().searchBatteries(request.args)

@app.route('/ProyectoDB/ice', methods=['GET', 'POST'])
def getAllIce():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return IceHandler().insertIceJson(request.json)
    else:
        if not request.args:
            return IceHandler().getAllIce()
        else:
            return IceHandler().searchIce(request.args)

@app.route('/ProyectoDB/parts', methods=['GET', 'POST'])
def getAllParts():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return PartsHandler().insertPartsJson(request.json)
    else:
        if not request.args:
            return PartsHandler().getAllParts()
        else:
            return PartsHandler().searchParts(request.args)

@app.route('/ProyectoDB/tools', methods=['GET', 'POST'])
def getAllTools():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return ToolsHandler().insertToolJson(request.json)
    else:
        if not request.args:
            return ToolsHandler().getAllTools()
        else:
            return ToolsHandler().searchTools(request.args)

@app.route('/ProyectoDB/clothing', methods=['GET', 'POST'])
def getAllClothing():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return ClothingHandler().insertClothingJson(request.json)
    else:
        if not request.args:
            return ClothingHandler().getAllClothing()
        else:
            return ClothingHandler().searchClothing(request.args)

@app.route('/ProyectoDB/fuel', methods=['GET', 'POST'])
def getAllFuel():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return FuelHandler().insertFuelJson(request.json)
    else:
        if not request.args:
            return FuelHandler().getAllFuel()
        else:
            return FuelHandler().searchFuel(request.args)

@app.route('/ProyectoDB/medication', methods=['GET', 'POST'])
def getAllMedicine():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return MedicineHandler().insertMedicineJson(request.json)
    else:
        if not request.args:
            return MedicineHandler().getAllMedicine()
        else:
            return MedicineHandler().searchMedicine(request.args)

@app.route('/ProyectoDB/medequip', methods=['GET', 'POST'])
def getAllMedEquipment():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return MedicalEquipmentHandler().insertMedicalEquipmentJson(request.json)
    else:
        if not request.args:
            return MedicalEquipmentHandler().getAllMedicalEquipment()
        else:
            return MedicalEquipmentHandler().searchMedicalEquipment(request.args)

@app.route('/ProyectoDB/heavyequip', methods=['GET', 'POST'])
def getAllHeavyEquipment():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return HeavyEquipmentHandler().insertHeavyEquipmentJson(request.json)
    else:
        if not request.args:
            return HeavyEquipmentHandler().getAllHeavyEquipment()
        else:
            return HeavyEquipmentHandler().searchHeavyEquipment(request.args)

@app.route('/ProyectoDB/generators', methods=['GET', 'POST'])
def getAllGenerators():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return GeneratorsHandler().insertGeneratorJson(request.json)
    else:
        if not request.args:
            return GeneratorsHandler().getAllGenerators()
        else:
            return GeneratorsHandler().searcGenerators(request.args)

#Order Post, and Get of all Orders(Request, Purchase and Reservation alik)
@app.route('/ProyectoDB/orders', methods=['GET', 'POST'])
def getAllOrders():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return OrdersHandler().insertOrderJson(request.json)
    else:
        if not request.args:
            return OrdersHandler().getAllOrders()
        else:
            return OrdersHandler().searchOrders(request.args)

#From this point onwards is peculiar information. From this point upwards, its posts and basic gets
@app.route('/ProyectoDB/resources/<int:resourceid>', methods=['GET', 'PUT', 'DELETE'])
def getResourceById(resourceid):
    if request.method == 'GET':
        return ResourceHandler().getResourceByID(resourceid)
    elif request.method == 'PUT':
        return ResourceHandler().updateResource(resourceid, request.form)
    elif request.method == 'DELETE':
        return ResourceHandler().deleteResource(resourceid)
    else:
        return jsonify(Error="Method not allowed."), 405

#Special Gets
#5  Maybe also #8. #11.1 A get for all available resources. Which means we're announcing what's available. IE Number 5
@app.route('/ProyectoDB/resources/available', methods=['GET'])
def getAllResourcesAvailable():
    if request.method == 'GET':
        return ResourceHandler().getAllResourcesAvailable()

#10 (revised)
@app.route('/ProyectoDB/orders/<string:ordertype>/type/<string:categoryname>', methods=['GET'])
def getAllResourcesOrderedByResourceName(ordertype, categoryname):
    # Must make a new class or method that searches the Carts by UserID for obvious reasons.
    if request.method == 'GET':
        # No poseido por Satanas. At least, for now.
        # Commented the working stuff for phase 1
        return OrdersHandler().getResourcesOrderedByResourceNameandOrderType(ordertype, categoryname)

#11 (revised)
@app.route('/ProyectoDB/resources/available/<string:categoryname>', methods=['GET'])
def getResourceAvailableByCatName(categoryname):
    if request.method == 'GET':
        return ResourceHandler().getResourceAvailableByCatName(categoryname)

#10.2
#@app.route('/ProyectoDB/resources/request/<string:resourcename>', methods=['GET'])
#def getResourceRequestedByName(resourcename):
 #   if request.method == 'GET':
  #      return OrdersHandler().getResourceRequestedyByName(resourcename)



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


#4, and #6, #7 Used for Getting Orders(Purchase, Request, Reservations) by ordertype.
@app.route('/ProyectoDB/orders/<string:ordertype>', methods=['GET'])
def getOrdersByOrderType(ordertype):
    if request.method == 'GET':
        return OrdersHandler().getOrdersByOrderType(ordertype)
    else:
        return jsonify(Error="Method not allowed"), 405


#4, #6 as well, and possible #7
@app.route('/ProyectoDB/orders/request/<int:orderid>', methods=['GET'])
def getRequestsByOrderID(orderid):
    if request.method == 'GET':
        return OrdersHandler().getRequestByOrderID(orderid)
    else:
        return jsonify(Error="Method not allowed"), 405



@app.route('/ProyectoDB/orders/<int:cartid>/<string:ordertype>', methods=['GET'])
def getAllRequestsByCartIdAndOrderType(cartid, ordertype):
    # Must make a new class or method that searches the Carts by UserID for obvious reasons.
    if request.method == 'GET':
        # No poseido por Satanas. At least, for now.
        # Commented the working stuff for phase 1
        return OrdersHandler().getReciptsByCartIdAndOrderType(cartid, ordertype)

#6.2. The ability to get all Reservation/Request/Purchases, by Ordertype,
@app.route('/ProyectoDB/orders/<int:userid>/type/<string:ordertype>', methods=['GET'])
def getAllOrdersByUserIdAndOrderType(userid, ordertype):
    # Must make a new class or method that searches the Carts by UserID for obvious reasons.
    if request.method == 'GET':
        # No poseido por Satanas. At least, for now.
        # Commented the working stuff for phase 1
        return OrdersHandler().getOrdersByUserIdAndOrderType(userid, ordertype)


#9
@app.route('/ProyectoDB/categories/resources/<int:resourceid>', methods=['GET'])
def getAllResourceDetails(resourceid):
    categoryname = CategoriesHandler().getCategoryByResourceID(resourceid)
    if categoryname == "BabyFood":
        return BabyFoodHandler().getBabyFoodByResourceID(resourceid)
    elif categoryname == "Batteries":
        return BatteriesHandler().getBatteriesByResourceID(resourceid)
    elif categoryname == "CannedFood":
        return CannedFoodHandler().getCFoodByResourceID(resourceid)
    elif categoryname == "Clothing":
        return ClothingHandler().getClothingByResourceID(resourceid)
    elif categoryname == "DryFood":
        return DryFoodHandler().getDryFoodByResourceID(resourceid)
    elif categoryname == "Fuel":
        return FuelHandler().getFuelByResourceID(resourceid)
    elif categoryname == "Generators":
        return GeneratorsHandler().getGeneratorsByResourceID(resourceid)
    elif categoryname == "HeavyEquipment":
        return HeavyEquipmentHandler().getHeavyEquipmentByResourceID(resourceid)
    elif categoryname == "Ice":
        return IceHandler().getIceByResourceID(resourceid)
    elif categoryname == "MedicalEquipment":
        return MedicalEquipmentHandler().getMedicalEquipmentByResourceID(resourceid)
    elif categoryname == "Medication":
        return MedicineHandler().getMedicineByResourceID(resourceid)
    elif categoryname == "Parts":
        return PartsHandler().getPartsByResourceID(resourceid)
    elif categoryname == "Tools":
        return ToolsHandler().getToolsByResourceID(resourceid)
    elif categoryname == "Water":
        return WaterHandler().getWaterByResourceID(resourceid)

 # 11 Part 2
@app.route('/ProyectoDB/resources/available/order', methods=['GET'])
def getResourceAvailableByResourceName():
    if request.method == 'GET':
        return ResourceHandler().getAllResourcesAvailableOrderByResourceName()

    # 11 Part 2
@app.route('/ProyectoDB/', methods=['GET'])
def getResorceAvailableByName(resourcename):
    if request.method == 'GET':
        return ResourceHandler().getResourceAvailabilityByName(resourcename)

    # Phase 3 Stuff


#Get for Request, Reservation, and Purchase via OrderID
@app.route('/ProyectoDB/orders/<int:orderid>',methods=['GET', 'PUT', 'DELETE'])
def getOrdersById(orderid):
    if request.method == 'GET':
        return OrdersHandler().getOrdersByID(orderid)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        return jsonify(Error="Method not allowed"), 405

if __name__ == "__main__":
    app.run()

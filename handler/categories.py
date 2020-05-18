from flask import jsonify
from dao.categories import CategoriesDAO


class CategoriesHandler:
    def build_category_dict(self, row):
        result = {}
        result['CategoryID'] = row[0]
        result['CategoryName'] = row[1]
        result['ResourceID'] = row[2]
        result['SupplierID'] = row[3]
        return result

    def build_category_attributes(self, categoryid, resourceid, categoryname, supplierid):
        result = {}
        result['CategoryID'] = categoryid
        result['CategoryName'] = categoryname
        result['ResourceID'] = resourceid
        result['SupplierID'] = supplierid
        return result


    def getAllCategories(self):
        dao = CategoriesDAO()
        categories_list = dao.getAllCategories()
        result_list = []
        for row in categories_list:
            result = self.build_category_dict(row)
            result_list.append(result)
        return jsonify(Attributes=result_list)

    def getCategoryByID(self, categoryid):
        dao = CategoriesDAO
        row = dao.getCategoryById(categoryid)
        if not row:
            return jsonify(Error="Category Not Found "), 404
        else:
            category = self.build_category_dict(row)
            return jsonify(Category=category)

    def getCategoryByResourceID(self, resourceid):
        dao = CategoriesDAO()
        row = dao.getCategoryByResourceId(resourceid)
        if not row:
            return jsonify(Error="Category Not Found "), 404
        else:
            #print(type(row[0]))
            #attribute = self.build_category_dict(row)
            #return jsonify(Category=attribute)
            return row[0]
        # 9 in the Email Part 1
    #def getCategoryNameByResourceID(self, ResourceID):
       # dao = CategoriesDAO
       # row = dao.getCategoryNameByResourceID(ResourceID)
       # if not row:
        #    return jsonify (Error="CategoryName not found")
        #else:
         #   category = self.build_category_dict(row)
        #return category

    def searchCategories(self, args):
        resourceid = args.get("resourceid")
        supplierid = args.get("supplierid")
        dao = CategoriesDAO()
        categories_list = []
        if (len(args) == 1) and resourceid:
            categories_list = dao.getCategoryByResourceId(resourceid)
        elif (len(args) == 1) and supplierid:
            categories_list = dao.getCategoryBySupplierId(supplierid)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in categories_list:
            result = self.build_category_dict(row)
            result_list.append(result)
        return jsonify(Categories=result_list)

    def insertCategoriesJson(self, json):
        categoryname = json['CategoryName']
        resourceid = json['ResourceID']
        supplierid = json['SupplierID']
        if categoryname and resourceid and supplierid:
            dao = CategoriesDAO()
            categoryid = dao.insert(categoryname, resourceid, supplierid)
            result = self.build_category_attributes(categoryid, resourceid,
                                                    categoryname, supplierid)
            return jsonify(Category=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request")

    def deleteCategory(self, categoryid):
        dao = CategoriesDAO()
        if not dao.getCategoryById(categoryid):
            return jsonify(Error="Category not found."), 404
        else:
            dao.delete(categoryid)
            return jsonify(DeleteStatus="OK"), 200

    def updateCategory(self, categoryid, form):
        dao = CategoriesDAO()
        if not dao.getCategoryById(categoryid):
            return jsonify(Error="Category not found."), 404
        else:
            if len(form) != 3:
                return jsonify(Error="Malformed update request")
            else:
                resourceid = form['resourceid']
                categoryname = form['catgory']
                supplierid = form['supplierid']
                if resourceid and categoryname and supplierid:
                    dao.update(categoryid, resourceid, supplierid, categoryname)
                    result = self.build_category_attributes(categoryid, supplierid, resourceid,
                                                            categoryname)
                    return jsonify(Resource=result), 400
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400
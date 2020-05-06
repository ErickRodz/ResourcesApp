from flask import jsonify
from dao.tools import ToolsDAO


class ToolsHandler:
    def build_tools_dict(self, row):
        result = {}
        result['toolid'] = row[0]
        result['toolmaterial'] = row[1]
        result['toolcolor'] = row[2]
        result['tooldescription'] = row[3]
        result['resourceid'] = row[4]
        return result

    def build_tools_attributes(self, toolid, toolmaterial, toolcolor, tooldescription, resourceid):
        result = {}
        result['toolid'] = toolid
        result['toolmaterial'] = toolmaterial
        result['toolcolor'] = toolcolor
        result['tooldescription'] = tooldescription
        result['resourceid'] = resourceid
        return result
           
    def getAllTools(self):
        dao = ToolsDAO()
        tools_list = dao.getAllTools()
        result_list = []
        for row in tools_list:
            result = self.build_tools_dict(row)
            result_list.append(result)
        return jsonify(Tools=result_list)
    
    def getToolByID(self, toolid):
        dao = ToolsDAO()
        row = dao.getToolsById(toolid)
        if not row:
            return jsonify(Error="Tool not found"), 404
        else:
            tool = self.build_tools_dict(row)
            return jsonify(Tool=tool)
        
    def getToolsByResourceID(self, resourceid):
        dao = ToolsDAO()
        row = dao.getToolByResourceID(resourceid)
        if not row:
            return jsonify(Error="Tool Not Found "), 404
        else:
            Tool = self.build_tools_dict(row)
            return jsonify(Tool=Tool)

    def getResourceIDByToolID(self, Toolid):
        dao = ToolsDAO()
        row = dao.getResourceIDByToolID(Toolid)
        if not row:
            return jsonify(Error="Tool Not Found "), 404
        else:
            Tool = self.build_tools_dict(row)
            return jsonify(Tool=Tool)
    
    def searchTools(self, args):
        # resourceid = args.get('resourceid')
        toolmaterial = args.get('toolmaterial')
        toolcolor = args.get('toolcolor')
        tooldescription = args.get('tooldescription')
        dao = ToolsDAO()
        tools_list = []
        if (len(args) == 2) and toolmaterial and toolcolor:
            tools_list = dao.getTooldByColorAndMaterial(toolcolor, toolmaterial)
        elif (len(args) == 1) and toolmaterial:
            tools_list = dao.getToolsByMaterial(toolmaterial)
        elif (len(args) == 1) and toolcolor:
            tools_list = dao.getToolsByColor(toolcolor)
        elif (len(args) == 1) and tooldescription:
            tools_list = dao.getToolsByDescription(tooldescription)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in tools_list:
            result = self.build_tools_dict(row)
            result_list.append(result)
        return jsonify(Tools=result_list)
    
    def insertTool(self, form):
        if (len(form) != 4):
            return jsonify(Error="Malformed post request"), 404
        resourceid = form['resourceid']
        toolmaterial = form['toolmaterial']
        toolcolor = form['toolcolor']
        tooldescription = form['tooldescription']
        if resourceid and toolmaterial and toolcolor and toolcolor:
            dao = ToolsDAO()
            toolid = dao.insert(resourceid, toolmaterial, toolcolor, tooldescription)
            result = self.build_tools_attributes(toolid, resourceid, toolmaterial, toolcolor, tooldescription)
            return jsonify(Tool=result)
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteTool(self, toolid):
        dao = ToolsDAO()
        if not dao.getToolsById(toolid):
            return jsonify(Error="Tool not found"), 404
        else:
            dao.delete(toolid)
            return jsonify(DeleteStatus="OK"), 200

    def updateTool(self, toolid, form):
        dao = ToolsDAO()
        if not dao.getToolsById(toolid):
            return jsonify(Error="Tool not found"), 404
        else:
            resourceid = form['resourceid']
            toolmaterial = form['toolmaterial']
            toolcolor = form['toolcolor']
            tooldescription = form['tooldescription']
            if toolmaterial and toolcolor and tooldescription:
                dao.update(toolid, toolmaterial, toolcolor, tooldescription)
                result = self.build_tools_attributes(toolid, resourceid, toolmaterial, toolcolor, tooldescription)
                return jsonify(Tool=result), 200
            else:
                return jsonify(Error="Unepected attributes un put request"), 404
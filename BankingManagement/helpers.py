import json
def list_to_json(objList):
        # objs = []
        # if objList is not None:
        #     for obj in objList:
        #         objs.append(obj.to_json())
        json_str = json.dumps(objList)
        return json_str
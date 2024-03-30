def list_to_json(objList):
        objs = []
        if objList is not None:
            for obj in objList:
                objs.append(obj.to_json())
        return objs
from models import database, role as r, login_method as lm, transfer_method as tm, service as s 
from enums.role_type import RoleType

db = database.Database().get_db()
roles = db['roles']
login_methods = db['login_methods']
transfer_methods = db['transfer_methods']
services = db['services']
accounts = db['accounts']

admin = accounts.find_one({'Role': RoleType.ADMIN.value})
lst_collections = db.list_collection_names()
admin_id = admin["_id"]

def initialize_data():
    init_roles()
    init_login_methods()
    init_services()
    init_transfer_methods()

def init_roles():
    if "roles" not in lst_collections:
        lstRoles = [
            r.Role(role_name='User', value=RoleType.USER.value, created_by=admin_id, modified_by=admin_id),
            r.Role(role_name='Employee', value=RoleType.EMPLOYEE.value, created_by=admin_id, modified_by=admin_id),
            r.Role(role_name='Administrator', value=RoleType.ADMIN.value, created_by=admin_id, modified_by=admin_id)
        ]

        for role in lstRoles:
            roles.insert_one(role.to_json())

def init_login_methods():
    if "login-methods" in lst_collections:
        pass

def init_transfer_methods():
    if "transfer-methods" in lst_collections:
        pass

def init_services():
    if "services" in lst_collections:
        pass
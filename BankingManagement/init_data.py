from models import database, account as a, role as r, login_method as lm, transfer_method as tm, service as s 
from enums.role_type import RoleType
from enums.login_type import LoginType

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
    init_accounts()
    init_roles()
    init_login_methods()
    init_services()
    init_transfer_methods()

def init_accounts():
    acc = a.Account(username="admin", password="admin123@", role=RoleType.ADMIN.value)

    if "accounts" not in lst_collections:
        lstAccounts = [
            a.Account(username="user01", password="user01@", role=RoleType.USER.value),
            a.Account(username="employee01", password="employee01@", role=RoleType.EMPLOYEE.value),
            acc
        ]

        for account in lstAccounts:
            accounts.insert_one(account.to_json())
        return
    
    admin_account = accounts.find_one({"Role":RoleType.ADMIN.value, "Username":"admin"})
    if not admin_account:
        accounts.insert_one(acc.to_json())

def init_roles():
    if "roles" not in lst_collections:
        lstRoles = [
            r.Role(roleName='User', value=RoleType.USER.value, createdBy=admin_id, modifiedBy=admin_id),
            r.Role(roleName='Employee', value=RoleType.EMPLOYEE.value, createdBy=admin_id, modifiedBy=admin_id),
            r.Role(roleName='Administrator', value=RoleType.ADMIN.value, createdBy=admin_id, modifiedBy=admin_id)
        ]

        for role in lstRoles:
            roles.insert_one(role.to_json())

def init_login_methods():
    if "login-methods" not in lst_collections:
        lstMethods = [
            lm.LoginMethod(methodName="By Username with password", value=LoginType.NORMAL.value, createdBy=admin_id, modifiedBy=admin_id),
            lm.LoginMethod(methodName="By face identifier", value=LoginType.FACE_ID.value, createdBy=admin_id, modifiedBy=admin_id),
            lm.LoginMethod(methodName="By finger print", value=LoginType.FINGER_PRINT.value, createdBy=admin_id, modifiedBy=admin_id)
        ]

        for method in lstMethods:
            login_methods.insert_one(method.to_json())

def init_transfer_methods():
    if "transfer-methods" not in lst_collections:
        pass

def init_services():
    if "services" not in lst_collections:
        pass
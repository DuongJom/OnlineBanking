from models import database, account as a, role as r, login_method as lm
from models import transfer_method as tm, card_type as t
from enums.role_type import RoleType
from enums.login_type import LoginType
from enums.transfer_type import TransferType
from enums.card_type import CardType

db = database.Database().get_db()
accounts = db['accounts']
roles = db['roles']
login_methods = db['login_methods']
transfer_methods = db['transfer_methods']
card_types = db['card_types']

admin = accounts.find_one({'Role': RoleType.ADMIN.value})
lst_collections = db.list_collection_names()
admin_id = admin["_id"]

def initialize_data(app):
    init_accounts(app)
    init_roles()
    init_login_methods()
    init_transfer_methods()
    init_card_types()

def init_accounts(app):
    acc = a.Account(username=app.username_adm01, password=app.password_adm01, role=RoleType.ADMIN.value)

    if "accounts" not in lst_collections:
        lstAccounts = [
            a.Account(username=app.username_usr01, password=app.password_usr01, role=RoleType.USER.value),
            a.Account(username=app.username_emp01, password=app.password_emp01, role=RoleType.EMPLOYEE.value),
            acc
        ]

        for account in lstAccounts:
            accounts.insert_one(account.to_json())
        return
    
    admin_account = accounts.find_one({"Role":RoleType.ADMIN.value, "Username":app.username_adm01})
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
    if "login_methods" not in lst_collections:
        lstMethods = [
            lm.LoginMethod(methodName="By Username with password", value=LoginType.NORMAL.value, createdBy=admin_id, modifiedBy=admin_id),
            lm.LoginMethod(methodName="By face identifier", value=LoginType.FACE_ID.value, createdBy=admin_id, modifiedBy=admin_id),
            lm.LoginMethod(methodName="By finger print", value=LoginType.FINGER_PRINT.value, createdBy=admin_id, modifiedBy=admin_id)
        ]

        for method in lstMethods:
            login_methods.insert_one(method.to_json())

def init_transfer_methods():
    if "transfer_methods" not in lst_collections:
        lstMethods = [
            tm.TransferMethod(methodName="SMS", value=TransferType.SMS.value, createdBy=admin_id, modifiedBy=admin_id),
            tm.TransferMethod(methodName="Face Identification", value=TransferType.FACE_ID.value, createdBy=admin_id, modifiedBy=admin_id),
            tm.TransferMethod(methodName="Pin code", value=TransferType.PIN_CODE.value, createdBy=admin_id, modifiedBy=admin_id)
        ]

        for method in lstMethods:
            transfer_methods.insert_one(method.to_json())

def init_card_types():
    if "card_types" not in lst_collections:
        lstTypes = [
            t.CardType(typeName="Credit Card", typeValue=CardType.CREDITS.value, createdBy=admin_id, modifiedBy=admin_id),
            t.CardType(typeName="Debit Card", typeValue=CardType.DEBITS.value, createdBy=admin_id, modifiedBy=admin_id),
        ]

        for type in lstTypes:
            card_types.insert_one(type.to_json())


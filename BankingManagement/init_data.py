from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

from models import database, account as a, role as r, login_method as lm
from models import transfer_method as tm, card_type as t
from models.branch import Branch
from models.loan import Loan
from enums.role_type import RoleType
from enums.login_type import LoginType
from enums.transfer_type import TransferType
from enums.card_type import CardType
from enums.collection import CollectionType

db = database.Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]
roles = db[CollectionType.ROLES.value]
login_methods = db[CollectionType.LOGIN_METHODS.value]
transfer_methods = db[CollectionType.TRANSFER_METHODS.value]
card_types = db[CollectionType.CARD_TYPES.value]
branches = db[CollectionType.BRANCHES.value]
loans = db[CollectionType.LOANS.value]

lst_collections = db.list_collection_names()

def initialize_data(app):
    init_accounts(app)
    init_branches()
    init_roles()
    init_login_methods()
    init_transfer_methods()
    init_card_types()
    init_loans()

def init_accounts(app):
    if CollectionType.ACCOUNTS.value not in lst_collections:
        lstAccounts = [
            a.Account(id=1, username=app.username_usr01, password=app.password_usr01, role=RoleType.USER.value),
            a.Account(id=2, username=app.username_emp01, password=app.password_emp01, role=RoleType.EMPLOYEE.value),
            a.Account(id=3, username=app.username_adm01, password=app.password_adm01, role=RoleType.ADMIN.value)
        ]

        for account in lstAccounts:
            accounts.insert_one(account.to_json())

def init_branches():
    admin = accounts.find_one({'Role': RoleType.ADMIN.value})
    admin_id = int(admin["_id"])

    if CollectionType.BRANCHES.value not in lst_collections:
        lst_branches = [
            Branch(id=1, branchName="Branch 1", address="So 01, duong Vo Van Ngan, phuong Linh Chieu, TP.Thu Duc, TP.HCM", createdBy=admin_id, modifiedBy=admin_id),
            Branch(id=2, branchName="Transaction Office 1", address="So 137, duong Pham Van Dong, phuong Linh Trung, TP.Thu Duc, TP.HCM", createdBy=admin_id, modifiedBy=admin_id)
        ]
        for branch in lst_branches:
            branches.insert_one(branch.to_json())

def init_roles():
    admin = accounts.find_one({'Role': RoleType.ADMIN.value})
    admin_id = int(admin["_id"])

    if CollectionType.ROLES.value not in lst_collections:
        lstRoles = [
            r.Role(id=1, roleName='User', value=RoleType.USER.value, createdBy=admin_id, modifiedBy=admin_id),
            r.Role(id=2, roleName='Employee', value=RoleType.EMPLOYEE.value, createdBy=admin_id, modifiedBy=admin_id),
            r.Role(id=3, roleName='Administrator', value=RoleType.ADMIN.value, createdBy=admin_id, modifiedBy=admin_id)
        ]

        for role in lstRoles:
            roles.insert_one(role.to_json())

def init_login_methods():
    admin = accounts.find_one({'Role': RoleType.ADMIN.value})
    admin_id = int(admin["_id"])

    if CollectionType.LOGIN_METHODS.value not in lst_collections:
        lstMethods = [
            lm.LoginMethod(id=1, methodName="By Username with password", value=LoginType.NORMAL.value, createdBy=admin_id, modifiedBy=admin_id),
            lm.LoginMethod(id=2, methodName="By face identifier", value=LoginType.FACE_ID.value, createdBy=admin_id, modifiedBy=admin_id),
            lm.LoginMethod(id=3, methodName="By finger print", value=LoginType.FINGER_PRINT.value, createdBy=admin_id, modifiedBy=admin_id)
        ]

        for method in lstMethods:
            login_methods.insert_one(method.to_json())

def init_transfer_methods():
    admin = accounts.find_one({'Role': RoleType.ADMIN.value})
    admin_id = int(admin["_id"])

    if CollectionType.TRANSFER_METHODS.value not in lst_collections:
        lstMethods = [
            tm.TransferMethod(id=1, methodName="SMS", value=TransferType.SMS.value, createdBy=admin_id, modifiedBy=admin_id),
            tm.TransferMethod(id=2, methodName="Face Identification", value=TransferType.FACE_ID.value, createdBy=admin_id, modifiedBy=admin_id),
            tm.TransferMethod(id=3, methodName="Pin code", value=TransferType.PIN_CODE.value, createdBy=admin_id, modifiedBy=admin_id)
        ]

        for method in lstMethods:
            transfer_methods.insert_one(method.to_json())

def init_card_types():
    admin = accounts.find_one({'Role': RoleType.ADMIN.value})
    admin_id = int(admin["_id"])

    if CollectionType.CARD_TYPES.value not in lst_collections:
        lstTypes = [
            t.CardType(id=1, typeName="Credit Card", typeValue=CardType.CREDITS.value, createdBy=admin_id, modifiedBy=admin_id),
            t.CardType(id=2, typeName="Debit Card", typeValue=CardType.DEBITS.value, createdBy=admin_id, modifiedBy=admin_id),
        ]

        for type in lstTypes:
            card_types.insert_one(type.to_json())

def init_loans():
    admin = accounts.find_one({'Role': RoleType.ADMIN.value})
    admin_id = int(admin["_id"])

    if CollectionType.LOANS.value not in lst_collections:
        lstLoans = [
            Loan(id=1, owner=4, term=6, amount=1000000, interest_rate=5, due_date=dt.now() + relativedelta(months=6), createdBy=admin_id, modifiedBy=admin_id),
            Loan(id=2, owner=4, term=12, amount=500000, interest_rate=8, due_date=dt.now() + relativedelta(months=12), createdBy=admin_id, modifiedBy=admin_id),
        ]

        for loan in lstLoans:
            loans.insert_one(loan.to_json())
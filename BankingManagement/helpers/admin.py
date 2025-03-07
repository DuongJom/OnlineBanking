from flask import session
import io
import pandas as pd

from enums.data_type import DataType
from enums.sex_type import SexType
from enums.role_type import RoleType
from enums.card_type import CardType
from enums.mime_type import MIMEType
from message import messages_success, messages_failure
from models import database, user as u, address, card, account as acc
from helpers.helpers import issue_new_card, generate_login_info, getMIMETypeValue

db = database.Database().get_db()
accounts = db['accounts']
users = db['users']
card_types = db['card_types']
branches = db['branches']
roles = db['roles']
addresses = db['addresses']
cards = db['cards']
employees = db['employee']
news = db['news']

def verify_input_data(row_index, **kwargs):
    for k, v in kwargs.items():
        if  not isinstance(v,str) or v == None:
            return {'status': "error", 'message': messages_failure["null_data"].format(k), "row_index": row_index}
        
    if accounts.find_one({"Username": kwargs["Username"]}) != None:
        return {'status': "error", 'message': messages_failure["username_existed"].format(kwargs["Username"]), "row_index": row_index}
    if users.find_one({"Email": kwargs["Email"]}) != None:
        return {'status': "error", 'message': messages_failure["email_existed"].format(kwargs["Email"]), "row_index": row_index}
    if users.find_one({"Phone": kwargs["Phone"]}) != None:
        return {'status': "error", 'message': messages_failure["phone_existed"].format(kwargs["Phone"]), "row_index": row_index}
    
    return {'status': "success", 'message': messages_success["create_success"].format(kwargs["Username"]), "row_index": row_index}

# data is a dictionary account data
def create_accounts(data):
    admin_id = session.get("account_id")
    total = len(data)
    counter = 0
    row_index = 1
    response_data = {"total": total, "logs": []}
    res = None

    for accData in data:
        # User info
        username = accData["Username"].strip()
        gender_text = accData["Gender"].strip()
        gender = None
        if gender_text.lower().strip() == "male":
            gender = SexType.MALE
        elif gender_text.lower().strip() == "female":
            gender = SexType.FEMALE
        else:
            gender = SexType.OTHER

        phone = str(accData["Phone"]).strip()
        email = accData["Email"].strip()

        #account info
        name = accData["Name"].strip()
        text_role = accData["Role"]
        branchName = accData["Branch"].strip()
        loginMethods = accData["Login Method"]
        transferMethods = accData["Transfer Method"]
        text_address = accData["Address"]
        new_address = None
        request_branch = None

        card_type = card_types.find_one({"TypeValue": CardType.CREDITS.value}, {"_id":0})
        card_info = issue_new_card()
        new_card = card.Card(cardNumber=card_info['cardNumber'], cvv=card_info['cvvNumber'], type=card_type, createdBy = admin_id)
        loginInfo = generate_login_info(email, phone)            

        roleValue = None

        if text_role.lower().strip() == "user":
            roleValue = RoleType.USER.value
        elif text_role.lower().strip() == "employee":
            roleValue = RoleType.EMPLOYEE.value
        elif text_role.lower().strip() == "admin":
            roleValue = RoleType.ADMIN.value
        else:
            roleValue = RoleType.USER

        mar = list(map(lambda x: x.strip(), text_address.split(',')))
        new_address = address.Address(street = mar[0], ward = mar[1], district = mar[2], city = mar[3], country = mar[4], createdBy = admin_id).to_json()
        res = verify_input_data(row_index , Username = username, Email = email, Phone = phone)

        if res["status"] == "success":
            counter += 1
            new_user = u.User(name = name, sex = gender, address = new_address, phone = phone, email = email, card = new_card.to_json(), createdBy = admin_id)
            new_account = acc.Account(accountNumber = card_info['accountNumber'], branch = request_branch, user = new_user.to_json(),
                                    username = username, password = loginInfo['Password'], role = roleValue,
                                    transferMethod = transferMethods, loginMethod = loginMethods, createdBy = admin_id)
            
            cards.insert_one(new_card.to_json())
            if new_address != None:
                addresses.insert_one(new_address)
            users.insert_one(new_user.to_json())
            accounts.insert_one(new_account.to_json())

        row_index += 1
        response_data["logs"].append(res)
        response_data.update({"success_create": counter})
    return response_data

def generate_export_data(dataType, file_type, filters):
    if dataType == DataType.ACCOUNT.value:
        collection = accounts
    elif dataType == DataType.USER.value:
        collection = users
    elif dataType == DataType.BRANCH.value:
        collection = branches
    elif dataType == DataType.EMPLOYEE.value:
        collection = employees
    elif dataType == DataType.NEWS.value:
        collection = news

    items = list(collection.find(filters))
    df = pd.json_normalize(items) 
    output = io.BytesIO()
    mime = None

    if file_type == str(MIMEType.CSV.value):
        df.to_csv(output, index=False, encoding='utf-8')
        output.seek(0) 
        mime = getMIMETypeValue(MIMEType.CSV)
    elif file_type == str(MIMEType.JSON.value):
        df = df.applymap(lambda x: x if isinstance(x, str) else str(x))
        df = df.applymap(lambda x: x.encode('utf-8', errors='replace').decode('utf-8'))
        df.to_json(output, index=False, force_ascii=False, orient='records', lines=True)
        output.seek(0)
        mime = getMIMETypeValue(MIMEType.JSON)
    elif file_type == str(MIMEType.EXCEL_XLSX.value):
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        mime = getMIMETypeValue(MIMEType.EXCEL_XLSX)

    return {'mime': mime, 'output': output}

def get_account(id):
    pipeline = [
        {
            "$match": {
                "_id": id
            }
        },
        # Join với collection login_methods cho LoginMethod
        {"$lookup": {
            "from": "login_methods",
            "localField": "LoginMethod",
            "foreignField": "_id",
            "as": "login_method_docs"
        }},
        # Join với collection transfer_methods cho TransferMethod
        {"$lookup": {
            "from": "transfer_methods",
            "localField": "TransferMethod",
            "foreignField": "_id",
            "as": "transfer_method_docs"
        }},
        # Join với collection users cho AccountOwner
        {"$lookup": {
            "from": "users",
            "localField": "AccountOwner",
            "foreignField": "_id",
            "as": "owner_doc"
        }},
        # Join với collection branches cho Branch
        {"$lookup": {
            "from": "branches",
            "localField": "Branch",
            "foreignField": "_id",
            "as": "branch_doc"
        }},
        # Join với collection roles cho Role
        {"$lookup": {
            "from": "roles",
            "localField": "Role",
            "foreignField": "_id",
            "as": "role_doc"
        }},
        
        # Project kết quả cần thiết
        {"$project": {
            "_id": 1,
            "Username": 1,
            "AccountNumber": 1,
            "Balance": 1,
            "Owner_name": {
                "$ifNull": [{"$arrayElemAt": ["$owner_doc.Name", 0]}, None]
            },

            "Branch_name": {
                "$ifNull": [{"$arrayElemAt": ["$branch_doc.BranchName", 0]}, None]
            },

            "Role_name": {
                "$ifNull": [{"$arrayElemAt": ["$role_doc.RoleName", 0]}, None]
            },

            "lst_login_method": {
                "$ifNull": [{
                    "$map": {
                        "input": "$login_method_docs",
                        "as": "method",
                        "in": "$$method.MethodName"
                    }
                }, []]
            },

            "lst_transfer_method": {
                "$ifNull": [{
                    "$map": {
                        "input": "$transfer_method_docs",
                        "as": "method",
                        "in": "$$method.MethodName"
                    }
                }, []]
            }
        }}
    ]
    account = dict(next(accounts.aggregate(pipeline)))
    return account
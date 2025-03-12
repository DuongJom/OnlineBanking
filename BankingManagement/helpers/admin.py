from flask import session
import io
import pandas as pd

from enums import card_type, data_type, mime_type, collection, role_type
from message import messages_success, messages_failure
from models import database, card as model_card, user, account
from helpers.helpers import issue_new_card, generate_login_info, getMIMETypeValue, get_max_id

db = database.Database().get_db()
accounts = db[collection.CollectionType.ACCOUNTS.value]
users = db[collection.CollectionType.USERS.value]
cards = db[collection.CollectionType.CARDS.value]
branches = db[collection.CollectionType.BRANCHES.value]
employees = db[collection.CollectionType.EMPLOYEES.value]
news = db[collection.CollectionType.NEWS.value]

def create_accounts(data):
    admin_id = session.get("account_id")
    total = len(data)
    counter = 0
    row_index = 1
    response_data = {"total": total, "logs": []}
    res = None

    for accData in data:
        fullname = accData["Fullname"]
        gender = int(accData["Gender"].split('.')[0])
        phone = str(accData["Phone"]).strip()
        email = accData["Email"].strip()
        branch = int(accData["Branch"].split('.')[0])
        address = accData["Address"]
        card_info = issue_new_card()
        login_info = generate_login_info(email, phone)     

        is_email_exits = True if users.find_one({"Email": email}) else False
        is_phone_exits = True if users.find_one({"Phone": phone}) else False
        is_error = False
        res = {'status': "success", 'message': messages_success["create_success"].format(login_info['Username']), "row_index": row_index}

        if is_email_exits:
            is_error = True
            res = {'status': "error", 'message': messages_failure["email_existed"].format(email), "row_index": row_index}
        if is_phone_exits:
            is_error = True
            res = {'status': "error", 'message': messages_failure["phone_existed"].format(phone), "row_index": row_index}

        if not is_error:
            new_card_id = get_max_id(database=db, collection_name=collection.CollectionType.CARDS.value)
            new_card = model_card.Card(
                id=new_card_id, 
                cardNumber=card_info['cardNumber'], 
                cvv=card_info['cvvNumber'], 
                type=card_type.CardType.CREDITS.value,
                createdBy = admin_id
            )

            new_user_id = get_max_id(database=db, collection_name=collection.CollectionType.USERS.value)
            new_user = user.User(
                id=new_user_id, 
                name=fullname, 
                sex=int(gender), 
                address=address.strip(), 
                phone=phone, 
                email=email, 
                card=[new_card_id,],
                createdBy = admin_id
            )

            new_account_id = get_max_id(database=db, collection_name=collection.CollectionType.ACCOUNTS.value)
            new_account = account.Account(
                id=new_account_id,
                accountNumber=card_info['accountNumber'], 
                branch=int(branch), 
                user=new_user_id, 
                username=login_info['Username'], 
                password=login_info['Password'], 
                role=role_type.RoleType.USER.value, 
                transferMethod=[1], 
                loginMethod=[1],
                createdBy = admin_id
            )

            cards.insert_one(new_card.to_json())
            users.insert_one(new_user.to_json())
            accounts.insert_one(new_account.to_json())

        row_index += 1
        response_data["logs"].append(res)
        response_data.update({"success_create": counter})
    return response_data

def generate_export_data(dataType, file_type, filters):
    if dataType == data_type.DataType.ACCOUNT.value:
        collection = accounts
    elif dataType == data_type.DataType.USER.value:
        collection = users
    elif dataType == data_type.DataType.BRANCH.value:
        collection = branches
    elif dataType == data_type.DataType.EMPLOYEE.value:
        collection = employees
    elif dataType == data_type.DataType.NEWS.value:
        collection = news

    items = list(collection.find(filters))
    df = pd.json_normalize(items) 
    output = io.BytesIO()
    mime = None

    if file_type == str(mime_type.MIMEType.CSV.value):
        df.to_csv(output, index=False, encoding='utf-8')
        output.seek(0) 
        mime = getMIMETypeValue(mime_type.MIMEType.CSV)
    elif file_type == str(mime_type.MIMEType.JSON.value):
        df = df.applymap(lambda x: x if isinstance(x, str) else str(x))
        df = df.applymap(lambda x: x.encode('utf-8', errors='replace').decode('utf-8'))
        df.to_json(output, index=False, force_ascii=False, orient='records', lines=True)
        output.seek(0)
        mime = getMIMETypeValue(mime_type.MIMEType.JSON)
    elif file_type == str(mime_type.MIMEType.EXCEL_XLSX.value):
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        mime = getMIMETypeValue(mime_type.MIMEType.EXCEL_XLSX)

    return {'mime': mime, 'output': output}

def get_account(id):
    pipeline = [
        {
            "$match": {
                "_id": id
            }
        },
        {"$lookup": {
            "from": "login_methods",
            "localField": "LoginMethod",
            "foreignField": "_id",
            "as": "login_method_docs"
        }},
        {"$lookup": {
            "from": "transfer_methods",
            "localField": "TransferMethod",
            "foreignField": "_id",
            "as": "transfer_method_docs"
        }},
        {"$lookup": {
            "from": "users",
            "localField": "AccountOwner",
            "foreignField": "_id",
            "as": "owner_doc"
        }},
        {"$lookup": {
            "from": "branches",
            "localField": "Branch",
            "foreignField": "_id",
            "as": "branch_doc"
        }},
        {"$lookup": {
            "from": "roles",
            "localField": "Role",
            "foreignField": "_id",
            "as": "role_doc"
        }},
        {"$project": {
            "_id": 1,
            "Username": 1,
            "AccountNumber": 1,
            "Balance": 1,
            "IsDeleted": 1,
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
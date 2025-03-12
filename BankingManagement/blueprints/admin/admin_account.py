from flask import Blueprint, request, jsonify, render_template, flash, redirect, session, url_for, send_file
import json
import pandas as pd
from io import BytesIO

from helpers.helpers import login_required, issue_new_card, get_max_id, generate_login_info, send_email, get_file_extension
from helpers.admin import get_account, create_accounts, generate_export_data
from models import database, card as model_card, user, account
from enums import deleted_type, collection, card_type, file_type, collection
from message import messages_success, messages_failure
from app import app, mail

admin_account_blueprint = Blueprint('admin_account', __name__)

db = database.Database().get_db()
accounts = db[collection.CollectionType.ACCOUNTS.value]
login_methods = db[collection.CollectionType.LOGIN_METHODS.value]
transfer_methods = db[collection.CollectionType.TRANSFER_METHODS.value]
users = db[collection.CollectionType.USERS.value]
branches = db[collection.CollectionType.BRANCHES.value]
roles = db[collection.CollectionType.ROLES.value]
cards = db[collection.CollectionType.CARDS.value]

@admin_account_blueprint.route('/admin/account/<int:page_no>', methods=['GET'])
@login_required
def admin_account(page_no):
    if request.method == 'GET':
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            criteria = json.loads(request.args.get('criteria'))
            for key, value in criteria.items():
                if isinstance(value, str) and value.isdigit(): 
                    criteria[key] = int(value)
                elif isinstance(value, (int, float)):  
                    criteria[key] = int(value)

            items_per_page = 10
            total_documents = accounts.count_documents({})
            total_pages = (total_documents + items_per_page - 1) // items_per_page
            
            pipeline = [
                {"$match": criteria},
                {"$skip": (page_no - 1) * items_per_page},
                {"$limit": items_per_page},

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
                    "Account_number": "$AccountNumber",
                    "Balance": "$Balance",
                    "Owner_ID": "$AccountOwner",
                    "Owner_name": {
                        "$ifNull": [{"$arrayElemAt": ["$owner_doc.Name", 0]}, None]
                    },
                    "Branch_ID": "$Branch",
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
            lst_results = [list(item.values()) for item in list(accounts.aggregate(pipeline))]
            return jsonify({'items': lst_results, 'total_pages': total_pages})
        return render_template('admin/account/account.html')
    
@admin_account_blueprint.route('/admin/account/view/<int:id>', methods=['GET'])
@login_required
def view_account(id):
    account = get_account(id)
    return render_template('admin/account/view_account.html', account = account, is_hidden=True)
    
@admin_account_blueprint.route('/admin/account/new', methods=['GET', 'POST'])
@login_required
def add_account():
    if request.method == "GET":
        lst_login_method = login_methods.find()
        lst_transfer_method = transfer_methods.find()
        lst_role = roles.find()
        lst_branch = branches.find()
        return render_template('admin/account/add_account.html', 
                               lst_transfer_method = lst_transfer_method,
                               lst_login_method = lst_login_method,
                               lst_role = lst_role,
                               lst_branch = lst_branch,
                               is_hidden=True)
    try:
        log_in_id = session.get("account_id")
        card_info = issue_new_card()
        country = request.form['country']
        city = request.form['city']
        distinct = request.form['district']
        ward = request.form['ward']
        street = request.form['street']
        address = f'{street}, {ward}, {distinct}, {city}, {country}'
        role = request.form['role']
        branch = request.form['branch']
        name = request.form.get('name')
        sex = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email') 
        transfer_method_ids = [int(id) for id in request.form.getlist('transferMethod') if id.isdigit()]
        phone = request.form['phone']
        login_method_ids = [int(id) for id in request.form.getlist('loginMethod') if id.isdigit()]
        email = request.form['email']

        error_message = None
        is_exist_email = True if users.find_one({"Email": email}) else False
        is_exist_phone = True if users.find_one({"Phone": phone}) else False
        
        if is_exist_email:
            error_message = messages_failure['email_existed'].format(email) 
        elif is_exist_phone:
            error_message = messages_failure['phone_existed'].format(phone)
            
        if error_message:
            flash(error_message, 'error')
            return redirect("/admin/account/new")
        
        new_card_id = get_max_id(database=db, collection_name=collection.CollectionType.CARDS.value)
        new_card = model_card.Card(
            id=new_card_id, 
            cardNumber=card_info['cardNumber'], 
            cvv=card_info['cvvNumber'], 
            type=card_type.CardType.CREDITS.value,
            createdBy = log_in_id
        )

        new_user_id = get_max_id(database=db, collection_name=collection.CollectionType.USERS.value)
        new_user = user.User(
            id=new_user_id, 
            name=name, 
            sex=int(sex), 
            address=address.strip(), 
            phone=phone, 
            email=email, 
            card=[new_card_id,],
            createdBy = log_in_id
        )

        login_info = generate_login_info(email, phone)
        new_account_id = get_max_id(database=db, collection_name=collection.CollectionType.ACCOUNTS.value)
        new_account = account.Account(
            id=new_account_id,
            accountNumber=card_info['accountNumber'], 
            branch=int(branch), 
            user=new_user_id, 
            username=login_info['Username'], 
            password=login_info['Password'], 
            role=int(role), 
            transferMethod=transfer_method_ids, 
            loginMethod=login_method_ids,
            createdBy = log_in_id
        )
        cards.insert_one(new_card.to_json())
        users.insert_one(new_user.to_json())
        accounts.insert_one(new_account.to_json())

        html = render_template('email/send_login_info.html', username = login_info['Username'], password = login_info['Password'])
        attachments = [{'path': './static/img/bank.png', 'filename':'bank.png', 'mime_type': 'image/png'}]
        subject = "Send login information"
        send_email(app=app, mail=mail, recipients=[email], subject=subject, html=html, attachments=attachments)
        flash(messages_success['register_success'].format(email), 'success')
    except Exception:
        flash(messages_failure['internal_error'], 'error')
    return redirect('/admin/account/new') 

@admin_account_blueprint.route('/admin/account/delete/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    try:
        account = accounts.find_one({"_id": id})
        current_page = request.form["current_page"]
        accounts.update_one(
            {'_id': id},
            {"$set": {"IsDeleted": deleted_type.DeletedType.DELETED.value}
        })      
        flash(messages_success['delete_success'].format(account["Username"]), 'success')  
    except Exception:
          flash(messages_failure['internal_error'], 'error')
          return redirect('/admin/account/1')
    return redirect(f'/admin/account/{current_page}')

@admin_account_blueprint.route('/admin/account/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_account(id):
    if request.method == "GET":
        lst_login_method = login_methods.find()
        lst_transfer_method = transfer_methods.find()
        lst_role = roles.find()
        lst_branch = branches.find()
        account = get_account(id)
        return render_template('admin/account/edit_account.html', 
                               account = account,
                               lst_branch = lst_branch,
                               lst_login_method = lst_login_method,
                               lst_transfer_method = lst_transfer_method,
                               lst_role = lst_role,
                               is_hidden=True)
    try:
        log_in_id = int(session.get("account_id"))
        new_role = int(request.form['role'])
        new_branch = int(request.form['branch'])
        lst_new_login_method = [int(method) for method in request.form.getlist('loginMethod')]
        lst_new_transfer_method = [int(method) for method in request.form.getlist('transferMethod')]
        new_status = int(request.form['status'])

        accounts.update_one(
            {'_id': id},
            {"$set": {
                "Role": new_role,
                "LoginMethod": lst_new_login_method,
                "TransferMethod": lst_new_transfer_method,
                "Branch": new_branch,
                "IsDeleted": new_status,
                "ModifiedBy": log_in_id
            }}
        )

        flash(messages_success["update_success"].format("Account"), 'success')
    except Exception:
        flash(messages_failure['internal_error'], 'error')
        return redirect(f'admin/account/edit/{id}')
    return redirect(url_for("admin_account.admin_account", page_no = 1))

@admin_account_blueprint.route('/admin/account/import', methods=['POST'])
@login_required
def import_data():
    file = request.files['file']
    ext = get_file_extension(file.filename)

    if ext == file_type.FileType.CSV.value:
        df = pd.read_csv(BytesIO(file.read()))
    elif ext == file_type.FileType.XLSX.value:
        df = pd.read_excel(BytesIO(file.read()), engine='openpyxl')     
         
    data = df.to_dict(orient='records')
    res = None
    res = create_accounts(data)
    return jsonify(res) 

@admin_account_blueprint.route('/admin/export_data/<dataType>', methods=['POST'])
@login_required
def export_data(dataType):
    filters = request.json.get('filter')
    file_type = request.json.get('file_type')
    data = generate_export_data(dataType=dataType, file_type=file_type, filters=filters)
    return send_file(data['output'], as_attachment=True, download_name="", mimetype=data['mime'])

            
    






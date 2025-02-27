from flask import Blueprint, request, jsonify, render_template, url_for
import json

from helpers.helpers import login_required
from models.database import Database

admin_account_blueprint = Blueprint('admin_account', __name__)

db = Database().get_db()
accounts = db['accounts']
login_methods = db['login_methods']
users = db['users']
branches = db['branches']
roles = db['roles']

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
                # Join với collection login_methods cho LoginMethod
                {"$lookup": {
                    "from": "login_methods",
                    "localField": "LoginMethod",
                    "foreignField": "_id",
                    "as": "login_method_docs"
                }},
                # Join với collection login_methods cho TransferMethod
                {"$lookup": {
                    "from": "login_methods",
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
                    "Username": 1,
                    "Account_number":"$AccountNumber",
                    "Balance": "$Balance",
                    "Owner_ID": "$AccountOwner",
                    "Owner_name": {"$arrayElemAt": ["$owner_doc.Name", 0]},
                    "Branch_ID": "$Branch",
                    "Branch_name": {"$arrayElemAt": ["$branch_doc.BranchName", 0]},
                    "Role_ID": "$Role",
                    "Role_name": {"$arrayElemAt": ["$role_doc.RoleName", 0]},
                    "lst_login_method": "$login_method_docs.MethodName",
                    "lst_transfer_method": "$transfer_method_docs.MethodName"
                }}
            ]
            results = list(accounts.aggregate(pipeline))
            return jsonify({'items': results, 'total_pages': total_pages})
        return render_template('admin/account/account.html')




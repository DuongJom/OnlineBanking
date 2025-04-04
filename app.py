from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/online_banking"
mongo = PyMongo(app)

# Loan payment route
@app.route('/user/loan')
def loan_page():
    # Get user ID from session (you should implement proper authentication)
    user_id = "user123"  # This should come from your authentication system
    
    # Get loan details from MongoDB
    loan = mongo.db.loans.find_one({"user_id": user_id})
    if not loan:
        loan = {
            "amount": 10000,
            "remaining_amount": 7500,
            "next_payment_date": "2024-04-01"
        }
    
    # Get payment history
    payments = list(mongo.db.payments.find(
        {"user_id": user_id, "type": "loan"},
        {"_id": 0, "date": 1, "amount": 1, "method": 1, "status": 1}
    ).sort("date", -1))
    
    return render_template('user/loan.html', loan=loan, payments=payments)

# API endpoint for processing loan payments
@app.route('/api/loan/payment', methods=['POST'])
def process_loan_payment():
    try:
        data = request.get_json()
        user_id = "user123"  # This should come from your authentication system
        
        # Validate payment data
        amount = float(data.get('amount', 0))
        payment_method = data.get('payment_method')
        payment_date = data.get('payment_date')
        
        if not all([amount, payment_method, payment_date]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Get loan details
        loan = mongo.db.loans.find_one({"user_id": user_id})
        if not loan:
            return jsonify({"error": "No active loan found"}), 404
        
        # Validate payment amount
        if amount <= 0:
            return jsonify({"error": "Invalid payment amount"}), 400
        
        if amount > loan['remaining_amount']:
            return jsonify({"error": "Payment amount exceeds remaining loan amount"}), 400
        
        # Create payment record
        payment = {
            "user_id": user_id,
            "type": "loan",
            "amount": amount,
            "method": payment_method,
            "date": payment_date,
            "status": "Completed",
            "created_at": datetime.utcnow()
        }
        
        # Save payment to database
        mongo.db.payments.insert_one(payment)
        
        # Update loan remaining amount
        new_remaining = loan['remaining_amount'] - amount
        mongo.db.loans.update_one(
            {"user_id": user_id},
            {"$set": {"remaining_amount": new_remaining}}
        )
        
        # If payment method should be saved
        if data.get('save_payment_method'):
            mongo.db.saved_payment_methods.update_one(
                {"user_id": user_id},
                {"$set": {"method": payment_method}},
                upsert=True
            )
        
        return jsonify({
            "message": "Payment processed successfully",
            "payment_id": str(payment['_id'])
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
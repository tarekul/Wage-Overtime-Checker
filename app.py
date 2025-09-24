from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to the Wage Overtime Checker!"

@app.route('/check-pay', methods=['POST'])
def check_pay():
    data = request.get_json()
    
    hours_worked = data.get("hoursWorked")
    hourly_rate = data.get("hourlyRate")
    total_pay_received = data.get("totalPayReceived")
    
    # Calculate pay
    regular_hours = min(hours_worked, 40)
    overtime_hours = max(hours_worked - 40, 0)
    overtime_pay = overtime_hours * hourly_rate * 1.5
    expected_total_pay = (regular_hours * hourly_rate) + overtime_pay
    
    if hours_worked <= 0 or hourly_rate <= 0 or total_pay_received < 0:
        return jsonify({"error": "Invalid input values"})
        
    
    if hourly_rate < 7.25:
        return jsonify({
            "expectedPay": None,
            "overtimeOwed": None,
            "underpayment": None,
            "message": "Your entered hourly rate ($6.50) is below the federal minimum wage of $7.25. This may be a violation of federal labor law."
        })

    
    difference = expected_total_pay - total_pay_received
    
    if difference > 0:  # Underpaid
        message = f"You may be missing ${difference:.2f}. Consider contacting your employer or labor board."
    elif difference < 0:  # Overpaid
        message = f"You appear to have been overpaid by ${abs(difference):.2f}. Double-check with your employer."
    else:  # Paid correctly
        message = "Your pay matches the expected amount. No discrepancies found."

    return jsonify({
        "expectedPay": expected_total_pay,
        "overtimeOwed": overtime_pay,
        "underpayment": difference if difference > 0 else 0,
        "message": message
    })

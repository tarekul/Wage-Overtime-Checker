import json
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
    state = data.get("state")
    
    with open("state_laws.json") as f:
        STATE_LAWS = json.load(f)
    
    if state not in STATE_LAWS:
        return jsonify({"error": "State not recognized"})

    laws = STATE_LAWS[state]
    
    if hours_worked is None or hourly_rate is None or total_pay_received is None or state is None:
        return jsonify({"error": "Missing required fields"}), 400

    if hours_worked <= 0 or hourly_rate <= 0 or total_pay_received < 0:
        return jsonify({"error": "Invalid input values"}), 400
    
    # Calculate pay
    regular_hours = min(hours_worked, 40)
    overtime_hours = max(hours_worked - 40, 0)
    
    if laws.get("daily_overtime_hours"):
        # Here you would also require daily hours input per day
        pass
    
    overtime_pay = overtime_hours * hourly_rate * laws["daily_overtime_multiplier"]
    expected_total_pay = (regular_hours * hourly_rate) + overtime_pay
    difference = expected_total_pay - total_pay_received
    
    if hourly_rate < laws["min_wage"]:
        return jsonify({
            "state": state,
            "expectedPay": None,
            "overtimeOwed": None,
            "underpayment": None,
            "message": f"Your hourly rate (${hourly_rate:.2f}) is below the minimum wage for {state} (${laws['min_wage']:.2f})."
        })

    if difference > 0:  # Underpaid
        message = f"You may be missing ${difference:.2f}. Consider contacting your employer or labor board."
    elif difference < 0:  # Overpaid
        message = f"You appear to have been overpaid by ${abs(difference):.2f}. Double-check with your employer."
    else:  # Paid correctly
        message = "Your pay matches the expected amount. No discrepancies found."

    return jsonify({
        "state": state,
        "expectedPay": expected_total_pay,
        "overtimeOwed": overtime_pay,
        "underpayment": difference if difference > 0 else 0,
        "message": message
    })

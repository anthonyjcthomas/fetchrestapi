from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

# Memory
transactions = []
balances = {}

def parse_timestamp(ts_str):
    return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)

@app.route('/add', methods=['POST'])
def add_points():
    data = request.get_json()
    payer = data.get("payer")
    points = data.get("points")
    timestamp_str = data.get("timestamp")

    if payer is None or points is None or timestamp_str is None:

        return "Bad Request: Missing required fields.", 400

    # Parse timestamp
    try:
        timestamp = parse_timestamp(timestamp_str)
    except ValueError:
        return "Bad Request: Invalid timestamp format.", 400

    if payer not in balances:
        balances[payer] = 0

    if points >= 0:
        # Positive transaction: just add it
        transaction = {

            "payer": payer,
            "points": points,
            "timestamp": timestamp,
            "remaining_points": points

        }
        transactions.append(transaction)
        transactions.sort(key=lambda x: x["timestamp"])
        balances[payer] += points
    else:
        # Negative transaction
        to_remove = -points  # how many points we need to take back
        # Sort by timestamp
        transactions.sort(key=lambda x: x["timestamp"])

        for txn in transactions:
            if txn["payer"] == payer and txn["remaining_points"] > 0 and to_remove > 0:
                available = txn["remaining_points"]
                remove_amount = min(available, to_remove)
                txn["remaining_points"] -= remove_amount
                to_remove -= remove_amount

        # Update the payer balance
        balances[payer] += points  # negative case, should reduce balance

    return "", 200

@app.route('/spend', methods=['POST'])
def spend_points():
    data = request.get_json()
    points_to_spend = data.get("points")

    if points_to_spend is None or points_to_spend <= 0:
        return "Bad Request: Invalid points to spend.", 400

    # Check total available points
    total_points = sum(balances.values())
    if points_to_spend > total_points:
        return "Not enough points to spend.", 400

    # Spend points in chronological order
    transactions.sort(key=lambda x: x["timestamp"])
    points_remaining = points_to_spend
    spending_result = {}

    for txn in transactions:
        if points_remaining == 0:
            break

        if txn["remaining_points"] > 0:
            spendable = min(txn["remaining_points"], points_remaining)
            txn["remaining_points"] -= spendable
            points_remaining -= spendable

            payer = txn["payer"]
            balances[payer] -= spendable

            if payer not in spending_result:
                spending_result[payer] = 0
            spending_result[payer] -= spendable

    response_list = [{"payer": p, "points": amt} for p, amt in spending_result.items()]
    return jsonify(response_list), 200

@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify(balances), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)

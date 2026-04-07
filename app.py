from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for our expenses
expenses = []
expense_id_counter = 1

@app.route('/', methods=['GET'])
def index():
    # A simple HTML UI so you have something to screenshot!
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expense Tracker</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; background: #f4f7f6; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            input, button { padding: 10px; margin: 5px 0; width: calc(100% - 22px); border-radius: 4px; border: 1px solid #ccc; }
            button { background: #28a745; color: white; border: none; cursor: pointer; }
            button:hover { background: #218838; }
            li { background: #eee; margin: 5px 0; padding: 10px; display: flex; justify-content: space-between; border-radius: 4px; }
            .delete-btn { background: #dc3545; width: auto; padding: 5px 10px; color: white; border-radius: 4px; border: none; cursor: pointer; }
            .delete-btn:hover { background: #c82333; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Personal Expense Tracker</h2>
            <input type="text" id="item" placeholder="Expense Item (e.g. Coffee)">
            <input type="number" id="amount" placeholder="Amount ($)">
            <button onclick="addExpense()">Add Expense</button>
            
            <h3>Recent Expenses</h3>
            <ul id="expenseList"></ul>
        </div>

        <script>
            async function loadExpenses() {
                const res = await fetch('/api/expenses');
                const data = await res.json();
                const list = document.getElementById('expenseList');
                list.innerHTML = '';
                data.forEach(exp => {
                    list.innerHTML += `<li>${exp.item} - $${exp.amount} 
                    <button class="delete-btn" onclick="deleteExpense(${exp.id})">X</button></li>`;
                });
            }

            async function addExpense() {
                const item = document.getElementById('item').value;
                const amount = document.getElementById('amount').value;
                if(!item || !amount) return alert("Fill all fields");
                
                await fetch('/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({item, amount})
                });
                document.getElementById('item').value = '';
                document.getElementById('amount').value = '';
                loadExpenses();
            }

            async function deleteExpense(id) {
                await fetch(`/delete/${id}`, { method: 'DELETE' });
                loadExpenses();
            }

            loadExpenses();
        </script>
    </body>
    </html>
    """
    return html

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    global expense_id_counter
    data = request.json
    new_expense = {"id": expense_id_counter, "item": data['item'], "amount": data['amount']}
    expenses.append(new_expense)
    expense_id_counter += 1
    return jsonify({"message": "Expense added successfully"}), 201

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_expense(id):
    global expenses
    # Filter out the expense with the matching ID
    expenses = [exp for exp in expenses if exp['id'] != id]
    return jsonify({"message": "Expense deleted successfully"}), 200

if __name__ == '__main__':
    # Running on 0.0.0.0 makes it accessible to Docker
    app.run(host='0.0.0.0', port=5000)

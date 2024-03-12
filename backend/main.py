from flask import Flask,request,jsonify,g,render_template
import sqlite3
app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'], defaults={'name':'gaurav'})
@app.route('/home/<name>', methods=['GET', 'POST'])
def hello(name):
    
    return '<h2>Hello {} for first time </h2>'.format(name)

@app.route('/login')
def login():
    return True

@app.route('/register')
def register():
    user_name = request.args.get('user_name')
    pass1 = request.args.get('pass1')
    pass2 = request.args.get('pass2')
    number = request.args.get('number')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    d = cursor.execute('''Select * from User_Register where Number = {};'''.format(number))
    data = d.fetchall()
    if len(data) != 0:
        return "<h1>Number already exists</h1>"
    
    elif pass1 == pass2:
        cursor.execute('''INSERT INTO User_Register(User_name, Password, Number) VALUES ({},{},{});'''.format(user_name,pass1,number))
        conn.commit() 
        return '<h1>Registration successful</h1>'

@app.route('/query')
def query():
    group_name = request.args.get('group_name')
    user_name = request.args.get('user_name')
    name = request.args.get('name')
    type = request.args.get('type')
    amount = request.args.get('amount')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Group_Expense(Group_name, User_name, Name, Type, Amount, Date_of_expense) VALUES ({},{},{},{},{},datetime('now'));'''.format(group_name,user_name,name,type,amount))
    conn.commit() 
    return '<h1>done</h1>'

@app.route('/display_group')
def display_group():
    group_name = request.args.get('group_name')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    datas = cursor.execute('SELECT * from Group_Expense where Group_name = {}'.format(group_name))
    data = datas.fetchall()
    l = []
    s = {}
    total_exp = 0
    output = {}
    for Group_name, User_name, Name, Type, Amount, Date_of_expense in data:
        s={}
        s['Group_name'] = Group_name
        s['User_name'] = User_name
        s['Name'] = Name
        s['Type'] = Type
        s['Amount'] = Amount
        s['Date_of_expense'] = Date_of_expense
        if Type in output:
            output[Type] = output[Type] + Amount
        else:
            output[Type] = Amount
        l.append(s)
        total_exp += Amount
    output["result"] = l
    output["Total_Expense"] = total_exp
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug = True)
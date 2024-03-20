from flask import Flask,request,jsonify,g,render_template,redirect, url_for, session
import sqlite3
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/home', methods=['GET', 'POST'], defaults={'name':'gaurav'})
# @app.route('/home/<name>', methods=['GET', 'POST'])
def hello(name):
    
    return '<h2>Hello {} for first time </h2>'.format(session["name"])

@app.route('/login')
def login():
    user_name = request.args.get('user_name')
    pass1 = request.args.get('pass1')
    
    conn = sqlite3.connect('database.db')
    
    cursor = conn.cursor()
    
    d = cursor.execute('''Select User_name from User_Register where User_name = {} and Password = {};'''.format(user_name, pass1))
    data = d.fetchall()
    print(len(data))
    if len(data) != 0:
        session["name"] = user_name
        return "Hello {} ".format(user_name)

    return "Nahi hai yaar to register kar"

@app.route('/register')
def register():
    user_name = request.args.get('user_name')
    pass1 = request.args.get('pass1')
    pass2 = request.args.get('pass2')
    number = request.args.get('number')
    email = request.args.get('email')
    forget_password = request.args.get('forget_password')
    conn = sqlite3.connect('database.db')
    print(forget_password)
    if str(forget_password) == "True":
        return redirect("/sample")
    cursor = conn.cursor()
    d = cursor.execute('''Select Number, email from User_Register where Number = {} or email = "{}";'''.format(number, email))
    data = d.fetchall()[0]
    if len(data) != 0:
        if str(data[0]) == str(number) and str(data[1]) == str(email):
            return "<h1>Number and Email already exists</h1>"
        
        elif str(data[0]) == str(number):
            return "<h1>Number already exists</h1>"
        
        else: 
            return "<h1>Email already exists</h1>"
        
    elif pass1 == pass2:
        cursor.execute('''INSERT INTO User_Register(User_name, Password, Number, email) VALUES ({},{},{},{});'''.format(user_name,pass1,number,email))
        conn.commit() 
        return '<h1>Registration successful</h1>'

@app.route('/sample')
def method_name():
    return "hi"
@app.route('/forget_password')
def forget_password():
    u_tick = request.args.get('u_tick')
    email = request.args.get('email')
    pass1 = request.args.get('pass1')
    pass2 = request.args.get('pass2')
    number = request.args.get('number')
    conn = sqlite3.connect('database.db')
    
    cursor = conn.cursor()
    if pass1 == pass2:
        if str(u_tick) == "True":
            cursor.execute('''UPDATE User_Register SET Password = {} WHERE email = {};'''.format(pass1, email))
            conn.commit() 
        else:
            cursor.execute('''UPDATE User_Register SET Password = {} WHERE Number = {};'''.format(pass1, number))
            conn.commit()
    else:
        return 'HI'
    
    return "Table_Updated"
        

@app.route('/query')
def query():
    group_name = request.args.get('group_name')
    user_name = request.args.get('user_name')
    name = request.args.get('name')
    type = request.args.get('type')
    amount = request.args.get('amount')
    forget_password = request.args.get('forget_password')
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
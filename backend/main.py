from flask import Flask,request,jsonify,g,render_template
import sqlite3
app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'], defaults={'name':'gaurav'})
@app.route('/home/<name>', methods=['GET', 'POST'])
def hello(name):
    
    return '<h2>Hello {} for first time </h2>'.format(name)

@app.route('/query')
def query():
    group_name = request.args.get('group_name')
    user_name = request.args.get('user_name')
    name = request.args.get('name')
    type = request.args.get('type')
    amount = request.args.get('amount')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    d = cursor.execute('''INSERT INTO Group_Expense(Group_name, User_name, Name, Type, Amount, Date_of_expense) VALUES ({},{},{},{},{},datetime('now'));'''.format(group_name,user_name,name,type,amount))
    conn.commit() 
    return '<h1>done</h1>'

@app.route('/display_group')
def display_group():
    group_name = request.args.get('group_name')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    datas = cursor.execute('SELECT * from Group_Expense where Group_name = {}'.format(group_name))
    data = datas.fetchall()[0]
    s ={}
    for i in range(len(data)):
       s[i] = data[i]
        
    return jsonify(s)

if __name__ == '__main__':
    app.run(debug = True)

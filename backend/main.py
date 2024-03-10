from flask import Flask,request,jsonify,g,render_template
import sqlite3
app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'], defaults={'name':'gaurav'})
@app.route('/home/<name>', methods=['GET', 'POST'])
def hello(name):
    return '<h2>Hello {} for first time </h2>'.format(name)

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>This is main page</h1>'


if __name__ == '__main__':
    app.run(debug = True)

import pymysql
# import hashlib
import datetime
import time
from flask import Flask, render_template, request, session, redirect, url_for
import Query_Utility as query
import pprint

print('hi')
app = Flask(__name__)
app.secret_key = "NK3K"
# conn = pymysql.connect(host= '127.0.0.1',
#                        user='Wendy',
#                        password = '12345',
#                        # port = 3307,
#                        db='Project',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)
conn = pymysql.connect(host= 'localhost',
                       user='root',
                       password = '',
                       port = 3306,
                       db='wendy\'s',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor
                       )

@app.route('/', methods = ["GET","POST"])
def public_view():
    d1, data_dic = query.public_view(conn)
    # pprint.pprint(data['arrival_city'])
    return render_template("index.html",
                           departure_city = d1['departure_city'],
                           arrival_city = d1['arrival_city'],
                           d = data_dic)

@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    pass

@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    pass

if __name__ =='__main__':
    app.run('127.0.0.1', 5000, debug = True)
import pymysql
# import hashlib
import datetime
import time
from flask import Flask, render_template, request, session, redirect, url_for
import Query_Utility as query
import pprint


app = Flask(__name__)
app.secret_key = "NK3K"
# conn = pymysql.connect(host= '127.0.0.1',
#                        user='Wendy',
#                        password = '12345',
#                        port = 3307,
#                        db='fly',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)

conn = pymysql.connect(host= 'localhost',
                       user='root',
                       password = '',
                       db='fly',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


@app.route('/', methods = ["GET","POST"])
def init_app():
    d = query.get_top5_number(conn)
    return render_template('graph_test.html', data_list=d)



if __name__ =='__main__':
    app.run()
import pymysql
# import hashlib
import datetime
import time
from flask import Flask, render_template, request, session, redirect, url_for
import Query_Utility as query
import pprint


app = Flask(__name__)
app.secret_key = "NK3K"
conn = pymysql.connect(host= '127.0.0.1',
                       user='Wendy',
                       password = '12345',
                       port = 3307,
                       db='fly',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)



@app.route('/', methods = ["GET","POST"])
def init_app():
    data_list = [['Page Vist', 'Students Tutorial'],
                 ['2012', 100000],
                 ['2013', 23000],
                 ['2014', 46000],
                 ['2015', 49000],
                 ['2016', 55000],
                 ['2017', 100000]]
    d = query.get_top5_number(conn)
    print(d)

    return render_template('graph_test.html', data_list=d)



if __name__ =='__main__':
    app.run()
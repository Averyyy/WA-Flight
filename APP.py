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
                       db='Project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods = ["GET","POST"])
def init_app():
    return render_template("index.html")

@app.route('/public_view', methods = ["GET","POST"])
def public_view():
    if request.method =='GET':
        data_dic = query.public_view(conn)
        locations = query.get_locations(conn)
        # pprint.pprint(data['arrival_city'])
        # print(request.form['from'])
        # print(data_dic)
        print(locations)
        return render_template("public_view.html",
                           departure_city = locations['departure_loc'],
                           arrival_city = locations['arrival_loc'],
                           d = data_dic)

    elif request.method == 'POST':
        locations = query.get_locations(conn)
        print(request.form['from'],
              request.form['to'],
              request.form['date'])
        html_get = {'from':request.form['from'],
                    'to':request.form['to'],
                    'dt':request.form['date']}

        print(request.form['from'])
        print(1, html_get)
        data_dic = query.filter_result(conn,html_get)
        return render_template("public_view.html",
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               d=data_dic)


@app.route('/search',methods = ['GET','POST'])
def ty():
    print('Hello world')
    return

@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():

    return render_template("signup.html")

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template("signin.html")

    elif request.method == "POST":
        session['username'] = request.form['username']
        session["password"] = request.form["password"]
        if not query.login_check(conn, session['username'], session["password"], 'customer'):
            error = 'Invalid Account Information, Please Check or Register.'
            return redirect(url_for('sign_in'), error=error)

@app.route("/sign_in/customer_home", methods=["POST", "GET"])
def customer_home():
    pass


@app.route("/sign_in/agent_home", methods=["POST", "GET"])
def agent_home():
    pass

@app.route("/sign_in/staff_home", methods=["POST", "GET"])
def staff_home():
    pass


# @app.route('/register/customer', methods=['GET', 'POST'])
# def signup_cus(identity):
#     error = ""
#     if request.method == "GET":
#         return render_template("signup.html", error=error)
#     elif request.method == "POST":
#         info = {"email": request.form.get("Email"),
#                 "password": request.form.get("psw"),
#                 "name": request.form.get("pre name"),
#
#                 "building_number": request.form.get("bui num"),
#                 "street": request.form.get("street"),
#                 "city": request.form.get("city"),
#                 "state": request.form.get("state"),
#                 "phone_number": request.form.get("pho num"),
#                 "passport_number": request.form.get("psp num"),
#                 "passport_expiration": request.form.get("psp exp"),
#                 "passport_country": request.form.get("psp cou"),
#                 "date_of_birth": request.form.get("DoB"),
#                 "booking_agent_id": request.form.get("booking_agent_id"),
#                 "airline_name": request.form.get("airline_name")
#                 }
#
#         valid, error = query.reg_validation(conn, info)
#         # when db find it is an invalid login
#         if not valid:
#             return render_template("signup.html", error=error)
#
#         db_utils.register_to_database(conn, info, identity)
#         session["logged_in"] = True
#         session["type"] = identity
#         session["email"] = info["email"]
#         if identity == "airline_staff":
#             session["airline"] = info["airline_name"]
#         return redirect(url_for("search_flight"))

@app.route('/register/booking_agent', methods=['GET', 'POST'])
def signup_ba(identity):
    info = {
        "email": request.form.get("username"),
        "password": request.form.get("password"),
        "name": request.form.get("name"),
    }
    


@app.route('/register/airline_staff', methods=['GET', 'POST'])
def signup_as(identity):

    info = {
        "email": request.form.get("username"),
        "password": request.form.get("password"),
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "date_of_birth": request.form.get("DoB"),
        "airline_name": request.form.get("airline_name")
    }








if __name__ =='__main__':
    app.run()
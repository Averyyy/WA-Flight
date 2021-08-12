import pymysql
from flask import Flask, render_template, request, session, redirect, url_for
import Query_Utility as query
# from werkzeug.security import generate_password_hash, check_password_hash


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

# Utility Functions
def save_to_session(dic):
    for key in dic.keys():
        session[key] = dic[key]
    return

@app.route('/', methods = ["GET","POST"])
def init_app():
    session.clear()
    return render_template("index.html")

@app.route('/public_view', methods = ["GET","POST"])
def public_view():
    if request.method =='GET':
        data_dic = query.public_view(conn)
        locations = query.get_locations(conn)
        return render_template("public_view.html",
                           departure_city = locations['departure_loc'],
                           arrival_city = locations['arrival_loc'],
                           d = data_dic)

    elif request.method == 'POST':
        locations = query.get_locations(conn)
        html_get = {'from':request.form['from'],
                    'to':request.form['to'],
                    'dt':request.form['date']}
        data_dic = query.filter_result(conn,html_get)
        return render_template("public_view.html",
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               d=data_dic)


# ====== sign up
@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method =='GET':
        return render_template("signup.html")
    if request.method == 'POST':
        info_cus = {
            "email": request.form.get("Email"),
            "password":  request.form.get("psw"),
            "name": request.form.get("pre name"),
            "building_number": request.form.get("bui num"),
            "street": request.form.get("street"),
            "city": request.form.get("city"),
            "state": request.form.get("state"),
            "phone_number": request.form.get("pho num"),
            "passport_number": request.form.get("psp num"),
            "passport_expiration": request.form.get("psp exp"),
            "passport_country": request.form.get("psp cou"),
            "date_of_birth": request.form.get("DoB"),
        }
        info_ba = {
            "email": request.form.get("ba_email"),
            "password": request.form.get("ba_psw"),
            "booking_agent_id": request.form.get("ba_id")
        }
        info_as = {
            "email": request.form.get("as_uname"),
            "password": request.form.get("as_psw"),
            "first_name": request.form.get("as_first_name"),
            "last_name": request.form.get("as_last_name"),
            "date_of_birth": request.form.get("asDoB"),
            "airline_name": request.form.get("as_airline")
        }
        if query.check_full(info_cus):
            save_to_session(info_cus)
            return redirect(url_for("signup_cus"))
        elif query.check_full(info_ba):
            save_to_session(info_ba)
            return redirect(url_for("signup_ba"))
        elif query.check_full(info_as):
            save_to_session(info_as)
        return redirect(url_for("signup_as"))


@app.route('/sign_up/customer', methods=['GET', 'POST'])
def signup_cus():
    valid, err = query.reg_validation_cus(conn, session)
    if valid:
        session['signin'] = True
        session["user_type"] = 'customer'
        query.add_cus(conn, session)
        return redirect(url_for("customer_home"))
    else:
        return render_template('signup.html', error=err)


@app.route('/sign_up/booking_agent', methods=['POST', 'GET'])
def signup_ba():
    # Pass the session input information from html to the backend to check whether the address is already in use.
    valid, err = query.reg_validation_ba(conn, session)
    if valid:
        session['signin'] = True
        session["user_type"] = 'booking_agent'
        query.add_ba(conn, session)
        return redirect(url_for("agent_home"))
    else:
        return render_template('signup.html', error=err)


@app.route('/sign_up/airline_staff', methods=['GET', 'POST'])
def signup_as():
    valid, err = query.reg_validation_as(conn, session)
    if valid:
        query.add_as(conn, session)
        session['signin'] = True
        session["user_type"] = 'airline_staff'
        return redirect(url_for("staff_home"))
    else:
        return render_template('signup.html', error=err)



@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():

    if request.method =='GET':
        error = session.get('error')
        airlines = query.get_airlines(conn)
        return render_template("signin.html",
                               airlines = airlines, error = error)
    if request.method == 'POST':
        info_cus = {
            "email": request.form.get("uname"),
            "password": request.form.get("psw"),
        }
        info_ba = {
            "email": request.form.get("ba_uname"),
            "password": request.form.get("ba_psw"),
        }
        info_as = {
            "email": request.form.get("as_uname"),
            "password": request.form.get("as_psw"),
            "airline_name": request.form.get("airline_name")
        }
        if query.check_full(info_cus):
            save_to_session(info_cus)
            return redirect(url_for("customer_home"))
        elif query.check_full(info_ba):
            save_to_session(info_ba)
            return redirect(url_for("agent_home"))
        elif query.check_full(info_as):
            save_to_session(info_as)
            return redirect(url_for("staff_home"))

@app.route("/sign_in/customer_home", methods=["POST", "GET"])
def customer_home():
    session['signin'] = query.sign_in_check(conn, session['email'],session["password"], 'customer','')
    session["user_type"] = 'customer'
    print(session.get('user_type'))
    locations = query.get_locations(conn)
    d = query.get_top5_number(conn)
    if not session["signin"] and request.method == 'GET':
        session["error"] = 'Invalid username or password, please try again.'
        return redirect(url_for("sign_in"))
    elif session["signin"] and request.method == "GET":
        data_dic = query.public_view(conn)
        purchased_flight = query.get_purchased_flight(conn, session)
        return render_template('homepage_customer.html',
                               # same results as
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased = purchased_flight,
                               airlines = query.get_airlines(conn),
                               flight_num = query.get_flight_num(conn),
                               data_list = d)
                               # spent = query.get_spent(query.get_past_year_period())))
    elif request.method =='POST':
        html_get = {'from': request.form.get('from'),
                    'to': request.form.get('to'),
                    'dt': request.form.get('date'),
                    'flight_num':request.form.get("flight_num")}
        data_dic = query.filter_result(conn, html_get)
        purchased_flight = query.get_purchased_flight(conn, session)

        flight_num = html_get["flight_num"]
        if flight_num == '':
            return render_template('homepage_customer.html',
                               # same results as
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased = purchased_flight,
                               airlines = query.get_airlines(conn),
                               flight_num = query.get_flight_num(conn),
                               data_list = d)
        else:
            success,err = query.purchase(conn, flight_num, session['email'], 'NULL')
            if success:
                return redirect(url_for("customer_home"))
            else:
                return redirect(url_for("customer_home"))


@app.route("/sign_in/agent_home", methods=["POST", "GET"])
def agent_home():
    session['signin'] = query.sign_in_check(conn, session['email'],session["password"], 'booking_agent','')
    session["user_type"] = 'booking_agent'
    da = query.get_top_customer_number(conn,session)
    print('datalist: ', da)
    locations = query.get_locations(conn)
    total_month = query.view_commission_month(conn, session)[0]
    avg_month = query.view_commission_month(conn, session)[1]
    total_year = query.view_commission_month(conn, session)[2]
    avg_year = query.view_commission_month(conn, session)[3]
    if not session["signin"] and request.method == 'GET':
        session["error"] = 'Invalid username or password, please try again.'
        return redirect(url_for("sign_in"))
    elif session["signin"] and request.method == "GET":
        data_dic = query.public_view(conn)
        locations = query.get_locations(conn)
        purchased_flight = query.get_purchased_flight(conn, session)
        return render_template('homepage_booking_agent.html',
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased=purchased_flight,
                               total_month = total_month,
                               avg_month = avg_month,
                               total_year= total_year,
                               avg_year=avg_year,
                               date_list1 = da)

    elif request.method == 'POST':
        html_get = {'from': request.form.get('from'),
                    'to': request.form.get('to'),
                    'dt': request.form.get('date'),
                    'customer_email': request.form.get('customer_email'),
                    'flight_num': request.form.get("flight_num")
                    }
        data_dic = query.filter_result(conn, html_get)
        purchased_flight = query.get_purchased_flight(conn, session)
        flight_num = html_get["flight_num"]
        if flight_num == '':
            return render_template('homepage_customer.html',
                                   # same results as
                                   departure_city=locations['departure_loc'],
                                   arrival_city=locations['arrival_loc'],
                                   all=data_dic,
                                   purchased=purchased_flight,
                                   flight_num=query.get_flight_num(conn),
                                   total_month=total_month,
                                   avg_month=avg_month)
        else:
            if html_get['customer_email'] is None or html_get['customer_email'] == '':
                success, err = False, 'Please enter both flight num and the customer email.'
                print('executing if_clause')
            else:
                print('executing else_clause')
                print(html_get['customer_email'])
                success, err = query.purchase(conn, flight_num, html_get['customer_email'], session['email'])
            if success:
                return redirect(url_for("agent_home"))
            else:
                return redirect(url_for("agent_home"))


@app.route("/sign_in/staff_home", methods=["POST", "GET"])
def staff_home():
    session['signin'] = query.sign_in_check(conn, session['email'],session["password"], 'booking_agent',session['airline_name'])
    session["user_type"] = 'airline_staff'
    session['signin'] = query.sign_in_check(conn, session['email'],session["password"], 'airline_staff',session['airline_name'])
    if not session["signin"] and request.method == 'GET':
        session["error"] = 'Invalid username or password, please try again.'
        return redirect(url_for("sign_in"))
    elif session["signin"] and request.method == "GET":
        data_dic = query.public_view(conn)
        locations = query.get_locations(conn)
        purchased_flight = query.get_purchased_flight(conn, session)
        return render_template("homepage_staff.html",
                               departure_city=locations['departure_loc'],
                               arrival_city=locations['arrival_loc'],
                               all=data_dic,
                               purchased=purchased_flight,
                               error = session.get('createflighterror')
                               )
    elif session["signin"] and request.method == "POST":
        create_para = {
            'flight_num': request.form.get("flight_c"),
            'price': request.form.get('price'),
            'departure_time': request.form.get("depdate"),
            'arrival_time': request.form.get('arrdate'),
            'departure': request.form.get('depplace'),
            'arrival': request.form.get('arrplace'),
            'plane': request.form.get('plane'),
            'status': request.form.get("status"),
            'planeid': request.form.get("planeid"),
            'seats' : request.form.get('seats')
        }

        if create_para['price']:
            if query.create_flight(conn, session, create_para['flight_num'], create_para["price"], create_para["departure_time"],create_para['arrival_time'],create_para['departure'][-3:], create_para['arrival'][-3:], create_para['plane']):
                return redirect(url_for('staff_home'))
            else:
                session['createflighterror'] = 'Create Flight failed'

        if create_para["status"]:
            if query.change_flight_status(conn, create_para['flight_num'], create_para["status"]):
                return redirect(url_for('staff_home'))
            else:
                session["createflighterror"] = 'Update Status failed'

        if create_para["seats"]:
            if query.add_airplane(conn,session, create_para["planeid"], create_para["seats"]):
                session['createflighterror'] = 'Add airplane'
            else:
                session["createflighterror"] = 'Update Status failed'
        return redirect(url_for("staff_home"))


@app.route("/sign_out", methods = ['POST','GET'])
def sign_out():
    if request.method == 'GET':
        session.clear()
        return render_template('sign_out.html')



if __name__ =='__main__':
    app.run()
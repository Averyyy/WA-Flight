import pymysql
# import hashlib
import datetime
import time
from flask import Flask, render_template, request, session, redirect, url_for
import pprint
import random

from werkzeug.security import generate_password_hash, check_password_hash

PASSWORD_HASH = 'md5'
# ===========================================================================================
#public view

# =================================

dic_airport_city = {"HKG":"Hongkong",
                    "MBC":"Mars Orbit",
                    "PEK":"Beijing",
                    "PVG":"Shanghai",
                    "TYO":"Tokyo"}

def airport_city(airport):
    return dic_airport_city[airport]

def remove_duplicate(lis):
    return list(set(lis))
# =================================
# the options for searching filter
def get_locations(conn):
    # Fetch all the data
    cursor = conn.cursor()
    query = "select * from flight"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    d_dic = {
        'departure_airport': [],
        'arrival_airport': [],
        'departure_loc':[],
        'arrival_loc':[]
    }

    for i in range(len(data)):
        d_dic['departure_airport'].append(str(data[i]['departure_airport']))
        d_dic['arrival_airport'].append(str(data[i]['arrival_airport']))

    print(d_dic)

    # get rid of all the duplicate elements
    d_dic['departure_airport'] = remove_duplicate(d_dic['departure_airport'])
    d_dic['arrival_airport'] = remove_duplicate(d_dic['arrival_airport'])

    # mapping back the airport to the city
    for i in d_dic['departure_airport']:
        d_dic['departure_loc'].append("%s | %s" % (airport_city(i), i))

    for i in d_dic['arrival_airport']:
        d_dic['arrival_loc'].append("%s | %s" % (airport_city(i), i))


    return d_dic

def get_airlines(conn):
    cursor = conn.cursor()
    query = "select * from airline"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    airlines = []
    for i in range(len(data)):
        airlines.append(str(data[i]['airline_name']))
    return airlines

def get_flight_num(conn):
    cursor = conn.cursor()
    query = "select distinct flight_num from flight where status = \'upcoming\'"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    flight_num= []
    for i in range(len(data)):
        flight_num.append(str(data[i]['flight_num']))
    return flight_num

# ======== Start of purchase function

def existing_ticket_id(conn):
    cursor = conn.cursor()
    query = "select ticket_id from ticket"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    ticket_id = []
    for i in range(len(data)):
        ticket_id.append(str(data[i]['ticket_id']))
    print('check existing_ticket_id excecuted, ticket_id list: ', ticket_id)
    return ticket_id


# ticket_id generator
def random_ticket_id(conn):
    seed1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seed2 = '1234567890'
    ticket_id = ''
    for i in range(2):
        ticket_id +=random.choice(seed1)
    for k in range(3):
        ticket_id += random.choice(seed2)
    #   logic check to see if ticket_id already exists
    if ticket_id not in existing_ticket_id(conn):
        print('generated random ticket id:', ticket_id)
        return ticket_id
    else:
        random_ticket_id(conn)

def get_airline(conn, flight_num):
    cursor = conn.cursor()
    query = "select airline_name from flight where flight_num =\'%s\'"%flight_num
    cursor.execute(query)
    airline = cursor.fetchall()[0]['airline_name']
    cursor.close()
    print('airline got is:', airline)
    return airline


def purchase(conn, flight_num, customer_email, booking_agent_email = 'NULL'):
    success, err = False, ''
    # TODO!!! check whether the selected flight is full


    # insert data into ticket （ticket_id, airline_name, flight_num）
    cursor = conn.cursor()
    ticket_id = random_ticket_id(conn)
    airline_name = get_airline(conn, flight_num)
    query = 'insert into ticket values' \
            '(\'%s\',\'%s\',\'%s\')' % (ticket_id,airline_name, flight_num)
    print(query)
    cursor.execute(query)
    conn.commit()
    cursor.close()

    # insert data into purchases (ticket_id, customer_email, booking_agent_email, purchase date)
    cursor = conn.cursor()
    year, month, day = getting_date()
    purchase_date = formatting_date(year, month, day)
    print('formatted date',purchase_date)
    if booking_agent_email != 'Null':
        query = 'insert into purchases values' \
            '(\'%s\',\'%s\',\'%s\',\'%s\')' % (ticket_id, customer_email, booking_agent_email,purchase_date)
    else:
        query = 'insert into purchases values' \
                '(\'%s\',\'%s\',%s,\'%s\')' % (ticket_id, customer_email, booking_agent_email, purchase_date)
    print(query)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    success = True
    print(success, err)
    return success, err

# ======== Start of day time formatting fuction
def getting_date():
    now = str(datetime.datetime.now()).split()[0]
    temp = now.split('-')
    date = temp[2]
    month = temp[1]
    year = temp[0]
    return year,month,date
    '''noted that the return is str type not int type!'''

def formatting_date(year,month,date):
    str = '%s-%s-%s'%(year,month,date)
    return str

def getting_period(day):
    print(type(day))
    start = '%s 00:00:00'%str(day)
    end = '%s 23:59:59'%str(day)
    return start, end

def getting_past_month_period(year,month,day):
    start = '%s 00:00:00'%(formatting_date(year,str(int(month)-1),str(int(day)+1)))
    end = '%s 23:59:59'%(formatting_date(year,month,day))
    return start, end
# print(getting_past_month_period('2021','8','10'))

def getting_past_year_period(year,month,day):
    start = '%s 00:00:00'%(formatting_date(str(int(month)-1),month,day))
    end = '%s 23:59:59'%(formatting_date(year,month,day))
    return start, end
# print(getting_past_year_period(getting_date()))

# ======== End of day time formatting fuction
# the options for searching filter
# NOT IN USE
# def get_departure_time():
#     d_dic = {
#         'departure_time': [],
#         'arrival_time': []
#     }
#
#     for i in range(len(data)):
#         d_dic['departure_time'].append(str(data[i]['departure_time']))
#         d_dic['arrival_time'].append(str(data[i]['arrival_time']))
#
#     # get rid of all the duplicate elements
#     d_dic['departure_time'] = remove_duplicate(d_dic['CHANGE'])
#     d_dic['arrival_time'] = remove_duplicate(d_dic['CHANGE'])



def public_view(conn):
    # From query fetch all
    cursor=conn.cursor()
    query = "select * from flight where status = \'upcoming\'"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    for i in data:
        i['Departure']= "%s | %s" % (airport_city(i['departure_airport']),i['departure_airport'])
        i['Arrival']= "%s | %s" % (airport_city(i['arrival_airport']),i['arrival_airport'])
    return data

def filter_result(conn,html_get):
    query = "select * from flight where"
    if html_get['from'] and html_get['from'] != None:
        html_get['departure_airport'] = html_get['from'].split('|')[1].strip()
        query += ' status = \'upcoming\' and %s = \'%s\''% ('departure_airport', html_get['departure_airport'])
    if html_get['to'] and html_get['to'] != None:
        html_get['arrival_airport'] = html_get['to'].split('|')[1].strip()
        query += ' and %s =\'%s\'' % ('arrival_airport', html_get['arrival_airport'])
    if html_get['dt'] != '' and html_get['dt'] != None :
        print(html_get['dt'])
        start, end = getting_period(html_get['dt'])
        print(start, end)
        query += ' and %s between \'%s\' and \'%s\'' % ('departure_time', start, end)
    if (html_get['from'] == '' or html_get['from'] is None) and (html_get['to']== '' or html_get['to'] is None) and (html_get['dt']== '' or html_get['dt'] is None):
        query += ' status = \'upcoming\''
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    for i in data:
        i['Departure']= "%s | %s" % (airport_city(i['departure_airport']),i['departure_airport'])
        i['Arrival']= "%s | %s" % (airport_city(i['arrival_airport']),i['arrival_airport'])
    return data

def get_purchased_flight(conn,session):
    cursor = conn.cursor()
    query ='select * from flight where flight_num in (select flight_num from ticket, purchases ' \
           'where ticket.ticket_id = purchases.ticket_id and %s = \'%s\')'
    if session["user_type"] == 'customer':
        query = query%('customer_email', session['email'])
    if session["user_type"] == 'booking_agent':
        query = query % ('booking_agent_email', session['email'])
    if session["user_type"] == 'airline_staff':
        query = 'select * from flight where flight_num in (select flight_num from ticket where airline_name = \'%s\')'%(session["airline_name"])
    print(query)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    for i in data:
        i['Departure'] = "%s | %s" % (airport_city(i['departure_airport']), i['departure_airport'])
        i['Arrival'] = "%s | %s" % (airport_city(i['arrival_airport']), i['arrival_airport'])
    return data

# ===========================================================================================
#sign in
def sign_in_check(conn, username, password,role, airline_name):
    cursor = conn.cursor()
    # username = username.replace('\'', '\\\'')
    query = """SELECT password FROM %s WHERE """ % role
    if role == "airline_staff":
        query += """username = \'%s\'""" % username
        query += """ AND airline_name = \'%s\' """ %airline_name
    else:
        query += """email = \'%s\'""" % username
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    if not data:
        return False
    # return check_password_hash(data[0][0], password)
    return data[0]['password'] == password

# ======== Sign up
# sign up validation check
def reg_validation_cus(conn,session):
    query = 'select * from customer ' \
            'where email = \'%s\' ' \
            'and password = \'%s\' '  % (session['email'], session['password'])
    print(query)

    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)
    cursor.close()
    if data:
        return False, 'Email already in use.'
    return True, ''

def reg_validation_ba(conn,session):
    query = 'select * from booking_agent ' \
            'where email = \'%s\' ' \
            'and password = \'%s\' ' \
            'and booking_agent_id = \'%s\''%(session['email'],session['password'],session['booking_agent_id'])
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)
    cursor.close()
    if data:
        return  False,'Email already in use.'
    return True, ''

def reg_validation_as(conn,session):
    query = 'select * from airline_staff ' \
            'where username = \'%s\' ' \
            'and password = \'%s\' '% (session['username'], session['password'])
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    if data:
        return False, 'Already registered.'
    return True, ''

# inserting data into database
def add_cus(conn, session):
    # set a query
    query = 'insert into customer values' \
            '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (session['email'], session['name'],
                                                             session['password'], session['building_number'],
                                                             session['street'], session['city'],
                                                            session['state'], session['phone_number'],
                                                            session['passport_number'], session['passport_expiration'],
                                                            session['passport_country'], session['date_of_birth'])

    # use cursor to insert data
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return

def add_ba(conn, session):
    query = 'insert into booking_agent values' \
            '(\'%s\',\'%s\',\'%s\')'%(session['email'],session['password'],session['booking_agent_id'])
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return

def add_as(conn, session):
    query = 'insert into airline_staff values' \
            '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(session['username'],session['password'],
                                                            session['first_name'],session['last_name'],
                                                            session['date_of_birth'],session['airline_name'],)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return

# ======== End of sign up

# Start of Homepage utility function

# customer


# agent
def view_commission_month(conn, session):
    # print(getting_past_month_period(getting_date()[0],getting_date()[1],getting_date()[2])[0],  getting_past_month_period(getting_date()[0],getting_date()[1],getting_date()[2])[1])
    query = 'SELECT SUM(flight.price)*0.1 as total, SUM(flight.price)*0.1/COUNT(purchases.ticket_id) as avg, COUNT(purchases.ticket_id) AS num '\
            'FROM flight, ticket, purchases '\
            'WHERE flight.flight_num = ticket.flight_num AND purchases.ticket_id = ticket.ticket_id '\
            'AND ticket.ticket_id in (select ticket_id '\
            'from purchases '\
            'where booking_agent_email = \'%s\' '\
            'and purchase_date between \'%s\' and \'%s\');'%(session["email"],  getting_past_month_period(getting_date()[0],getting_date()[1],getting_date()[2])[0],  getting_past_month_period(getting_date()[0],getting_date()[1],getting_date()[2])[1])
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    total = data[0]['total']
    avg = data[0]['avg']
    print(total, avg)
    return total, avg


# staff
def get_top5_number(conn):
    # need to insert time constrain using utility function
    query = 'select booking_agent_email, count(*) as ct from purchases ' \
            'where booking_agent_email is not null ' \
            'group by booking_agent_email ' \
            'order by ct DESC limit 5;'
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    data_list = [['Booking Agent','# Purchased']]
    for i in range(len(data)):
        data_list.append([data[i]['booking_agent_email'],data[i]['ct']])
    cursor.close()
    print(data_list)
    return data_list



# End of homepage utility function
def check_full(dic):
    for key in dic.keys():
        print(key, dic[key])
        if dic[key] == '' or dic[key]== None:
            return False
    return True
import pymysql
# import hashlib
import datetime
import time
from flask import Flask, render_template, request, session, redirect, url_for
import pprint

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

# the options for searching filter
# NOT IN USE
def get_departure_time():
    d_dic = {
        'departure_time': [],
        'arrival_time': []
    }

    for i in range(len(data)):
        d_dic['departure_time'].append(str(data[i]['departure_time']))
        d_dic['arrival_time'].append(str(data[i]['arrival_time']))

    # get rid of all the duplicate elements
    d_dic['departure_time'] = remove_duplicate(d_dic['CHANGE'])
    d_dic['arrival_time'] = remove_duplicate(d_dic['CHANGE'])



def public_view(conn):
    # From query fetch all
    cursor=conn.cursor()
    query = "select * from flight"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    for i in data:
        i['Departure']= "%s | %s" % (airport_city(i['departure_airport']),i['departure_airport'])
        i['Arrival']= "%s | %s" % (airport_city(i['arrival_airport']),i['arrival_airport'])
    return data

def filter_result(conn,html_get):
    # html_get is a list from user filter input, it can have multiple results or it can be empty
    # in the Flask html_get = {'from':request.form['from'],
    #                     'to':request.form['to'],
    #                     'dt':request.form['departure']} -- Shanghai | PVG
    query = "select * from flight where"
    if html_get['from']:
        html_get['departure_airport'] = html_get['from'].split('|')[1].strip()
        query += ' %s = \'%s\' '% ('departure_airport', html_get['departure_airport'])
    if html_get['to']:
        html_get['arrival_airport'] = html_get['to'].split('|')[1].strip()
        query += 'and %s =\'%s\' ' % ('arrival_airport', html_get['arrival_airport'])
    if html_get['dt'] != '':
        query += 'and %s = \'%s\'' % ('dt', html_get['dt'])
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    for i in data:
        i['Departure']= "%s | %s" % (airport_city(i['departure_airport']),i['departure_airport'])
        i['Arrival']= "%s | %s" % (airport_city(i['arrival_airport']),i['arrival_airport'])
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


def check_full(dic):
    for key in dic.keys():
        print(key, dic[key])
        if dic[key] == '' or dic[key]== None:
            return False
    return True
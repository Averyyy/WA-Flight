import pymysql
# import hashlib
import datetime
import time
from flask import Flask, render_template, request, session, redirect, url_for
import pprint
# =================================
dic_airport_city = {"PVG":"Shanghai",
                    "PEK":"Beijing",
                    "CAN":"Guangzhou",
                    "SZX":"Shenzhen",
                    "NRT":"Tokyo",
                    "JFK":"New York",
                    "LHR":"London"}

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
        d_dic['departure_airport'].append(str(data[i]['departure_name']))
        d_dic['arrival_airport'].append(str(data[i]['arrival_name']))

    # get rid of all the duplicate elements
    d_dic['departure_airport'] = remove_duplicate(d_dic['departure_airport'])
    d_dic['arrival_airport'] = remove_duplicate(d_dic['arrival_airport'])

    # mapping back the airport to the city
    for i in d_dic['departure_airport']:
        d_dic['departure_loc'].append("%s | %s" % (airport_city(i), i))

    for i in d_dic['arrival_airport']:
        d_dic['arrival_loc'].append("%s | %s" % (airport_city(i), i))

    return d_dic

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
        i['Departure']= "%s | %s" % (airport_city(i['departure_name']),i['departure_name'])
        i['Arrival']= "%s | %s" % (airport_city(i['arrival_name']),i['arrival_name'])
    return data

def filter_result(conn,html_get):
    # html_get is a list from user filter input, it can have multiple results or it can be empty
    # in the Flask html_get = {'from':request.form['from'],
    #                     'to':request.form['to'],
    #                     'dt':request.form['departure']} -- Shanghai | PVG
    query = "select * from flight where"
    if html_get['from']:
        html_get['departure_name'] = html_get['from'].split('|')[1].strip()
        query += ' %s = \'%s\' '% ('departure_name', html_get['departure_name'])
    if html_get['to']:
        html_get['arrival_name'] = html_get['to'].split('|')[1].strip()
        query += 'and %s =\'%s\' ' % ('arrival_name', html_get['arrival_name'])
    if html_get['dt'] != '':
        query += 'and %s = \'%s\'' % ('dt', html_get['dt'])
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    for i in data:
        i['Departure']= "%s | %s" % (airport_city(i['departure_name']),i['departure_name'])
        i['Arrival']= "%s | %s" % (airport_city(i['arrival_name']),i['arrival_name'])
    return data

def reg_validation_cus(conn,info):

    return status, err

def reg_validation_ba(conn,session):
    query = 'select * from booking_agent ' \
            'where email = \'%s\' ' \
            'and pass_word = \'%s\' ' \
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

def add_ba(conn, session):
    query = 'insert into booking_agent values' \
            '(\'%s\',\'%s\',\'%s\')'%(session['email'],session['password'],session['booking_agent_id'])
    print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    return

def reg_validation_as(conn,session):
    return status, err


def check_full(dic):
    for key in dic.keys():
        print(key, dic[key])
        if dic[key] == '' or dic[key]== None:
            return False
    return True
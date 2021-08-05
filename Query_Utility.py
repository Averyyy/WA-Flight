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

def public_view(conn):
    # From query fetch all
    cursor=conn.cursor()
    query = "select * from flight"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    d_dic = {
             'airline':[],
             'departure_city': [],
             'departure_airport':[],
             'arrival_city': [],
             'arrival_airport': [],
             'price':[]
             }

    for i in range(len(data)):
        d_dic['airline'].append(data[i]['airline_name'])
        d_dic['departure_airport'].append(str(data[i]['departure_name']))
        d_dic['arrival_airport'].append(str(data[i]['arrival_name']))
        d_dic['price'].append(str(data[i]['price']))

    # get rid of all the duplicate elements
    d_dic['airline'] = remove_duplicate(d_dic['airline'])
    d_dic['departure_airport'] = remove_duplicate(d_dic['departure_airport'])
    d_dic['arrival_airport'] = remove_duplicate(d_dic['arrival_airport'])
    d_dic['price'] = remove_duplicate(d_dic['price'])

    # mapping back the airport to the city
    for i in d_dic['departure_airport']:
        d_dic['departure_city'].append("%s | %s" % (airport_city(i),i))
    for i in d_dic['arrival_airport']:
        d_dic['arrival_city'].append("%s | %s" % (airport_city(i),i))

    for i in data:
        print(i)
        print(i,i['departure_name'])
        i['Departure']= "%s | %s" % (airport_city(i['departure_name']),i['departure_name'])
        i['Arrival']= "%s | %s" % (airport_city(i['arrival_name']),i['arrival_name'])


    pprint.pprint(d_dic)
    pprint.pprint(data)
    return d_dic, data
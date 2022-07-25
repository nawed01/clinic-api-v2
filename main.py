import re
import pymysql
from mysql.connector import Error
from sqlalchemy import true
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import time,datetime

@app.route('/signup', methods = ['POST'])
def signUp_user():
    try:
        _json = request.json
        _phone_number = _json['phone_number']
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # check if user already exist ? if not register
        cursor.execute("SELECT EXISTS(SELECT * from user WHERE phone_number=%s)",_phone_number)
        result = cursor.fetchone()
        key = f"EXISTS(SELECT * from user WHERE phone_number='{_phone_number}')"
        if (result[key] == 0):
            # not found
            # crate user
            cursor.execute("INSERT INTO user(phone_number, created_at) VALUES(%s, %s)",(_phone_number, timestamp))
            conn.commit()
            respone = jsonify(getDictonary(get_user(_phone_number),201))
            return respone
        else:
            respone = jsonify(getDictonary(get_user(_phone_number),200))
            return respone
       
    except pymysql.Error as e:
        print(e)
        return showMessage()
    finally:
        cursor.close() 
        conn.close()
     
def get_user(phone_number):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, phone_number, created_at FROM user WHERE phone_number=%s",phone_number)
        user = cursor.fetchone()
        return user
    except pymysql.Error as e:
        print(e)
        return showMessage()
    finally:
        cursor.close() 
        conn.close()  

@app.route('/profile/<int:user_id>', methods = ['GET'])
def get_user_profile(user_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT userID, name, address FROM profile WHERE userID =%s", user_id)
        user = cursor.fetchone()
        respone = jsonify(getDictonary(user,200))
        return respone
    except pymysql.Error as e:
        print(e)
        return showMessage()
    finally:
        cursor.close() 
        conn.close() 

@app.route('/profile', methods = ['POST'])
def create_user_profile():
    try:
        _json = request.json
        _address = _json['address']
        _name = _json['name']
        _userID = _json['userID']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("INSERT INTO profile(userID, name, address) VALUES(%s, %s,%s)",(_userID, _name, _address))
        
        conn.commit()
        respone = get_user_profile(_userID)
        return respone
    except pymysql.Error as e:
        print(e)
        return showMessage()
    finally:
        cursor.close() 
        conn.close() 



@app.route('/form/<int:user_id>', methods = ['GET'])
def get_user_forms(user_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT patient_name, age, gender, brief, appointment_at, created_at FROM form WHERE userID =%s", user_id)
        forms = cursor.fetchall()
        # data = {}
        # for index, form in enumerate(forms):
        #     data[index+1] = form
        respone = jsonify(getDictonary(forms,200))
        return respone
    except pymysql.Error as e:
        print(e)
        return showMessage()
    finally:
        cursor.close() 
        conn.close() 

@app.route('/form', methods = ['POST'])
def create_user_form():
    try:
        _json = request.json
        _userID = _json['userID']
        _patient_name = _json['patient_name']
        _age = _json['age']
        _gender = _json['gender']
        _phone_number = _json['phone_number']
        _brief = _json['brief']
        _appointment_at = _json['appointment_at']
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("INSERT INTO form(userID, patient_name, age, gender, phone_number, brief, appointment_at, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(_userID, _patient_name, _age,_gender, _phone_number, _brief, _appointment_at, timestamp))
        conn.commit()
        respone = jsonify(getDictonary("Success",201))
        return respone
    except pymysql.Error as e:
        print(e)
        return showMessage()
    finally:
        cursor.close() 
        conn.close() 

def getDictonary(data,status_code):
      dictionary = {
            "data": data,
            "status": status_code
        }
      return dictionary
        
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message':'Error',
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
    
        
if __name__ == "__main__":
    app.run(debug=true)

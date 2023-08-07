


import pymysql
from flask import Flask, redirect, render_template, request, session


# start
app = Flask(__name__)
# session secret key
app.secret_key = '&*%*$%*)&)(++)+)(&*^%^&^*$%&^'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        contact = request.form["contact"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        age = request.form["age"]
        height= request.form["height"]
        weight = request.form["weight"]

        # server form validation: ensures we receive the correct infomation
        # eliminate empties, correct phone number, password length, match
        # password length: password = "12345A" len(password) -> 6
        if len(password) < 8:
            return render_template('register.html', error_message = 'Password should be atleast 8 characters')
        
        elif password != confirm:
            return render_template('register.html', error_message = 'Password Dont Match!!!!')
        
        else:
            connection = pymysql.connect(host='localhost', user='root', password='', database='healthmate')

            cursor_register = connection.cursor()
            sql_register = 'insert into users (username, email, contact, password,age, height, weight) values (%s, %s, %s,%s,%s,%s,%s)'
            cursor_register.execute(sql_register, (username, email,contact, password , age ,height,weight ))

            # commit(): ensures that the table has been updated with the new record
            connection.commit()
            # send the sms to a registered user: phone
            # username, password
            # from sms import send_sms
            # send_sms(contact, f'Thank for registering, your username is {username} and password is {password} keep it safe')


            return redirect('/login')

    else:
        return render_template('register.html')
    


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='healthmate')
        cursor_login = connection.cursor()
        sql_login = 'select * from users where username = %s and password = %s'
        
        cursor_login.execute(sql_login, (username, password))

        # rowcount: counting the records on a table and return a numeric value
        if cursor_login.rowcount == 0:
            return render_template('login.html', error_message = 'Invalid Credentials, Try Again!!!')
        else:
            session['key'] = username
            return redirect('/home')

    else:
        return render_template('login.html')




@app.route('/cancer')
def cancer():
    return render_template('cancer.html')



@app.route('/docs')
def docs():
    return render_template('docs.html')


@app.route('/patient', methods=['POST', 'GET'])
def patient():
    if request.method == 'POST':
        
        allergies = request.form['allergies']
        condition= request.form['special-condition']
        immunization = request.form['immunization-schedule']
        pregnancy = request.form['pregnancy']
        deathage = request.form['death-age']
        deathcause = request.form['age_deathcause']
        latrines= request.form['functional-latrines']
        water = request.form['clean-water']
        facility= request.form['health-facility']

        connection = pymysql.connect(host='localhost', user='root', password='', database='uzimadb')
        cursor=connection.cursor()

        data = (allergies,condition,immunization,pregnancy,deathage,deathcause,latrines,water,facility)

        sql = "insert into forms (allergies,conditions,immunization,pregnancy,age_death,age_deathcause,latrines,water,facility) values (%s, %s, %s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql,data)
        connection.commit()
        return render_template('patient.html', message = 'saved succesfuly')


    else:
        return render_template('patient.html')



@app.route('/page')
def page():
    return render_template('page.html')


@app.route('/condition')
def condition():
    return render_template('condition.html')


@app.route('/about us')
def aboutus():
    return render_template('about us.html')



@app.route('/reports')
def reports():
    
    connection = pymysql.connect(host='localhost', user='root', password='', database='uzimadb')
    cursor=connection.cursor()

    sql = "select * from forms "
    cursor.execute(sql)
    count = cursor.rowcount
    if count == 0:
        return render_template('reports.html', message = "no reports available")
    else:
        reports = cursor.fetchall()
        return render_template('reports.html', reports = reports)


@app.route('/cancermedi')
def cancermedi():
    return render_template('cancermedi.html')


@app.route('/cancernutri')
def cancernutri():
    return render_template('cancernutri.html')



@app.route('/covid')
def covid():
    return render_template('covid.html')



@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/covidfit')
def covidfit():
    return render_template('covidfit.html')


@app.route('/covidmedi')
def covidmedi():
    return render_template('covidmedi.html')


@app.route('/covidnutri')
def covidnutri():
    return render_template('covidnutri.html')



@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


@app.route('/diabetenutri')
def diabetenutri():
    return render_template('diabetenutri.html')


@app.route('/diabetesmedi')
def diabetesmedi():
    return render_template('diabetesmedi.html')



@app.route('/diafitness')
def diafitness():
    return render_template('diafitness.html')




@app.route('/medipham')
def medipham():
    connection  = pymysql.connect(host='localhost', user='root', password='', database='healthmate')
    print("Connection Successful")

    # x category
    cursorbreastcancer = connection.cursor()
    sqlbreastcancer = 'select * from products where product_category = "breastcancer"'
    cursorbreastcancer.execute(sqlbreastcancer)
    breastcancer = cursorbreastcancer.fetchall()

    # y category
    cursorbloodcancer = connection.cursor()
    sqlbloodcancer = 'select * from products where product_category = "bloodcancer"'
    cursorbloodcancer.execute(sqlbloodcancer)
    bloodcancer = cursorbloodcancer.fetchall()

     # detergent category
    cursorZ = connection.cursor()
    sqlZ = 'select * from products where product_category = "z"'
    cursorZ.execute(sqlZ)

    z_items = cursorZ.fetchall()

    return render_template('medipham.html', records = breastcancer, easter = bloodcancer, latest = z_items)



@app.route('/single/<product_id>')
def single(product_id):
    connection  = pymysql.connect(host='localhost', user='root', password='', database='healthmate')
    print("Connection Successful")
    print(product_id)

    cursor_single = connection.cursor()
    sql_single = 'select * from products where product_id = %s'
    # Formatting options (%s) -> 
    cursor_single.execute(sql_single, product_id)
    
    single = cursor_single.fetchone()
    print(single[3])

    # similar items based on category -> single[4]
    cursor_similar = connection.cursor()
    sql_similar = 'select * from products where product_category = %s'
    cursor_similar.execute(sql_similar, single[3])

    data = cursor_similar.fetchall()
    print("similar data", data)

    return render_template('single.html', single_record = single, similar = data)



import base64
import datetime

import requests
from requests.auth import HTTPBasicAuth


@app.route('/mpesa', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phonenumber = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phonenumber,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phonenumber,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href="/" class="btn btn-dark btn-sm">Back to Products</a>'
    else:
        return render_template('single.html')
    
    


    


    

app.run(debug=True)
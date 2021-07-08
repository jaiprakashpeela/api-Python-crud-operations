import csv
import re
import psycopg2
from psycopg2 import Error
from datetime import date
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return {"msg": "Dummy msg "}


def db_conn_cursor():
    # details of new database
    Username = "postgres"
    Password = "postgres"
    DATABASE = "postgres_jai"
    PORT = "5432"
    HostName = "127.0.0.1"
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=Username, password=Password, host=HostName, port=PORT, database=DATABASE)
        # cursor creation for database operations

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return connection


# creating an global variable for db and cursor
db_conn = db_conn_cursor()
cursor = db_conn.cursor()


# calculating age using age by date 0f birth
def get_Age(birthDate):
    a = birthDate.split('/')
    Day = int(a[0])
    month = int(a[1])
    Year = int(a[2])
    today = date.today()
    age = today.year - Year - ((today.month, today.day) < (month, Day))
    return age


# verifying email command using regular expression
def verify_email_format(email):
    regex = '^[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True;
    else:
        return False;


# Util functions for name split
def get_name(name):
    names = name.split()
    first_name = names[0]
    last_name = names[1]
    return first_name, last_name


@app.route("/import")
# using csv module to read rows from csv file
def insert_row_csv():
    # creating an cursor
    file_name = 'row_insert.csv'
    with open(file_name, newline='') as csv_file:
        # converting rows in dict
        data = csv.DictReader(csv_file)
        for row in data:
            if verify_email_format(row['Email']):
                First_name, Last_name = get_name(row['Name'])
                Age = get_Age(row['DateOfBirth'])
                city = row[city]
                state = row[state]
                row_list = (row['Id'], First_name, Last_name, row['Email'], Age, city, state)
                cursor.execute("INSERT INTO employee VALUES (%s,%s, %s, %s, %s, %s, %s)", row_list)
                db_conn.commit()
            else:
                continue
    return {"message": " imported all rows from csv "}


@app.route('/insert', methods=['POST', 'PUT'])
def insert():
    method = None
    data = request.get_json()
    if request.method == "POST":
        if verify_email_format(data['Email']):
            First_name, Last_name = get_name(data['Name'])
            Age = get_Age(data['DateOfBirth'])
            row_list = (data['Id'], First_name, Last_name, data['Email'], Age, data['city'], data['state'])
            cursor.execute("INSERT INTO employee VALUES (%s,%s, %s, %s, %s, %s, %s)", row_list)
            method = True
        else:
            return {"message": "please check email format "}
    else:
        try:
            cursor.execute("UPDATE employee SET firstname = %s WHERE no_id = %s", (data['firstname'], data['Id']))
            method = False
        except Exception as e:
            return {"error": e}
    db_conn.commit()

    if method:
        return {"message": " Inserted row"}
    else:
        return {"msg": "updated row"}


@app.route('/query', methods=['GET', 'DELETE'])
def query():
    method = None
    data = request.get_json()
    if request.method == "GET":
        try:
            cursor.execute("SELECT * FROM employee WHERE no_id = %s", str(data['Id']))
            result = cursor.fetchall()
            db_conn.commit()
            method = True
        except Exception as e:
            return {"error": e}
    else:
        cursor.execute("DELETE FROM employee WHERE no_id = %s", (str(data['Id'])))
        db_conn.commit()
        method = False

    if method:
        return {"results": result}
    else:
        return {"result": "deleted row "}


if __name__ == '__main__':
    app.run(debug=True)
    db_conn.close()
    cursor.close()

# Importing Libraries
import mysql.connector
from mysql.connector import Error

postNetWorth = 0
preNetWorth = 0


# Function to Connect To MySQL Database
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database Connection Successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


# Variable To Call To Initialize Connection To MySQL Database
initialize = create_db_connection("fake_name", "fake_name", 'fake_password', "fake_name")


# Function That Asks User Which Action They Would Like To Perform For Their Bank Account
def options():
    choice = input("Would You Like To EDIT, READ, CREATE, HISTORY, EXIT : ")
    while not choice.upper() == 'EXIT':
        if choice.upper() == 'EDIT':
            edit_information()
            choice = input("Would You Like To EDIT, READ, CREATE, HISTORY, EXIT : ")
        if choice.upper() == 'READ':
            read_information()
            choice = input("Would You Like To EDIT, READ, CREATE, HISTORY, EXIT : ")
        if choice.upper() == 'CREATE':
            create_information()
            choice = input("Would You Like To EDIT, READ, CREATE, HISTORY, EXIT : ")
        if choice.upper() == 'HISTORY':
            get_history()
            choice = input("Would You Like To EDIT, READ, CREATE, HISTORY, EXIT : ")
    exit()


# Function To Insert Multiple Records Into A Database Table
def create_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")


# Function To Update Records In A Database Table
def edit_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.execute(sql, val)
        connection.commit()
        print("Query Successful")
    except Error as err:
        print(f"Error: '{err}'")


# Function To Retrieve Net Worth From The Database And Store In Global Variables
def read_query(connection, query, user):
    global preNetWorth
    global postNetWorth
    cursor = connection.cursor()
    try:
        cursor.execute(query, user)
        result = cursor.fetchall()
        preNetWorth = str(result[0])
        preNetWorth = preNetWorth.strip('( ,)')
        print(f'Current Net Worth Is {preNetWorth}')
        postNetWorth = float(preNetWorth)
    except Error as err:
        print(f"Error: '{err}'")


# Function To Retrieve And Print All Records From A Table
def history_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for result in result:
            print(result)
    except Error as err:
        print(f"Error: '{err}'")


# Function To Add Information To A User's Bank Account History
def create_information():
    global initialize
    date = input('Enter Date: ')
    purchase = input('Enter Purchase: ')
    value = int(input('Enter Amount: '))
    sql = '''
       INSERT INTO HISTORY (DATE, PURCHASE, VALUE)
       VALUES (%s, %s, %s)
       '''
    val = [(date, purchase, value)]
    create_query(initialize, sql, val)


# Function To Update A User's Net Worth In The Database
def edit_information():
    global postNetWorth
    global initialize
    read_information()
    current_worth = float(input('Enter New Amount: '))
    final_worth = current_worth + postNetWorth
    sql = '''
   UPDATE BANK SET Net_Worth = %s WHERE ID = %s
   '''
    val = (final_worth, 1)
    edit_query(initialize, sql, val)


# Function To Read And Display A User's Net Worth From The Database
def read_information():
    global initialize
    user = list(input('Enter ID: '))
    q1 = '''
    SELECT Net_Worth FROM BANK WHERE ID = %s;
    '''
    read_query(initialize, q1, user)


# Function To Retrieve And Print The Transaction History
def get_history():
    global initialize
    q1 = '''
   SELECT * FROM HISTORY;
   '''
    history_query(initialize, q1)


def final_run():
    options()


final_run()

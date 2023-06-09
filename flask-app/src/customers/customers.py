from flask import Blueprint, request, jsonify, make_response
import json
from src import db
from datetime import datetime

customers = Blueprint('customers', __name__)

'''

-----------------------------------------

All GET Routes for Customer Blueprint

'''
# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()

    cursor.execute("SELECT * FROM Customers")

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

# Get all customers names for the form from the DB
@customers.route('/customers/names', methods=['GET'])
def get_customers_form():
    cursor = db.get_db().cursor()

    cursor.execute("SELECT CONCAT(FirstName, ' ', LastName) as label, CustomerID as value FROM Customers")

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute("SELECT * FROM Customers WHERE CustomerID = %s", (userID,))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'


    return the_response

# Get customer ticket detail for customer with particular userID
@customers.route('/customers/<userID>/tickets', methods=['GET'])
def get_customer_ticket(userID):

    cursor = db.get_db().cursor()

    query = "SELECT VenueName, Description, Date, Seat_Row, Seat_Column, Section FROM \
                Customers JOIN Tickets USING (CustomerID) JOIN Venues USING (VenueID) JOIN Performance USING (PerformanceID) WHERE CustomerID = %s"

    cursor.execute(query, (userID,))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

# Getting dependent info based on CustomerID 
@customers.route('/customers/<userID>/dependents', methods = ['GET'])
def get_dependent(userID):
    cursor = db.get_db().cursor()

    query = f"SELECT CONCAT(FirstName, ' ', LastName) as label, DependentID as value From Dependent Where Parent = %s and FirstName !='unavailable'"

    cursor.execute(query, (userID,))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

# Getting Customers Info for Edit Form 
@customers.route('/customers/<cIDInf>/info', methods=['GET'])
def get_customers_info(cIDInf):
    cursor = db.get_db().cursor()

    query = "SELECT FirstName, LastName, Email, PhoneNumber FROM Customers WHERE CustomerID = %s"

    cursor.execute(query, (cIDInf,))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    db.get_db().commit()

    return the_response

# Find all of the artists and present in form format
@customers.route('/customers/fanof', methods = ['GET'])
def get_artists_name():
    cursor = db.get_db().cursor()

    cursor.execute("SELECT CONCAT(FirstName, ' ', LastName) as label, ArtistID as value FROM Artists")

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

# Get emergency contact information of Dependents for a customer
@customers.route('/customers/dependent/<cIdDInf>/info', methods=['GET'])
def get_dependents_info(cIdDInf):
    cursor = db.get_db().cursor()

    query = "SELECT FirstName, LastName, Email, PhoneNumber, Relationship, Street, City, State, Zipcode, Country FROM Dependent WHERE Parent = %s"

    cursor.execute(query, (cIdDInf,))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    db.get_db().commit()

    return the_response

'''
-----------------------------------------

 All POST routes for Customer Blueprint
'''

# Adding a new Customer 
@customers.route('/customers', methods=['POST'])
def add_customer():
    cursor = db.get_db().cursor()

    cust_info = request.json

    cust_tuple = f"('{cust_info.get('CusFirstName', 'NULL')}', '{cust_info.get('CusLastName')}', '{cust_info.get('CusPhone')}', '{cust_info.get('CusEmail')}', '{cust_info.get('CusDOB')[:10]}', \
        '{cust_info.get('CusStreet')}', '{cust_info.get('CustCity')}', '{cust_info.get('CustState')}', '{cust_info.get('CustZipcode')}', '{cust_info.get('CustCountry')}')"
    
    query = f"INSERT INTO Customers (FirstName, LastName, PhoneNumber, Email, DOB, Street, City, State, ZipCode, Country) VALUES {cust_tuple}"

    cursor.execute(query)

    db.get_db().commit()

    return "Successfully added user into database."

# Adding a dependent for a customer 
@customers.route('/customers/<customerID>/dependents', methods=['POST'])
def add_customer_dependent(customerID):
    cursor = db.get_db().cursor()

    cust_info = request.json

    cust_tuple = f"('{cust_info.get('DepFirstName', 'NULL')}', '{cust_info.get('DepLastName')}', '{cust_info.get('DepPhoneCopy')}', '{cust_info.get('DepEmail')}', '{cust_info.get('Relationship')}', \
        '{cust_info.get('DepStreet')}', '{cust_info.get('DepCity')}', '{cust_info.get('DepState')}', '{cust_info.get('DepZipcode')}', '{cust_info.get('DepCountry')}', {customerID})"
    
    query = f"INSERT INTO Dependent (FirstName, LastName, PhoneNumber, Email, Relationship, Street, City, State, ZipCode, Country, Parent) VALUES {cust_tuple}"

    cursor.execute(query)

    db.get_db().commit()

    return "Successfully added dependent."

# Submitting favourite artist
@customers.route('/customers/artist/fanof/<CidAid>', methods=['POST'])
def add_favourite_artist(CidAid):
    
    cursor = db.get_db().cursor()

    artist_info = request.json

    for artist_ID in artist_info:
        query = f"INSERT INTO Fan_Of (CustomerID, ArtistID) VALUES ({CidAid}, {artist_ID})"

        cursor.execute(query)

    db.get_db().commit()

    return "Successfully added Favourite Artists"

'''
-----------------------------------------

 All DELETE routes for Customer Blueprint
'''

# Deleting Dependent
@customers.route('/customers/<userID>/remove_dependent/<dependentID>', methods=['DELETE'])
def delete_dependent(userID, dependentID):
    cursor = db.get_db().cursor()
    
    query = f"UPDATE Dependent SET FirstName = 'unavailable', LastName = 'unavailable', \
        PhoneNumber = NULL, Email = NULL, Street = NULL, City = NULL, State  = NULL, \
            Zipcode  = NULL, Country  = NULL, Relationship = 'unavailable' WHERE Parent = %s and DependentID  = %s"
    
    cursor.execute(query, (userID, dependentID))

    db.get_db().commit()

    return "Deleted dependent"

# Deleteing customer account 
@customers.route('/customers/<userID>', methods =['DELETE'])
def delete_account(userID):
    cursor = db.get_db().cursor()

    query = f"UPDATE Customers SET FirstName = 'unavailable', LastName = 'unavailable', \
        PhoneNumber = NULL, Email = NULL, Street = NULL, City = NULL, State  = NULL, \
            Zipcode = NULL, Country = NULL WHERE CustomerID = %s"
    
    cursor.execute(query, (userID,))

    db.get_db().commit()
    
    return "Deleted customer account"


'''
-----------------------------------------

 All PUT routes for Customer Blueprint
'''

# Update Customers Info from Edit form
@customers.route('/customers/<userID>', methods=['PUT'])
def put_customers(userID):
    cursor = db.get_db().cursor()

    c_info = request.json

    query = f"UPDATE Customers SET FirstName = '{c_info.get('VOFirstNameCopy')}', LastName = '{c_info.get('VOLastNameCopy')}', \
    PhoneNumber = '{c_info.get('VOPhoneCopy')}', Email = '{c_info.get('VOEmailCopy')}' WHERE CustomerID = %s"

    cursor.execute(query, (userID,))

    db.get_db().commit()

    return "Success!"


# Update A Dependent Info from Edit form
@customers.route('/customers/dependent/<DepId>', methods=['PUT'])
def put_customers_dependent(DepId):
    cursor = db.get_db().cursor()

    d_info = request.json

    query = f"UPDATE Dependent SET FirstName = '{d_info.get('DepFirstName')}', LastName = '{d_info.get('DepLastName')}', \
    PhoneNumber = '{d_info.get('DepPhoneCopy')}', Relationship = '{d_info.get('Relationship')}', \
    Street = '{d_info.get('DepStreet')}', City = '{d_info.get('DepCity')}', State = '{d_info.get('DepState')}', \
    Zipcode = '{d_info.get('DepZipcode')}', Country = '{d_info.get('DepCountry')}' WHERE DependentID = %s"

    cursor.execute(query, (DepId,))

    db.get_db().commit()

    return "Success!"

# Purchasing ticket by setting a Ticket to a specific Customer
@customers.route('/customers/<userID>/assign_ticket/<ticketID>', methods=['PUT'])
def assign_ticket(userID, ticketID):
    cursor = db.get_db().cursor()

    query = f"UPDATE Tickets SET CustomerID = %s WHERE TicketID = %s"
    
    cursor.execute(query, (userID, ticketID))

    db.get_db().commit()

    return "Successfully assigned ticket"

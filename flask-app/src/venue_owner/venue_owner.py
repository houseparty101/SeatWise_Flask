from flask import Blueprint, request, jsonify, make_response
import json
from src import db

# Create a new Flask Blueprint
# IMPORTANT: Notice in the routes below, we are adding routes to the 
# blueprint object, not the app object.
venue_owner = Blueprint('venue_owners', __name__)

'''

-----------------------------------------

All GET Routes for Venue Owner Blueprint

'''

# Get all venues owned by a venue owner 
@venue_owner.route('/venues/<VenueOwnerID>', methods=['GET'])
def get_owner_venues(VenueOwnerID):
    cursor = db.get_db().cursor()

    query = "SELECT VenueName as label, VenueID as value FROM Venues WHERE OwnerID = %s"

    cursor.execute(query, (VenueOwnerID,))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

# Get All Venue Owner First + Last Name
@venue_owner.route('/venue_owner/name', methods=['GET'])
def get_venue_owner_names():
    cursor = db.get_db().cursor()

    query = "SELECT CONCAT(FirstName, ' ', LastName) as label, OwnerID as value FROM VenueOwner"

    cursor.execute(query)

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

# Get All Info of a Venue Owner
@venue_owner.route('/venue_owner/<voIDinfo>/info', methods=['GET'])
def get_venue_owner_email(voIDinfo):
    cursor = db.get_db().cursor()

    query = "SELECT FirstName, LastName, PhoneNumber, Email FROM VenueOwner WHERE OwnerID = %s"

    cursor.execute(query, (voIDinfo,))

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

# Get All Venue Owners
@venue_owner.route('/venue_owner', methods=['GET'])
def get_venue_owners():
    cursor = db.get_db().cursor()

    query = "SELECT * FROM VenueOwner"

    cursor.execute(query)

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'



    return the_response

'''

-----------------------------------------

All POST Routes for Venue Owner Blueprint

'''

# Add a new venue owner
@venue_owner.route('/venue_owner', methods=['POST'])
def add_venue_owner():
    cursor = db.get_db().cursor()

    vo_info = request.json

    vo_tuple = f"('{vo_info.get('VOFirstName')}', '{vo_info.get('VOLastName')}', '{vo_info.get('VOPhone')}', '{vo_info.get('VOEmail')}')"

    query = f"INSERT INTO VenueOwner (FirstName, LastName, PhoneNumber, Email) VALUES {vo_tuple}"

    cursor.execute(query)

    db.get_db().commit()

    return "Successfully added new Venue Owner"

'''

-----------------------------------------

All PUT Routes for Venue Owner Blueprint

'''

# Update the Info of the specified Venue Owner
@venue_owner.route('/venue_owner/<VenueOwnerID>', methods=['PUT'])
def put_venue_owners(VenueOwnerID):
    cursor = db.get_db().cursor()

    vo_info = request.json

    query = f"UPDATE VenueOwner SET FirstName = '{vo_info.get('VOFirstName')}', LastName = '{vo_info.get('VOLastName')}', \
    PhoneNumber = '{vo_info.get('VOPhone')}', Email = '{vo_info.get('VOEmail')}' WHERE OwnerID = %s"

    cursor.execute(query, (VenueOwnerID,))

    db.get_db().commit()

    return "Success!"
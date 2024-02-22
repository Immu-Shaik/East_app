Address Book Application

This is a simple address book application built with FastAPI and SQLite. 
It allows users to perform CRUD operations on addresses and retrieve addresses 
within a specified distance from a given location.

Installation

Clone the repository:

git clone https://github.com/yourusername/address-book.git
Navigate to the project directory:


cd address-book
Install the required dependencies:

pip install -r requirements.txt
Usage
Start the FastAPI application:
uvicorn main:app --reload

Once the server is running, you can access the Swagger documentation by visiting http://localhost:8000/docs in your web browser. Here you can explore and interact with the API endpoints.

Use the provided API endpoints to perform CRUD operations on addresses:

POST /addresses/: Create a new address.
GET /addresses/{address_id}: Retrieve an address by ID.
PUT /addresses/{address_id}: Update an existing address.
DELETE /addresses/{address_id}: Delete an address by ID.
POST /addresses/distance/: Retrieve addresses within a specified distance from a given location.


Models
Address

id: The unique identifier for the address.
street: The street name.
city: The city name.
state: The state name.
postal_code: The postal code.
latitude: The latitude coordinate of the address.
longitude: The longitude coordinate of the address.

AddressCreate
Pydantic model for creating a new address.
AddressUpdate
Pydantic model for updating an existing address.

AddressInDB

Pydantic model for the address stored in the database.

AddressDistanceQuery

Pydantic model for specifying the location and distance query parameters.
Contributing"# East_app" 

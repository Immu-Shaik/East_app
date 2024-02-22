from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geopy.distance import geodesic

# Create FastAPI instance
app = FastAPI()

# SQLite database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./addresses.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Address model
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    postal_code = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic models for request and response
class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    latitude: float
    longitude: float

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AddressInDB(AddressCreate):
    id: int

class AddressDistanceQuery(BaseModel):
    latitude: float
    longitude: float
    distance: float

# Routes
@app.post("/addresses/", response_model=AddressInDB)
def create_address(address: AddressCreate):
    db = SessionLocal()
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    db.close()
    return db_address

@app.get("/addresses/{address_id}", response_model=AddressInDB)
def read_address(address_id: int):
    db = SessionLocal()
    address = db.query(Address).filter(Address.id == address_id).first()
    db.close()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.put("/addresses/{address_id}", response_model=AddressInDB)
def update_address(address_id: int, address: AddressUpdate):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for attr, value in address.dict(exclude_unset=True).items():
        setattr(db_address, attr, value)
    db.commit()
    db.refresh(db_address)
    db.close()
    return db_address

@app.delete("/addresses/{address_id}")
def delete_address(address_id: int):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    db.close()
    return {"message": "Address deleted successfully"}

@app.post("/addresses/distance/", response_model=List[AddressInDB])
def get_addresses_within_distance(query: AddressDistanceQuery):
    db = SessionLocal()
    addresses = db.query(Address).all()
    db.close()
    filtered_addresses = []
    for address in addresses:
        distance = geodesic((address.latitude, address.longitude),
                            (query.latitude, query.longitude)).miles
        if distance <= query.distance:
            filtered_addresses.append(address)
    return filtered_addresses

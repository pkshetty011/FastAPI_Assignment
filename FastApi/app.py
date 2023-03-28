from fastapi import FastAPI
from typing import List
from geopy import distance
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel

class Address(BaseModel):
    id: int
    name: str
    street: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float

DATABASE_URL = "sqlite:///./addresses.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AddressModel(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.post("/addresses/")
async def create_address(address: Address):
    db = SessionLocal()
    db_address = AddressModel(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/addresses/{address_id}")
async def read_address(address_id: int):
    db = SessionLocal()
    db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}")
async def update_address(address_id: int, address: Address):
    db = SessionLocal()
    db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    update_data = address.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.delete("/addresses/{address_id}")
async def delete_address(address_id: int):
    db = SessionLocal()
    db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return {"message": "Address deleted successfully"}

@app.get("/addresses/")
async def read_addresses(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    addresses = db.query(AddressModel).offset(skip).limit(limit).all()
    return addresses

@app.get("/addresses/nearby")
async def read_addresses_nearby(latitude: float, longitude: float, distance_km: float = 1.0):
    db = SessionLocal()
    addresses = db.query(AddressModel).all()
    nearby_addresses = []
    user_location = (latitude, longitude)
    for address in addresses:
        address_location = (address.latitude, address.longitude)
        if distance.distance(user_location, address_location).km <= distance_km:
            nearby_addresses.append(address)
    return nearby_addresses


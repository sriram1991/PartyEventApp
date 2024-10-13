import json.decoder
import sys
from linecache import cache

import models

sys.path.append("..")

from starlette import status
from models import Location

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from routers.auth import get_current_user

from database import engine, SessionLocal, get_db
from models import Base
from logger import logger

router = APIRouter(
    prefix="/location",
    tags=["location"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreateLocation(BaseModel):
    name: str
    description: str
    address: str
    pincode: int
    state: str
    city: str


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def getAllLocation(db: db_dependency):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        location = db.query(Location).all()
        logger.info(location)
        if location is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return location
    except Exception as e:
        logger.error("error in fetch All location", exc_info=e)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_location(user: user_dependency, db: db_dependency, location_request: CreateLocation):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    location_model = Location(**location_request.dict())
    #in case of foreign key key=user.get('id')
    # location_model.location = location_request.id
    db.add(location_model)
    db.commit()


@router.get("/getAll")
def get_all_locations(db: db_dependency):
    return getAllLocation(db)


@router.get("/get/{location_id}")
def get_location(db: db_dependency, location_id: int):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')

        logger.info(location_id)
        location = db.query(Location).filter(Location.id == location_id).first()
        logger.info(location)
        if location is None:
            return logger.error(f"Selected id is invalid data or no match found in DB for location: {location_id}")

        return location
    except Exception as e:
        logger.error("error in fetch location", exc_info=e)

@router.put("/update/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_location(user: user_dependency, db: db_dependency,
                          location_request: CreateLocation, location_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        return logger.error(f"Selected id is invalid data or no match found in DB for Location {location_id}")

    location.name = location_request.name
    location.description = location_request.description
    location.address = location_request.address
    location.pincode = location_request.pincode
    location.city = location_request.city
    location.state = location_request.state

    db.add(location)
    db.commit()

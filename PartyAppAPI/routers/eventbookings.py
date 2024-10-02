import sys

from logger import logger

sys.path.append("..")

from routers.location import getAllLocation
from routers.partyevent import get_all_party_event
from routers.slots import get_all_slots
from routers.theaters import get_all_theaters
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from database import engine, get_db
from models import Base, Gallery, PartyEvent, BookingEntry

router = APIRouter(
    prefix="/booking",
    tags=["booking"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreateEventBooking(BaseModel):
    total_amount: int
    date: datetime = None
    no_of_peoples: int
    addons_selected: str
    booking_name: str
    booking_mobile: str
    booking_email: str
    advance_amount: int
    discount_coupon: str
    referral_code: str


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
theaters_dependency = Annotated[dict, Depends(get_all_theaters)]
location_dependency = Annotated[dict, Depends(getAllLocation)]
slots_dependency = Annotated[dict, Depends(get_all_slots)]
party_dependency = Annotated[dict, Depends(get_all_party_event)]


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_event_booking(db: db_dependency, event_request: CreateEventBooking):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        booking_model = BookingEntry(**event_request.dict())
        #in case of foreign key key=user.get('id')

        logger.info(f"booking_model - {booking_model}")
        db.add(booking_model)
        db.commit()
    except Exception as e:
        logger.error("error in fetch All Theaters ", exc_info=e)

def get_all_event_bookings(user: user_dependency, db: db_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        bookingList = db.query(BookingEntry).all()

        logger.info(f"bookingList - {bookingList}")
        if bookingList is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Could not validate user.')
        return bookingList
    except Exception as e:
        logger.error("error in fetch All booking events ", exc_info=e)

@router.get("/getAll")
def get_all_booking(user: user_dependency, db: db_dependency):
    return get_all_event_bookings(user, db)


@router.get("/get/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_booking_by_id(user: user_dependency, db: db_dependency, booking_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        bookings = db.query(BookingEntry).filter(BookingEntry.id == booking_id).first()
        print(bookings)
        if bookings is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Could not validate user.')
        return bookings
    except Exception as e:
        logger.error(f"error getting booking_id {booking_id} ", exc_info=e)

@router.delete("/delete/{booking_id}")
async def delete_booking(user: user_dependency, db: db_dependency, booking_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        bookings = db.query(BookingEntry).filter(BookingEntry.id == booking_id).first()
        if bookings is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Could not validate user.')
        db.query(BookingEntry).filter(BookingEntry.id == booking_id).delete()
        return bookings
    except Exception as e:
        logger.error(f"error in deleting Booking id {booking_id} ", exc_info=e)
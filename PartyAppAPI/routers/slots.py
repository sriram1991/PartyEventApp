import sys
from datetime import datetime

from logger import logger

sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from routers.location import getAllLocation
from database import engine, SessionLocal, get_db
from models import Base, Gallery, Slots

router = APIRouter(
    prefix="/slots",
    tags=["slots"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreateSlots(BaseModel):
    slot_time_duration: str
    slot_date: datetime = None
    location: int
    theater: int
    is_active: bool


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_all_slots(db: db_dependency):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        slots = db.query(Slots).all()
        logger.info(slots)
        if slots is None:
            return logger.error(f"No data found in Slots")

        return slots
    except Exception as e:
        logger.error(f"error in getting AllSlots - ", exc_info=e)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_slots(db: db_dependency, slots_request: CreateSlots):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        slots_model = Slots(**slots_request.dict())
        db.add(slots_model)
        db.commit()
    except Exception as e:
        logger.error(f"error in creating slots - ", exc_info=e)

@router.get("/getAll")
def get_slots(db: db_dependency):
    return get_all_slots(db)


@router.get("/get/{slot_id}")
async def get_slot(db: db_dependency, slot_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        slot = db.query(Slots).filter(Slots.id == slot_id).first()
        if slot is None:
            return logger.error(f"Selected slots_id is invalid data or no match found in DB for {slot_id}")
        return slot
    except Exception as e:
        logger.error(f"error in getting slot id {slot_id} - ", exc_info=e)

@router.put("/update/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_slots(user: user_dependency, db: db_dependency,
                       slots_request: CreateSlots, slot_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        slots = db.query(Slots).filter(Slots.id == slot_id).first()
        if slots is None:
            return logger.error(f"Selected slots_id is invalid data or no match found in DB for {slot_id} to update")

        slots.slot_time_duration = slots_request.slot_time_duration
        slots.slot_date = slots_request.slot_date
        slots.is_active = slots_request.is_active

        db.add(slots)
        db.commit()
    except Exception as e:
        logger.error(f"error in updating slot id {slot_id} - ", exc_info=e)
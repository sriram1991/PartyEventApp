import sys
from datetime import datetime

sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from routers.location import get_all_location
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
    is_active: bool


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
theaters_dependency = Annotated[dict, Depends(get_all_location)]


def get_all_slots(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    slots = db.query(Slots).all()
    print(slots)
    if slots is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return slots


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_location(user: user_dependency, db: db_dependency, slots_request: CreateSlots):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    slots_model = Slots(**slots_request.dict())
    db.add(slots_model)
    db.commit()


@router.get("/getAll")
def get_slots(user: user_dependency, db: db_dependency):
    return get_all_slots(user, db)


@router.get("/get/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_slot(user: user_dependency, db: db_dependency, slot_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    slot = db.query(Slots).filter(Slots.id == slot_id).first()
    if slot is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return slot


@router.put("/update/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_slots(user: user_dependency, db: db_dependency,
                       slots_request: CreateSlots, location_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    slots = db.query(Slots).filter(Slots.id == location_id).first()
    if slots is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

    slots.slot_time_duration = slots_request.slot_time_duration
    slots.slot_date = slots_request.slot_date
    slots.is_active = slots_request.is_active

    db.add(slots)
    db.commit()

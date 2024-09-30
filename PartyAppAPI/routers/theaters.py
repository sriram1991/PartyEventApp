import sys

sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from routers.location import getAllLocation
from database import engine, SessionLocal, get_db
from models import Base, Gallery, Theater

router = APIRouter(
    prefix="/theater",
    tags=["theater"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreateTheater(BaseModel):
    name: str
    description: str
    price: int
    no_of_peoples: int
    extra_cost_each_person: int
    location: int
    no_of_slots: int
    slots: int


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
location_dependency = Annotated[dict, Depends(getAllLocation)]


def get_all_theaters(db: db_dependency):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Could not validate user.')
    theaterList = db.query(Theater).all()
    print(theaterList)

    if theaterList is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return theaterList


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_theater(user: user_dependency, db: db_dependency,
                   theater_request: CreateTheater):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    theater_model = Theater(**theater_request.dict())
    #in case of foreign key key=user.get('id')

    print(str(theater_model))
    db.add(theater_model)
    db.commit()


@router.get("/getAll")
def get_theaters(db: db_dependency):
    return get_all_theaters(db)


@router.get("/get/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_theater(db: db_dependency, event_id: int = Path(gt=0)):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Could not validate user.')
    theater = db.query(Theater).filter(Theater.id == event_id).first()
    print(theater)
    if theater is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return theater


@router.put("/update/{theater_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_theater(user: user_dependency, db: db_dependency,
                         theater_request: CreateTheater, theater_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    theater = db.query(Theater).filter(Theater.id == theater_id).first()

    if theater is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

    theater.name = theater_request.name
    theater.description = theater_request.description
    theater.price = theater_request.price
    theater.no_of_peoples = theater_request.no_of_peoples
    theater.extra_cost_each_person = theater_request.extra_cost_each_person
    theater.location = theater_request.location
    theater.no_of_slots = theater_request.no_of_slots
    theater.slots = theater_request.slots

    db.add(theater)
    db.commit()

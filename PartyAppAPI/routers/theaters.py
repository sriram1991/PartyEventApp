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
from logger import logger

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
    is_active: bool
    location: int
    no_of_slots: int


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
location_dependency = Annotated[dict, Depends(getAllLocation)]


def get_all_theaters(db: db_dependency):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        theaterList = db.query(Theater).all()
        logger.info(theaterList)

        if theaterList is None:
            logger.error("No Theater's found ")
            return "No Theater's found "

        return theaterList
    except Exception as e:
        logger.error("error in fetch All Theaters ", exc_info=e)
        return "Error in fetch All Theaters"


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_theater(user: user_dependency, db: db_dependency,
                   theater_request: CreateTheater):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        theater_model = Theater(**theater_request.dict())
        #in case of foreign key key=user.get('id')

        logger.info(theater_model)
        db.add(theater_model)
        db.commit()
        return "Theater Created Successfully.."
    except Exception as e:
        logger.error("error in creating Theater ", exc_info=e)
        return "Theater creation Failed!"

@router.get("/getAll")
def get_theaters(db: db_dependency):
    return get_all_theaters(db)


@router.get("/get/{theater_id}")
def get_theater(db: db_dependency, theater_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        theater = db.query(Theater).filter(Theater.id == theater_id).first()
        logger.info(theater)
        if theater is None:
            logger.error(f"Selected id is invalid data or no match found in DB for {theater_id}")
            return f"Selected id is invalid data or no match found in DB for {theater_id}"
        return theater
    except Exception as e:
        logger.error("error in fetch All Theaters ", exc_info=e)
        return "error in fetch All Theaters"

@router.put("/update/{theater_id}")
async def update_theater(db: db_dependency,
                         theater_request: CreateTheater, theater_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        theater = db.query(Theater).filter(Theater.id == theater_id).first()

        if theater is None:
            logger.error(f"Selected id is invalid data or no match found in DB for {theater_id}")
            return f"Selected id is invalid data or no match found in DB for {theater_id}"

        theater.name = theater_request.name
        theater.description = theater_request.description
        theater.price = theater_request.price
        theater.no_of_peoples = theater_request.no_of_peoples
        theater.extra_cost_each_person = theater_request.extra_cost_each_person
        theater.location = theater_request.location
        theater.is_active = theater_request.is_active
        theater.no_of_slots = theater_request.no_of_slots

        db.add(theater)
        db.commit()
        return "Theater update success.."
    except Exception as e:
        logger.error(f"error in updating event {theater_id} in DB ", exc_info=e)
        return "Error in Theater update!"

@router.put("/disable/{theater_id}")
async def disable_theater(db: db_dependency,
                            theater_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        theater = db.query(Theater).filter(Theater.id == theater_id).first()
        print(theater.id)
        if theater is None:
            logger.error(f"No match found in DB for id: {theater_id}")
            return f"No match found in DB for id: {theater_id}"
        else:
            # disableing Theater
            theater.is_active = 0
            print("theater")
            print(theater)
            return f"Theater {theater_id} disabled success.."
    except Exception as e:
        logger.error(f"error in updating event {theater_id} in DB ", exc_info=e)
        return "Error in Theater update!"


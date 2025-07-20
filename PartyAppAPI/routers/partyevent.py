import sys

sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from database import engine, get_db
from models import Base, Gallery, PartyEvent
from logger import logger

router = APIRouter(
    prefix="/partyEvent",
    tags=["partyEvent"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreatePartyEvent(BaseModel):
    name: str
    description: str
    price: int
    image_path: str


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_all_party_event(db: db_dependency):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        eventList = db.query(PartyEvent).all()
        logger.info(f" eventList - {eventList}")

        if eventList is None:
            return logger.error("No Data found in Party Event")

        return eventList
    except Exception as e:
        logger.error("error in fetch All PartyEvents ", exc_info=e)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_party_event(user: user_dependency, db: db_dependency,
                       event_request: CreatePartyEvent):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        event_model = PartyEvent(**event_request.dict())
        #in case of foreign key key=user.get('id')

        logger.info(f"event_model - {event_model}")
        db.add(event_model)
        db.commit()
        return "Party event Created Successfully.."
    except Exception as e:
        logger.error("error in creating party event ", exc_info=e)
        return "Party_event creation Failed!"

@router.get("/get/{event_id}")
async def get_party_event(db: db_dependency, event_id: int):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        event = db.query(PartyEvent).filter(PartyEvent.id == event_id).first()
        logger.info(f"event - {event}")

        if event is None:
            return logger.error(f"Selected event_id is invalid data or no match found in DB for {event_id}")

        return event
    except Exception as e:
        logger.error(f"error in fetching event of {event_id} event id ", exc_info=e)
        return "error in fetching event of {event_id} event id "


@router.get("/getAll")
def get_party_event(db: db_dependency):
    return get_all_party_event(db)


@router.put("/update/{event_id}")
async def update_event(db: db_dependency,
                       event_request: CreatePartyEvent, event_id: int):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        event = db.query(PartyEvent).filter(PartyEvent.id == event_id).first()

        if event is None:
            return logger.error(f"Selected event_id is invalid data or no match found in DB for {event_id}")

        event.name = event_request.name
        event.description = event_request.description
        event.price = event_request.price
        event.image_path = event_request.image_path

        db.add(event)
        db.commit()
        return "Event update success.."
    except Exception as e:
        logger.error(f"error in updating event {event_id} in DB ", exc_info=e)
        return "Error in Event update!"

# write an delete event api
@router.delete("/delete/{event_id}")
async def delete_event(db: db_dependency, event_id: int):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        event = db.query(PartyEvent).filter(PartyEvent.id == event_id).first()

        if event is None:
            return logger.error(f"No match found in DB for id: {event_id}")
        else:
            # delete event_id
            print(event)
            db.delete(event)
            db.commit()
            return f"event {event_id} deleted.."
    except Exception as e:
        logger.error(f"error in deleting event {event_id} in DB ", exc_info=e)
        return "Error in event delete!"
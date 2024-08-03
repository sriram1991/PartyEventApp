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

router = APIRouter(
    prefix="/partyEvent",
    tags=["partyEvent"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreatePartyEvent(BaseModel):
    name: str
    description: str
    spacial_name: str
    spacial_other_name: str
    price: int
    image_path: str


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_all_party_event(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    eventList = db.query(PartyEvent).all()
    print(eventList)

    if eventList is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return eventList


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_party_event(user: user_dependency, db: db_dependency,
                       event_request: CreatePartyEvent):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    event_model = PartyEvent(**event_request.dict())
    #in case of foreign key key=user.get('id')

    print(str(event_model))
    db.add(event_model)
    db.commit()


@router.get("/getAll")
def get_party_event(user: user_dependency, db: db_dependency):
    return get_all_party_event(user, db)


@router.get("/get/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_slot(user: user_dependency, db: db_dependency, event_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    event = db.query(PartyEvent).filter(PartyEvent.id == event_id).first()

    if event is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return event


@router.put("/update/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_event(user: user_dependency, db: db_dependency,
                       event_request: CreatePartyEvent, event_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    event = db.query(PartyEvent).filter(PartyEvent.id == event_id).first()

    if event is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

    event.name = event_request.name
    event.description = event_request.description
    event.spacial_name = event_request.spacial_name
    event.spacial_other_name = event_request.spacial_other_name
    event.price = event_request.price
    event.image_path = event_request.image_path

    db.add(event)
    db.commit()

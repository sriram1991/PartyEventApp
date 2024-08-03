import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from routers.location import get_all_location
from database import engine, SessionLocal, get_db
from models import Base, Gallery

router = APIRouter(
    prefix="/theaters",
    tags=["theaters"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreateTheaters(BaseModel):
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
location_dependency = Annotated[dict, Depends(get_all_location)]



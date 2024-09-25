import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from database import engine, get_db
from models import Base, AddOns

router = APIRouter(
    prefix="/addon",
    tags=["addon"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreateAddon(BaseModel):
    name: str
    description: str
    type: str
    quantity: int
    price: int
    image_path: str
    is_available: bool


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_all_addons(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    addonList = db.query(AddOns).all()
    print(addonList)
    if addonList is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return addonList


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_addon(user: user_dependency, db: db_dependency, addon_request: CreateAddon):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    addon_model = AddOns(**addon_request.dict())
    db.add(addon_model)
    db.commit()


@router.get("/getAll")
def get_addons(user: user_dependency, db: db_dependency):
    return get_all_addons(user, db)


@router.get("/get/{addon_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_slot(user: user_dependency, db: db_dependency, addon_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    addon = db.query(AddOns).filter(AddOns.id == addon_id).first()

    if addon is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return addon


@router.put("/update/{addon_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_addons(user: user_dependency, db: db_dependency,
                       addon_request: CreateAddon, addon_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    addon = db.query(AddOns).filter(AddOns.id == addon_id).first()
    if addon is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

    addon.name = addon_request.name
    addon.description = addon_request.description
    addon.type = addon_request.type
    addon.quantity = addon_request.quantity
    addon.price = addon_request.price
    addon.image_path = addon_request.image_path
    addon.is_available = addon_request.is_available

    db.add(addon)
    db.commit()
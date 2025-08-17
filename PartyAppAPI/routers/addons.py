import sys
import os

import models
from logger import logger
from utils.constants import UPLOAD_DIR

sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File, Form
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
    price: int
    image_path: str
    is_available: bool


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_all_addons(db: db_dependency):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        addonList = db.query(AddOns).all()
        logger.info(f"addonList - {addonList}")

        if addonList is None:
            logger.error(f"No data found in AddOn.")
            return f"No data found in AddOn."

        return addonList
    except Exception as e:
        logger.error("error in fetch All AddOns ", exc_info=e)
        return "error in fetch All Addon"

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_addon(db: Session = Depends(get_db), name :str = Form(), description: str = Form(),
                 type: str = Form(), price: int = Form(),
                 is_available: bool = Form(), image_file: UploadFile = File(...)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        # addon_model = AddOns(**addon_request.dict())
        filename = image_file.filename
        logger.info(filename)
        print(image_file)
        print(image_file.filename)
        image_path = os.path.join(UPLOAD_DIR, filename)
        with open(image_path, "wb") as f:
            f.write(image_file.file.read())

        addon = models.AddOns(
            name=name,
            description=description,
            type=type,
            price=price,
            is_available=is_available,
            image_path=image_path
        )

        logger.info(addon)
        db.add(addon)
        db.commit()
        return "Addon Created Successfully.."
    except Exception as e:
        logger.error("error in creating Addons ", exc_info=e)
        return "Addon creation Failed!"

@router.get("/getAll")
def get_addons(db: db_dependency):
    return get_all_addons(db)


@router.get("/get/{addon_id}")
async def get_addons(db: db_dependency, addon_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        addon = db.query(AddOns).filter(AddOns.id == addon_id).first()
        logger.info(f"addon- {addon}")
        if addon is None:
            logger.error(f"Selected addon_id is invalid data or no match found in DB for {addon_id}")
            return f"Selected addon_id is invalid data or no match found in DB for {addon_id}"

        return addon
    except Exception as e:
        logger.error(f"error in fetch addon {addon_id} - ", exc_info=e)
        return f"error in fetch addon {addon_id} "

@router.put("/update/{addon_id}")
async def update_addons(db: db_dependency,
                       addon_request: CreateAddon, addon_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        addon = db.query(AddOns).filter(AddOns.id == addon_id).first()
        if addon is None:
            logger.error(f"Selected Gallery_id is invalid data or no match found in DB for {addon_id} to update")
            return f"Selected Gallery_id is invalid data or no match found in DB for {addon_id} to update"

        addon.name = addon_request.name
        addon.description = addon_request.description
        addon.type = addon_request.type
        addon.price = addon_request.price
        addon.image_path = addon_request.image_path
        addon.is_available = addon_request.is_available

        db.add(addon)
        db.commit()
        return "Addon update success.."
    except Exception as e:
        logger.error(f"error in updating addon {addon_id} - ", exc_info=e)
        return "Error in Addon update!"
    
    # write an delete addon api
@router.delete("/delete/{addon_id}")
async def delete_addon(db: db_dependency, addon_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        addon = db.query(AddOns).filter(AddOns.id == addon_id).first()
        if addon is None:
            logger.error(f"Selected addon_id is invalid data or no match found in DB for {addon_id} to delete")
            return f"Selected addon_id is invalid data or no match found in DB for {addon_id} to delete"

        db.delete(addon)
        db.commit()
        return "Addon deleted successfully.."
    except Exception as e:
        logger.error(f"error in deleting addon {addon_id} - ", exc_info=e)
        return "Error in Addon deletion!"

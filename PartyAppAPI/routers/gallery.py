import os
import sys
from pydoc import describe

from starlette.responses import JSONResponse

import models
from logger import logger
from utils.constants import UPLOAD_DIR

sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File, Form, Body
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from routers.theaters import get_all_theaters
from routers.location import getAllLocation
from database import engine, get_db
from models import Base, Gallery, Theater, Location, PartyEvent

router = APIRouter(
    prefix="/gallery",
    tags=["gallery"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreateGallery(BaseModel):
    name: str
    location: int
    theatre: int
    event_type: int
    description: str
    image_path: str


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
location_dependency = Annotated[dict, Depends(getAllLocation)]
theatre_dependency = Annotated[dict, Depends(get_all_theaters)]


@router.post("/createGallery", status_code=status.HTTP_201_CREATED)
async def saveDataToDB(db: Session = Depends(get_db), name :str = Form(), location: int = Form(),
                       theater: int = Form(), event_type: int= Form() ,description: str = Form(), image: UploadFile = File(...)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        filename = image.filename
        logger.info(filename)
        image_path = os.path.join(UPLOAD_DIR, filename)
        with open(image_path, "wb") as f:
            f.write(image.file.read())

        logger.info(name)
        logger.info(location)
        logger.info(theater)
        logger.info(description)
        logger.info(image_path)

        gallery = models.Gallery(
            name=name,
            location=location,
            theater=theater,
            event_type=event_type,
            description=description,
            image_path=image_path
        )

        db.add(gallery)
        db.commit()

        return "success"
    except Exception as e:
        logger.error("error in Uploading Image ", exc_info=e)


# # @router.get("/checkIsFileExist")
# async def read_upload_image(file_name):
#     try:
#         file_path = UPLOAD_DIR + file_name #'2018-03-04-16-28-07-031.jpg'
#         """
#         Read the uploaded images.
#         :return: A JSON response with a list of uploaded image filenames
#         """
#         # Get a list of uploaded image filenames
#         filenames = os.listdir(file_path)
#         return JSONResponse(content={"filenames": filenames}, media_type="application/json")
#     except Exception as e:
#         logger.error("error in Uploading Image ", exc_info=e)
#
@router.get("/galleryByLocationByTheatreByEventType/{location_id}/{theater_id}/{event_type}")
def get_gallery_by_location_by_theater_by_eventType(db: db_dependency, location_id: Optional[int] = None,
                                                    theater_id: Optional[int] = None, event_type: Optional[int] = None):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        logger.info(Gallery.location)
        logger.info(Gallery.theater)

        galleryList = db.query(Gallery).filter(Gallery.location == location_id,
            Gallery.theater == theater_id, Gallery.event_type == event_type).all()

        logger.info(f"galleryList by Location: {location_id} - Theater: {theater_id} - list:  {galleryList}")

        if galleryList is None:
            return logger.error(f"Selected id is invalid or no match found in DB for Theater Id: {theater_id} and Location Id: {location_id}")
        return galleryList
    except Exception as e:
        logger.error("error in fetch Gallery ", exc_info=e)

@router.get("/getAll")
def get_gallery(db: db_dependency):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        galleryList = db.query(Gallery).all()
        logger.info(f"galleryList -- {galleryList}")

        if galleryList is None:
            return logger.error("No Data found in Gallery")

        return galleryList
    except Exception as e:
        logger.error("error in fetch All Gallery Images ", exc_info=e)


# @router.post("/uploadFile")
# async def uploadFile(image: UploadFile = File(...)):
#     try:
#         filename = image.filename
#         filepath = os.path.join(UPLOAD_DIR, filename)
#         with open(filepath, "wb") as f:
#             f.write(image.file.read())
#
#         # Return a JSON response
#         return JSONResponse(content={"filename": filename}, media_type="application/json")
#     except Exception as e:
#         logger.error("error Uploading a Image ", exc_info=e)
#
@router.get("/get/{gallery_id}")
def get_gallery(db: db_dependency, gallery_id: int):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        logger.info(gallery)
        if gallery is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return gallery
    except Exception as e:
        logger.error("error in fetch Gallery ", exc_info=e)

@router.put("/update/{gallery_id}")
async def update_gallery(db: db_dependency, gallery_request: CreateGallery, gallery_id: int):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        logger.info(gallery.name)
        if gallery is None:
            return logger.error(f"Selected Gallery_id is invalid data or no match found in DB for {gallery_id}")

        gallery.name = gallery_request.name
        gallery.location = gallery_request.location
        gallery.theater = gallery_request.theater
        gallery.description = gallery_request.description

        db.add(gallery)
        db.commit()
        return "Gallery update success.."
    except Exception as e:
        logger.error("error occurred while updating Image info ", exc_info=e)
        return "Error in Gallery update!"
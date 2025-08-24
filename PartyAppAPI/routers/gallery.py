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
    theater: int
    event_type: int
    description: str
    image_path: str


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
location_dependency = Annotated[dict, Depends(getAllLocation)]
theater_dependency = Annotated[dict, Depends(get_all_theaters)]


@router.post("/createGallery", status_code=status.HTTP_201_CREATED)
async def saveDataToDB(db: Session = Depends(get_db), name :str = Form(), location: int = Form(),
                       theater: int = Form(), event_type: int= Form() ,description: str = Form(),
                       image: UploadFile = File(None)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        if image and image.filename:
            file_content = image.file.read()
            if len(file_content) > 1024 * 1024:  # 1MB
                raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                  detail='Image size must be less than 1MB')
            filename = image.filename
            logger.info(filename)
            image_path = os.path.join(UPLOAD_DIR, filename)
            with open(image_path, "wb") as f:
                f.write(file_content)
        else:
            image_path = None
            logger.info('No image file provided')

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

        return "Gallery Created Successfully.."
    except Exception as e:
        logger.error("error in Uploading Image ", exc_info=e)
        return "Gallery creation Failed!"


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
@router.get("/galleryByLocationByTheaterByEventType/{location_id}/{theater_id}/{event_type}")
def get_gallery_by_location_by_theater_by_eventType(db: db_dependency, location_id: int, theater_id: int, event_type: int):
    try:
        galleryList = db.query(Gallery).filter(
            Gallery.location == location_id,
            Gallery.theater == theater_id, 
            Gallery.event_type == event_type
        ).all()

        if not galleryList:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"No gallery found for location {location_id}, theater {theater_id}, event {event_type}")
        return galleryList
    except Exception as e:
        logger.error("error in fetch Gallery ", exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching gallery")


@router.get("/getAll")
def get_gallery(db: db_dependency):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        galleryList = db.query(Gallery).all()
        logger.info(f"galleryList -- {galleryList}")

        if galleryList is None:
            logger.error("No Data found in Gallery")
            return "No Data found in Gallery"

        return galleryList
    except Exception as e:
        logger.error("error in fetch All Gallery Images ", exc_info=e)
        return "Error in fetch All Gallery Images"


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
            logger.error(f"Selected id is invalid data or no match found in DB for {gallery_id}")
            # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            #                     detail='Could not validate user.')
        return gallery
    except Exception as e:
        logger.error("error in fetch Gallery ", exc_info=e)
        return "Error in fetch Gallery"

@router.put("/update/{gallery_id}")
async def update_gallery(db: db_dependency, gallery_id: int = Path(gt=0),
                        name: str = Form(), location: int = Form(),
                        theater: int = Form(), event_type: int = Form(),
                        description: str = Form(), image_file: UploadFile = File(None)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')

        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery is None:
            logger.error(f"Selected Gallery_id is invalid data or no match found in DB for {gallery_id}")
            return f"Selected Gallery_id is invalid data or no match found in DB for {gallery_id}"

        if image_file and image_file.filename:
            file_content = image_file.file.read()
            if len(file_content) > 1024 * 1024:  # 1MB
                raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                  detail='Image size must be less than 1MB')
            filename = image_file.filename
            logger.info(f'Processing image file: {filename}')
            image_path = os.path.join(UPLOAD_DIR, filename)
            with open(image_path, "wb") as f:
                f.write(file_content)
            gallery.image_path = image_path
            logger.info(f'Image saved to: {image_path}')
        else:
            logger.info('No image file provided or filename is empty')

        gallery.name = name
        gallery.location = location
        gallery.theater = theater
        gallery.event_type = event_type
        gallery.description = description

        db.add(gallery)
        db.commit()
        return "Gallery update success.."
    except Exception as e:
        logger.error("error occurred while updating Image info ", exc_info=e)
        return "Error in Gallery update!"


@router.delete("/delete/{gallery_id}")
async def delete_gallery(db: db_dependency, gallery_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
        if gallery is None:
            logger.error(f"No match found in DB for id: {gallery_id}")
            return f"No match found in DB for id: {gallery_id}"
        else:
            # delete gallery_id
            logger.info(f"Gallery id {gallery_id} got deleted!")
            db.delete(gallery)
            db.commit()
            return f"gallery {gallery_id} deleted.."
    except Exception as e:
        logger.error(f"error in deleting event {gallery_id} in DB ", exc_info=e)
        return "Error in gallery delete!"
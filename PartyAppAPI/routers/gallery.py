import os
import sys

from starlette.responses import JSONResponse

from utils.constants import UPLOAD_DIR

sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from routers.auth import get_current_user
from routers.theaters import get_all_theaters
from routers.location import get_all_location
from database import engine, get_db
from models import Base, Gallery, Theater, Location

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
    description: str
    image_path: str


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
location_dependency = Annotated[dict, Depends(get_all_location)]
theatre_dependency = Annotated[dict, Depends(get_all_theaters)]


# @router.get("/checkIsFileExist")
async def read_upload_image(file_name):
    file_path = UPLOAD_DIR + file_name #'2018-03-04-16-28-07-031.jpg'
    """
    Read the uploaded images.
    :return: A JSON response with a list of uploaded image filenames
    """
    # Get a list of uploaded image filenames
    filenames = os.listdir(file_path)
    return JSONResponse(content={"filenames": filenames}, media_type="application/json")


@router.get("/galleryByLocationByTheatre/{location_id}/{theater_id}")
def get_gallery_by_location_by_theater(db: db_dependency, location_id: int = Path(gt=0), theater_id: int = Path(gt=1)):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Could not validate user.')
    galleryList = (db.query(Gallery).filter(Location.id == location_id).
                   filter(Theater.id == theater_id).all())

    print(galleryList)
    if galleryList is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return galleryList

@router.get("/getAll")
def get_gallery(db: db_dependency):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Could not validate user.')
    galleryList = db.query(Gallery).all()
    print(galleryList)
    if galleryList is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return galleryList


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_gallery(user: user_dependency, db: db_dependency,
                    location: location_dependency, gallery_request: CreateGallery):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    gallery_model = Gallery(**gallery_request.dict())
    #in case of foreign key key=user.get('id')

    print(str(gallery_model))
    db.add(gallery_model)
    db.commit()


@router.post("/uploadFile")
async def uploadFile(image: UploadFile = File(...)):
    filename = image.filename
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(image.file.read())

    # Return a JSON response
    return JSONResponse(content={"filename": filename}, media_type="application/json")


@router.get("/get/{gallery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_gallery(db: db_dependency, gallery_id: int = Path(gt=0)):
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail='Could not validate user.')
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()

    if gallery is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return gallery


@router.put("/update/{gallery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_gallery(user: user_dependency, db: db_dependency,
                         gallery_request: CreateGallery, gallery_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()

    if gallery is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

    gallery.name = gallery_request.name
    gallery.location = gallery_request.location
    gallery.theatre = gallery_request.theatre
    gallery.description = gallery_request.description
    gallery.image_path = gallery_request.image_path

    db.add(gallery)
    db.commit()

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


def get_all_gallery(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    galleryList = db.query(Gallery).all()
    print(galleryList)
    if galleryList is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return galleryList

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_location(user: user_dependency, db: db_dependency,
                    location: location_dependency, gallery_request: CreateGallery):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    gallery_model = Gallery(**gallery_request.dict())
    #in case of foreign key key=user.get('id')

    print(str(gallery_model))
    db.add(gallery_model)
    db.commit()


@router.get("/getAll")
def get_gallery(user: user_dependency, db: db_dependency):
    return get_all_gallery(user, db)


@router.get("/get/{gallery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_slot(user: user_dependency, db: db_dependency, gallery_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()

    if gallery is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    return gallery
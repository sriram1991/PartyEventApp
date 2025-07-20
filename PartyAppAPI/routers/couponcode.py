import sys
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from logger import logger

from database import engine, get_db
from models import Base, CouponCode
from routers.auth import get_current_user
from fastapi import HTTPException
from pathlib import Path

sys.path.append("..")


router = APIRouter(
    prefix="/coupon_code",
    tags=["coupon_code"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)


class CreateCoupon(BaseModel):
    name: str
    unique_code: str
    discount: int
    is_active: bool


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_all_coupon(db: db_dependency):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        couponList = db.query(CouponCode).all()

        if couponList is None:
            return logger.error("No Data found in coupon")
            logger.info(f"couponList -- {couponList}")

        return couponList
    except Exception as e:
        logger.error("error in fetch All Co ", exc_info=e)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_coupon(db: db_dependency,
                        coupon_request: CreateCoupon):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        coupon_model = CouponCode(**coupon_request.dict())
        #in case of foreign key key=user.get('id')

        logger.info(coupon_model)
        db.add(coupon_model)
        db.commit()
        return "coupon Created Successfully.."
    except Exception as e:
        logger.info("error in creating Theater ", exc_info=e)
        return "coupon creation Failed!" 

@router.get("/getAll")
def get_theaters(db: db_dependency):
    return get_all_coupon(db)



@router.get("/get/{coupon_id}")
def get_coupon(db: db_dependency, coupon_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        coupon = db.query(CouponCode).filter(CouponCode.id == coupon_id).first()
        logger.info(coupon)
        if coupon is None:
            return logger.error(f"Selected id is invalid data or no match found in DB for {coupon_id}")
        return coupon
    except Exception as e:
        logger.error("error in fetch All Theaters ", exc_info=e)
        return "Error in fetch All Theaters"

@router.put("/update/{coupon_id}")
async def update_coupon(db: db_dependency,
                        coupon_request: CreateCoupon, coupon_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        coupon = db.query(CouponCode).filter(CouponCode.id == coupon_id).first()

        if coupon is None:
            return logger.error(f"Selected id is invalid data or no match found in DB for {coupon_id}")

        coupon.name = coupon_request.name
        coupon.uniqu_code = coupon_request.uniqu_code
        coupon.discount = coupon_request.discount
        coupon.is_active = coupon_request.is_active
        
        db.add(coupon)
        db.commit()
        return "coupon update success.."
    except Exception as e:
        logger.error(f"error in updating event {coupon_id} in DB ", exc_info=e)
        return "Error in coupon update!"


@router.delete("/delete/{coupon_id}")
def delete_coupon(db: db_dependency, coupon_id: int = Path(gt=0)):
    try:
        # if user is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                         detail='Could not validate user.')
        coupon = db.query(CouponCode).filter(CouponCode.id == coupon_id).first()
        if coupon is None:
            print("No coupon found...")
            return logger.error(f"No match found in DB for id: {coupon_id}")
        else:
            print(coupon.id)
            # delete coupon_id
            db.delete(coupon)
            db.commit()
            print("coupon")
            print(coupon)
            return f"coupon {coupon_id} deleted success.."
    except Exception as e:
        logger.error(f"error in deleting event {coupon_id} in DB ", exc_info=e)
        return "Error in coupon delete!"



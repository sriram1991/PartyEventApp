import sys

from logger import logger

sys.path.append("..")

from fastapi import APIRouter, Body, Depends, Request, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from passlib.context import CryptContext
from datetime import timedelta, datetime
from typing import Annotated
from jwt import PyJWTError
import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging

from database import SessionLocal, engine, get_db
from models import Users, Base

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

Base.metadata.create_all(bind=engine)

# text:secret partyapp --key: PartyApp
SECRET_KEY = '881ea7a96025def01f2cc24e68e0e06666eedfa45d34c902ef1fa064524676a2'
ALGO = 'HS256'

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str
    role: str
    is_active: bool
    mobile: str


db_dependency = Annotated[Session, Depends(get_db)]


def get_password_hash(password):
    return bcrypt_context.hash(password)


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    try:
        encode = {'sub': username, 'id': user_id}
        expires = datetime.utcnow() + expires_delta
        encode.update({'exp': expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGO)
    except Exception as e:
        logger.error(f"error creating access_token - ", exc_info=e)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except PyJWTError as e:
        logger.error(f"Could not validate user. - ", exc_info=e)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def reg_user(db: db_dependency, create_user: CreateUserRequest):
    try:
        create_user = Users(
            username=create_user.username,
            password=bcrypt_context.hash(create_user.password),
            email=create_user.email,
            role=create_user.role,
            is_active=create_user.is_active,
            mobile=create_user.mobile
        )

        validate_username = db.query(Users).filter(Users.username == create_user.username).first()
        validate_email = db.query(Users).filter(Users.email == create_user.email).first()
        validate_mobile = db.query(Users).filter(Users.mobile == create_user.mobile).first()
        logger.info(create_user.password)
        logger.info(validate_username)
        logger.info(validate_email)
        logger.info(validate_mobile)

        if create_user.password and (
                validate_username is not None or validate_email is not None or validate_mobile is not None):
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail='Username or Email already exist')

        db.add(create_user)
        db.commit()
        return "User creation Success..."
    except Exception as e:
        logger.error(f"Error occurred while user creation - ", exc_info=e)
        return "User creation Failed!"

def authenticate_user(username: str, password: str, db):
    try:
        user = db.query(Users).filter(Users.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Please provide a valid username.')

        if not bcrypt_context.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Please provide a valid Password.')
        return user
    except Exception as e:
        logger.error(f"Could not Authenticate user - ", exc_info=e)
        return "User Authentication Failed!"

@router.post("/login")
def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        token = create_access_token(user.username, user.id, timedelta(minutes=20))

        return {'access_token': token, 'token_type': 'bearer'}
    except Exception as e:
        logger.error(f"Error occurred in Authenticating user. - ", exc_info=e)

@router.put("/updateUser/{user_id}")
def update_user(user: get_current_user, db: db_dependency, user_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        db_user = db.query(Users).filter(user.username == user_id).first()

        db_user.email = user.email
        db_user.mobile = user.mobile
        db.add(db_user)
        db.commit()
        return "User update success.."
    except Exception as e:
        logger.error(f"error in updating user {user_id} - ", exc_info=e)
        return "User update Failed!"

@router.get("/getUser/{user_id}")
def get_user(user: get_current_user, db: db_dependency, user_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        db_user = db.query(Users).filter(user.username == user_id).first()

        return db_user
    except Exception as e:
        logger.error(f"error in updating user {user_id} - ", exc_info=e)
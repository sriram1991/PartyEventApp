import sys
sys.path.append("..")

from fastapi import APIRouter, Body, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from passlib.context import CryptContext
from datetime import timedelta, datetime
from typing import Annotated
from jwt import PyJWTError
import jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from PartyApp.database import SessionLocal, engine
from PartyApp.models import Users, Base

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


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def get_password_hash(password):
    return bcrypt_context.hash(password)


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGO)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


@router.post("/register", status_code=status.HTTP_201_CREATED)
def reg_user(db: db_dependency, create_user: CreateUserRequest):
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

    if create_user.password or validate_username is not None or validate_email is not None:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail='Username or Email already exist')

    db.add(create_user)
    db.commit()


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False

    if not bcrypt_context.verify(password, user.password):
        return False
    return user


@router.post("/token")
def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

# @router.post("/register1")
# def register_user(request: Request, obj=Body(), db: SessionLocal = Depends(get_db)):
#     print("-------------------------0")
#     print(request)
#     print("-------------------------1")
#     print(obj)
# validation1 = db.query(models.Users).filter(models.Users.username == obj.username).first()
# validation2 = db.query(models.Users).filter(models.Users.email == obj.newemail).first()

# if obj.password != obj.password2 or validation1 is not None or validation2 is not None:
#     msg = "Invalid registration request"
#     return {"request": request, "msg": msg}

# user_model = models.Users()
# user_model.username = obj.username
# user_model.email = obj.email
# user_model.first_name = obj.firstname
# user_model.last_name = obj.lastname
#
# hash_password = get_password_hash(obj.password)
# user_model.hashed_password = hash_password
# user_model.is_active = True
#
# db.add(user_model)
# db.commit()
#
# print(user_model.username)
# msg = "User successfully created"
# return {"status": status.HTTP_201_CREATED, "msg": msg}

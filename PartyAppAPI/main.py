from fastapi import FastAPI
import models
from database import engine
from routers import auth, couponcode, location, gallery, theaters, slots, addons, partyevent, eventbookings
from logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
logger.debug('Main class of API started.....')

models.Base.metadata.create_all(bind=engine)

# cors issue fix
origins = [
    "https://ebfuncity.com",
    "https://ebfuncity.com:8000",
    "https://ebfuncity.com:8000/*",
    "https://ebfuncity.com:8000/auth/login",
]

#mount the Images via static/images
app.mount("/static/images", StaticFiles(directory="static/images"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(location.router)
app.include_router(theaters.router)
app.include_router(gallery.router)
app.include_router(slots.router)
app.include_router(addons.router)
app.include_router(partyevent.router)
app.include_router(eventbookings.router)
app.include_router(couponcode.router)

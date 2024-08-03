from fastapi import FastAPI
import models
from database import engine
from routers import auth, location, gallery, theaters, slots, addons, partyevent

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(location.router)
app.include_router(theaters.router)
app.include_router(gallery.router)
app.include_router(slots.router)
app.include_router(addons.router)
app.include_router(partyevent.router)

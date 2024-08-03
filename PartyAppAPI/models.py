from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date, datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    role = Column(String)
    is_active = Column(Boolean)
    mobile = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    pincode = Column(Integer, nullable=False)
    city = Column(String)
    state = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Theater(Base):
    __tablename__ = 'theaters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    no_of_peoples = Column(Integer)
    extra_cost_each_person = Column(Integer)
    location = Column(Integer, ForeignKey('location.id'))
    no_of_slots = Column(Integer)
    slots = Column(Integer, ForeignKey('slots.id'))
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class PartyEvent(Base):
    __tablename__ = 'party_event'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    spacial_name = Column(String)
    spacial_other_name = Column(String)
    price = Column(Integer)
    image_path = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class AddOns(Base):
    __tablename__ = 'addons'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    type = Column(String)
    quantity = Column(Integer)
    price = Column(Integer)
    image_path = Column(String)
    is_available = Column(Boolean)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Gallery(Base):
    __tablename__ = 'gallery'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(Integer, ForeignKey("location.id"))
    theater = Column(Integer, ForeignKey("theater.id"))
    description = Column(String)
    image_path = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Slots(Base):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True, index=True)
    slot_time_duration = Column(String)
    slot_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean)
    theatre = Column(Integer, ForeignKey('theatre.id'))
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class BookingEntry(Base):
    __tablename__ = 'booking_entry'

    id = Column(Integer, primary_key=True, index=True)
    price_total = Column(Integer)
    theatre = Column(Integer, ForeignKey('theatre.id'))
    location = Column(Integer, ForeignKey('location.id'))
    party_event_selected = Column(Integer, ForeignKey('party_event.id'))
    date = Column(DateTime, default=datetime.utcnow)
    slot = Column(Integer, ForeignKey('slots.id'))
    no_of_peoples = Column(Integer)
    addons_selected = Column(String)
    booking_name = Column(String)
    booking_mobile = Column(Integer)
    booking_email = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

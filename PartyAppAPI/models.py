from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date, datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), unique=True)
    password = Column(String(150))
    email = Column(String(50), unique=True)
    role = Column(String(10))
    is_active = Column(Boolean)
    mobile = Column(String(10))
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(100), nullable=True)
    address = Column(String(100))
    pincode = Column(Integer, nullable=False)
    city = Column(String(15))
    state = Column(String(25))
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Theater(Base):
    __tablename__ = 'theater'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(25))
    description = Column(String(100), nullable=True)
    price = Column(Integer)
    no_of_peoples = Column(Integer)
    is_active = Column(Boolean)
    # event_type = Column(Integer, ForeignKey('party_event.id'))
    extra_cost_each_person = Column(Integer)
    location = Column(Integer, ForeignKey('location.id'))
    no_of_slots = Column(Integer)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class PartyEvent(Base):
    __tablename__ = 'party_event'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(25))
    description = Column(String(100), nullable=True)
    price = Column(Integer)
    image_path = Column(String(100), nullable=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class AddOns(Base):
    __tablename__ = 'addons'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(25))
    description = Column(String(100), nullable=True)
    type = Column(String(25))
    price = Column(Integer)
    image_path = Column(String(100), nullable=True)
    is_available = Column(Boolean)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Gallery(Base):
    __tablename__ = 'gallery'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(25))
    location = Column(Integer, ForeignKey("location.id"))
    theater = Column(Integer, ForeignKey("theater.id"))
    event_type = Column(Integer, ForeignKey("party_event.id"))
    description = Column(String(100), nullable=True)
    image_path = Column(String(100), nullable=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class Slots(Base):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slot_time_duration = Column(String(25))
    slot_date = Column(DateTime, default=datetime.utcnow)
    location = Column(Integer, ForeignKey("location.id"))
    theater = Column(Integer, ForeignKey("theater.id"))
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class CouponCode(Base):
    __tablename__ = 'coupon_code'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(25))
    unique_code = Column(String(25), unique=True)
    discount = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

class BookingEntry(Base):
    __tablename__ = 'booking_entry'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    total_amount = Column(Integer)
    theater = Column(Integer, ForeignKey('theater.id'))
    location = Column(Integer, ForeignKey('location.id'))
    party_event_selected = Column(Integer, ForeignKey('party_event.id'))
    date = Column(DateTime, default=datetime.utcnow)
    slot = Column(Integer, ForeignKey('slots.id'))
    no_of_peoples = Column(Integer, default=1, nullable=True)
    first_spacial_name = Column(String(100), nullable=True, default=null)
    second_spacial_name = Column(String(100), nullable=True, default=null)
    addons_selected = Column(String(50))
    booking_name = Column(String(100))
    booking_mobile = Column(String(15))
    booking_email = Column(String(100), nullable=True, default=null)
    advance_amount = Column(Integer, nullable=True, default=0)
    is_active = Column(Boolean, default=True, nullable=True)
    discount_coupon = Column(String(50), nullable=True, default=null)
    referral_code = Column(String(50), nullable=True, default=null)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    income = Column(Float)
    purpose = Column(String)
    applications = relationship("Application", back_populates="user")

class Scheme(Base):
    __tablename__ = "schemes"
    scheme_id = Column(Integer, primary_key=True, index=True)
    scheme_name = Column(String)
    category = Column(String)
    min_income = Column(Float)
    max_loan = Column(Float)
    interest_rate = Column(Float)

class Partner(Base):
    __tablename__ = "partners"
    partner_id = Column(Integer, primary_key=True, index=True)
    partner_name = Column(String)
    location = Column(String)
    type = Column(String)

class Application(Base):
    __tablename__ = "applications"
    application_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    scheme_id = Column(Integer, ForeignKey("schemes.scheme_id"))
    partner_id = Column(Integer, ForeignKey("partners.partner_id"))
    status = Column(String, default="pending")
    user = relationship("User", back_populates="applications")
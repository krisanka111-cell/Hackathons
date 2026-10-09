from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SchemeMatch API")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def seed_data():
    db = database.SessionLocal()
    if not db.query(models.Scheme).first():
        schemes = [
            models.Scheme(scheme_name="Education Loan Support", category="education", min_income=0, max_loan=500000, interest_rate=7.5),
            models.Scheme(scheme_name="Micro Enterprise Support", category="business", min_income=0, max_loan=200000, interest_rate=6.5),
            models.Scheme(scheme_name="Term Loan Scheme", category="business", min_income=0, max_loan=1000000, interest_rate=8.5),
        ]
        partners = [
            models.Partner(partner_name="PSB Education Desk", location="Mumbai", type="PSB"),
            models.Partner(partner_name="SCA Partner", location="Guwahati", type="SCA"),
            models.Partner(partner_name="NBFC-MFI", location="Jorhat", type="NBFC"),
        ]
        db.add_all(schemes)
        db.add_all(partners)
        db.commit()
    db.close()

@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/schemes/", response_model=List[schemas.SchemeOut])
def list_schemes(db: Session = Depends(get_db)):
    return db.query(models.Scheme).all()

@app.get("/partners/", response_model=List[schemas.PartnerOut])
def list_partners(db: Session = Depends(get_db)):
    return db.query(models.Partner).all()

@app.post("/applications/")
def create_application(app_in: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    db_app = models.Application(**app_in.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return {"message": "Application created", "application_id": db_app.application_id}
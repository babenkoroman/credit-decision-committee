from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.infrastructure.db.session import get_db

from src.schemas import ApplicationDTO

router = APIRouter()

import time 

@router.get("/")
def index():
    return {"message": "OK"}


@router.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "ok"}

from src.services.application import ApplicationService

@router.post("/application")
def application(application: ApplicationDTO): 
    start_time = time.perf_counter()
    service = ApplicationService(application)
    res = service.process()
    end_time = time.perf_counter()
    print(f'Время выполнения: {end_time - start_time:.4f} сек.')
    return res
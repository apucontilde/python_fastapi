from datetime import date
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Compensation
from app.settings import DATABASE_URL


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# def recreate_database():
#     # Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)


# recreate_database()

app = FastAPI(title="FastAPI CompensationsAPI", version="1.0.0")


@app.get("/")
def root():
    return {"message": "hiya"}


@app.post("/compensations")
def create_compensation(role_title: str, salary_p_year: int):
    with Session.begin() as session:
        session.begin()
        compensation = Compensation(role_title=role_title, salary_p_year=salary_p_year)
        session.add(compensation)
    return JSONResponse(
        status_code=200, content={"compensationId": compensation.id}
    )


@app.get("/compensations/{id}")
def find_compensation(id: int):
    with Session.begin() as session:
        compensation = session.query(Compensation).filter(Compensation.id == id).first()
    return JSONResponse(status_code=200, content={"compensation" : jsonable_encoder(compensation)})


@app.get("/compensations")
def get_compensations(page_size: int = 10, page: int = 1):
    if page_size > 100 or page_size < 0:
        page_size = 100

    with Session.begin() as session:
        compensations = session.query(Compensation).limit(page_size).offset((page - 1) * page_size).all()

    return JSONResponse(status_code=200, content={"compensations": jsonable_encoder(compensations), "page": page, "size": len(compensations)})


@app.delete("/compensations")
def delete_compensation(id: int):
    with Session.begin() as session:
        compensation = session.query(Compensation).get(id)
        session.delete(compensation)

    return JSONResponse(
        status_code=200, content={"message": "deleted succesfuly"}
    )

@app.exception_handler(Exception)
def exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"request": jsonable_encoder(request), "exception": jsonable_encoder(exc)},
    )



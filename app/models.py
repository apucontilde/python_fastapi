from typing import List
from sqlalchemy import Integer, String, DateTime, func as db_func, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column

class Base(DeclarativeBase):
    __abstract__ = True
    
    created_on = mapped_column(DateTime, default=db_func.now())
    updated_on = mapped_column(DateTime, default=db_func.now(), onupdate=db_func.now())
    
class Currency(Base):
    __tablename__ = "currency"
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[String] = mapped_column(String, required=True)
    max_decimals: Mapped[Integer] = mapped_column(Integer, required=True)

class Benefits(Base):
    __tablename__ = "benefits"
    benefit_desc: Mapped[String] = mapped_column(String, primary_key=True)

association_table = Table(
    "association_table",
    Base.metadata,
    mapped_column("benefit_id", ForeignKey("Benefits.id"), primary_key=True),
    mapped_column("compensentaion_id", ForeignKey("Compensation.id"), primary_key=True),
)

class Compensation(Base):
    __tablename__ = "compensation"
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_title: Mapped[String] = mapped_column(String, required=True)
    company_id: Mapped[Integer] =  mapped_column(ForeignKey("Company.id"))
    salary_p_year: Mapped[Integer] = mapped_column(Integer, required=True)
    currency_id: Mapped[Integer] =  mapped_column(ForeignKey("Currency.id"))
    currency: Mapped[Currency] = relationship()
    benefits: Mapped[List[Benefits]] = relationship(
        secondary=association_table, back_populates="compensation"
    )
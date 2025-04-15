from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Employee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    department = relationship("Department", backref="employees")
    job = relationship("Job", backref="employees")
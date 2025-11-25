from pydantic import BaseModel, Field, validator
from typing import List
from uuid import uuid4

class Student(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    grades: List[float] = Field(..., min_items=5, max_items=5)
    attendance: float = Field(..., ge=0, le=100)

    @validator('grades')
    def validate_grades(cls, v):
        if not all(0 <= grade <= 10 for grade in v):
            raise ValueError('Todas as notas devem estar entre 0 e 10')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva",
                "grades": [7.5, 8.0, 6.5, 9.0, 7.0],
                "attendance": 85.0
            }
        }

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    grades: List[float] = Field(..., min_items=5, max_items=5)
    attendance: float = Field(..., ge=0, le=100)

    @validator('grades')
    def validate_grades(cls, v):
        if not all(0 <= grade <= 10 for grade in v):
            raise ValueError('Todas as notas devem estar entre 0 e 10')
        return v

class StudentUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    grades: List[float] = Field(..., min_items=5, max_items=5)
    attendance: float = Field(..., ge=0, le=100)

    @validator('grades')
    def validate_grades(cls, v):
        if not all(0 <= grade <= 10 for grade in v):
            raise ValueError('Todas as notas devem estar entre 0 e 10')
        return v

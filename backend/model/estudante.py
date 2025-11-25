from pydantic import BaseModel, Field, validator
from typing import List
from uuid import uuid4


class Estudante(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    nome: str = Field(..., min_length=1, max_length=100)
    notas: List[float] = Field(..., min_items=5, max_items=5)
    frequencia: float = Field(..., ge=0, le=100)

    @validator("notas")
    def validar_notas(cls, valores):
        if not all(0 <= nota <= 10 for nota in valores):
            raise ValueError("Todas as notas devem estar entre 0 e 10")
        return valores

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João Silva",
                "notas": [7.5, 8.0, 6.5, 9.0, 7.0],
                "frequencia": 85.0,
            }
        }


class CriarEstudante(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    notas: List[float] = Field(..., min_items=5, max_items=5)
    frequencia: float = Field(..., ge=0, le=100)

    @validator("notas")
    def validar_notas(cls, valores):
        if not all(0 <= nota <= 10 for nota in valores):
            raise ValueError("Todas as notas devem estar entre 0 e 10")
        return valores


class AtualizarEstudante(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    notas: List[float] = Field(..., min_items=5, max_items=5)
    frequencia: float = Field(..., ge=0, le=100)

    @validator("notas")
    def validar_notas(cls, valores):
        if not all(0 <= nota <= 10 for nota in valores):
            raise ValueError("Todas as notas devem estar entre 0 e 10")
        return valores

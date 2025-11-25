from fastapi import APIRouter, HTTPException, status
from typing import List
from model.student import Estudante, criarEstudante, EstudanteUpdate
from service.student_service import student_service

router = APIRouter()

@router.post("/students", response_model=Estudante, status_code=status.HTTP_201_CREATED)
def create_student(student: criarEstudante):
    """Cria um novo aluno"""
    return student_service.create_student(student)

@router.get("/students", response_model=List[Estudante])
def get_students():
    """Lista todos os alunos"""
    return student_service.get_all_students()

@router.get("/students/{student_id}", response_model=Estudante)
def get_student(student_id: str):
    """Retorna um aluno específico"""
    student = student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return student

@router.put("/students/{student_id}", response_model=Estudante)
def update_student(student_id: str, student_data: EstudanteUpdate):
    """Atualiza um aluno existente"""
    student = student_service.update_student(student_id, student_data)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return student

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str):
    """Remove um aluno"""
    if not student_service.delete_student(student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return None

@router.get("/report")
def get_report():
    """Retorna relatório completo com todas as estatísticas"""
    return student_service.get_report()

@router.get("/report/class-average")
def get_class_average():
    """Retorna a média geral da turma"""
    return {
        "class_average": student_service.calculate_class_average()
    }

@router.get("/report/class-average-per-subject")
def get_class_average_per_subject():
    """Retorna a média da turma em cada disciplina"""
    return {
        "averages": student_service.calculate_class_average_per_subject()
    }

@router.get("/report/students-above-average")
def get_students_above_average():
    """Retorna alunos com média acima da média da turma"""
    return {
        "students": student_service.get_students_above_average()
    }

@router.get("/report/students-below-attendance")
def get_students_below_attendance():
    """Retorna alunos com frequência abaixo de 75%"""
    return {
        "students": student_service.get_students_below_attendance_threshold()
    }

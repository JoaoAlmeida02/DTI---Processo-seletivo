from fastapi import APIRouter, HTTPException, status
from typing import List

from model.estudante import AtualizarEstudante, CriarEstudante, Estudante
from service.estudanteService import estudante_service

router = APIRouter()


@router.post("/estudantes", response_model=Estudante, status_code=status.HTTP_201_CREATED)
def criar_estudante(estudante: CriarEstudante):
    return estudante_service.criar_estudante(estudante)


@router.get("/estudantes", response_model=List[Estudante])
def listar_estudantes():
    return estudante_service.listar_estudantes()


@router.get("/estudantes/{estudante_id}", response_model=Estudante)
def obter_estudante(estudante_id: str):
    estudante = estudante_service.obter_estudante_por_id(estudante_id)
    if not estudante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado",
        )
    return estudante


@router.put("/estudantes/{estudante_id}", response_model=Estudante)
def atualizar_estudante(estudante_id: str, dados_estudante: AtualizarEstudante):
    estudante = estudante_service.atualizar_estudante(estudante_id, dados_estudante)
    if not estudante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado",
        )
    return estudante


@router.delete("/estudantes/{estudante_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_estudante(estudante_id: str):
    if not estudante_service.remover_estudante(estudante_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado",
        )
    return None


@router.get("/relatorios")
def gerar_relatorio():
    return estudante_service.gerar_relatorio()


@router.get("/relatorios/media-turma")
def obter_media_turma():
    return {"media_turma": estudante_service.calcular_media_turma()}


@router.get("/relatorios/medias-por-disciplina")
def obter_medias_por_disciplina():
    return {"medias_por_disciplina": estudante_service.calcular_media_turma_por_disciplina()}


@router.get("/relatorios/estudantes-acima-da-media")
def obter_estudantes_acima_da_media():
    return {"estudantes": estudante_service.obter_estudantes_acima_da_media()}


@router.get("/relatorios/estudantes-com-baixa-frequencia")
def obter_estudantes_com_baixa_frequencia():
    return {
        "estudantes": estudante_service.obter_estudantes_com_baixa_frequencia()
    }

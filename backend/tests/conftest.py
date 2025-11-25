import pytest
from backend.service.estudanteService import EstudanteService
from backend.model.estudante import CriarEstudante, AtualizarEstudante


@pytest.fixture
def service():
    """Fixture que cria uma instância limpa do EstudanteService para cada teste"""
    return EstudanteService()


@pytest.fixture
def estudante_exemplo():
    """Fixture com dados de exemplo de estudante"""
    return CriarEstudante(
        nome="João Silva",
        notas=[7.5, 8.0, 6.5, 9.0, 7.0],
        frequencia=85.0
    )


@pytest.fixture
def estudante_exemplo_2():
    """Fixture com dados de outro estudante"""
    return CriarEstudante(
        nome="Maria Santos",
        notas=[8.5, 9.0, 7.5, 8.5, 9.0],
        frequencia=90.0
    )


@pytest.fixture
def estudante_baixa_frequencia():
    """Fixture com estudante com frequência baixa"""
    return CriarEstudante(
        nome="Pedro Costa",
        notas=[6.0, 5.5, 6.5, 7.0, 6.0],
        frequencia=70.0
    )


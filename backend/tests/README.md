# Testes Unitários

Este diretório contém os testes unitários do backend.

## Executando os testes

### Todos os testes
pytest

### Testes específicos
# Apenas testes do service
pytest backend/tests/test_estudante_service.py

# Apenas testes do controller
pytest backend/tests/test_estudante_controller.py

# Teste específico
pytest backend/tests/test_estudante_service.py::TestEstudanteService::test_criar_estudante_sucesso

### Com cobertura
pytest --cov=backend --cov-report=html

## Estrutura

- `conftest.py`: Fixtures compartilhadas entre testes
- `test_estudante_service.py`: Testes para a camada de serviço
- `test_estudante_controller.py`: Testes para os endpoints da API


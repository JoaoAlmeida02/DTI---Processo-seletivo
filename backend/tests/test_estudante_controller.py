import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.service.estudanteService import EstudanteService


@pytest.fixture
def client():
    """Fixture que cria um cliente de teste para a API"""
    return TestClient(app)


@pytest.fixture
def service_limpo():
    """Fixture que limpa o service antes de cada teste"""
    service = EstudanteService()
    # Limpar todos os estudantes
    estudantes = service.listar_estudantes()
    for estudante in estudantes:
        service.remover_estudante(estudante.id)
    return service


class TestEstudanteController:
    """Testes unitários para os endpoints do EstudanteController"""

    def test_criar_estudante_sucesso(self, client):
        """Testa criação de estudante via API"""
        payload = {
            "nome": "João Silva",
            "notas": [7.5, 8.0, 6.5, 9.0, 7.0],
            "frequencia": 85.0
        }
        
        response = client.post("/api/estudantes", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["notas"] == [7.5, 8.0, 6.5, 9.0, 7.0]
        assert data["frequencia"] == 85.0
        assert "id" in data

    def test_criar_estudante_nome_duplicado(self, client):
        """Testa que API retorna 409 para nome duplicado"""
        payload = {
            "nome": "João Silva",
            "notas": [7.5, 8.0, 6.5, 9.0, 7.0],
            "frequencia": 85.0
        }
        
        client.post("/api/estudantes", json=payload)
        response = client.post("/api/estudantes", json=payload)
        
        assert response.status_code == 409
        assert "Já existe um estudante com esse nome" in response.json()["detail"]

    def test_listar_estudantes_vazio(self, client):
        """Testa listagem quando não há estudantes"""
        response = client.get("/api/estudantes")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_estudantes_com_dados(self, client):
        """Testa listagem de estudantes"""
        payload = {
            "nome": "Maria Santos",
            "notas": [8.0, 8.5, 7.5, 9.0, 8.0],
            "frequencia": 90.0
        }
        
        client.post("/api/estudantes", json=payload)
        response = client.get("/api/estudantes")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(e["nome"] == "Maria Santos" for e in data)

    def test_obter_estudante_por_id_existente(self, client):
        """Testa obter estudante por ID"""
        payload = {
            "nome": "Pedro Costa",
            "notas": [6.0, 7.0, 6.5, 7.5, 6.5],
            "frequencia": 75.0
        }
        
        criar_response = client.post("/api/estudantes", json=payload)
        estudante_id = criar_response.json()["id"]
        
        response = client.get(f"/api/estudantes/{estudante_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == estudante_id
        assert data["nome"] == "Pedro Costa"

    def test_obter_estudante_por_id_inexistente(self, client):
        """Testa obter estudante inexistente retorna 404"""
        response = client.get("/api/estudantes/id-inexistente")
        
        assert response.status_code == 404
        assert "Aluno não encontrado" in response.json()["detail"]

    def test_atualizar_estudante_sucesso(self, client):
        """Testa atualização de estudante"""
        payload_criar = {
            "nome": "Ana Lima",
            "notas": [7.0, 7.5, 6.5, 8.0, 7.0],
            "frequencia": 80.0
        }
        
        criar_response = client.post("/api/estudantes", json=payload_criar)
        estudante_id = criar_response.json()["id"]
        
        payload_atualizar = {
            "nome": "Ana Lima Silva",
            "notas": [8.0, 8.5, 7.5, 9.0, 8.0],
            "frequencia": 85.0
        }
        
        response = client.put(f"/api/estudantes/{estudante_id}", json=payload_atualizar)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Ana Lima Silva"
        assert data["notas"] == [8.0, 8.5, 7.5, 9.0, 8.0]
        assert data["frequencia"] == 85.0

    def test_atualizar_estudante_inexistente(self, client):
        """Testa atualização de estudante inexistente retorna 404"""
        payload = {
            "nome": "Nome Qualquer",
            "notas": [8.0, 8.0, 8.0, 8.0, 8.0],
            "frequencia": 80.0
        }
        
        response = client.put("/api/estudantes/id-inexistente", json=payload)
        
        assert response.status_code == 404

    def test_remover_estudante_existente(self, client):
        """Testa remoção de estudante"""
        payload = {
            "nome": "Carlos Oliveira",
            "notas": [6.5, 7.0, 6.0, 7.5, 6.5],
            "frequencia": 70.0
        }
        
        criar_response = client.post("/api/estudantes", json=payload)
        estudante_id = criar_response.json()["id"]
        
        response = client.delete(f"/api/estudantes/{estudante_id}")
        
        assert response.status_code == 204
        
        # Verificar que foi removido
        get_response = client.get(f"/api/estudantes/{estudante_id}")
        assert get_response.status_code == 404

    def test_remover_estudante_inexistente(self, client):
        """Testa remoção de estudante inexistente retorna 404"""
        response = client.delete("/api/estudantes/id-inexistente")
        
        assert response.status_code == 404

    def test_gerar_relatorio(self, client):
        """Testa geração de relatório completo"""
        payload = {
            "nome": "Teste Relatório",
            "notas": [7.0, 8.0, 7.5, 8.5, 7.0],
            "frequencia": 85.0
        }
        
        client.post("/api/estudantes", json=payload)
        response = client.get("/api/relatorios")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_estudantes" in data
        assert "media_turma" in data
        assert "medias_por_disciplina" in data
        assert "estudantes_acima_da_media" in data
        assert "estudantes_com_baixa_frequencia" in data

    def test_obter_media_turma(self, client):
        """Testa endpoint de média da turma"""
        response = client.get("/api/relatorios/media-turma")
        
        assert response.status_code == 200
        data = response.json()
        assert "media_turma" in data
        assert isinstance(data["media_turma"], (int, float))

    def test_obter_medias_por_disciplina(self, client):
        """Testa endpoint de médias por disciplina"""
        response = client.get("/api/relatorios/medias-por-disciplina")
        
        assert response.status_code == 200
        data = response.json()
        assert "medias_por_disciplina" in data
        assert isinstance(data["medias_por_disciplina"], list)
        assert len(data["medias_por_disciplina"]) == 5

    def test_obter_estudantes_acima_da_media(self, client):
        """Testa endpoint de estudantes acima da média"""
        response = client.get("/api/relatorios/estudantes-acima-da-media")
        
        assert response.status_code == 200
        data = response.json()
        assert "estudantes" in data
        assert isinstance(data["estudantes"], list)

    def test_obter_estudantes_com_baixa_frequencia(self, client):
        """Testa endpoint de estudantes com baixa frequência"""
        response = client.get("/api/relatorios/estudantes-com-baixa-frequencia")
        
        assert response.status_code == 200
        data = response.json()
        assert "estudantes" in data
        assert isinstance(data["estudantes"], list)

    def test_validacao_notas_invalidas(self, client):
        """Testa validação de notas fora do range"""
        payload = {
            "nome": "Teste",
            "notas": [11.0, 8.0, 6.5, 9.0, 7.0],  # Nota > 10
            "frequencia": 85.0
        }
        
        response = client.post("/api/estudantes", json=payload)
        assert response.status_code == 422  # Unprocessable Entity

    def test_validacao_frequencia_invalida(self, client):
        """Testa validação de frequência fora do range"""
        payload = {
            "nome": "Teste",
            "notas": [7.0, 8.0, 6.5, 9.0, 7.0],
            "frequencia": 150.0  # Frequência > 100
        }
        
        response = client.post("/api/estudantes", json=payload)
        assert response.status_code == 422

    def test_validacao_numero_incorreto_notas(self, client):
        """Testa validação de número incorreto de notas"""
        payload = {
            "nome": "Teste",
            "notas": [7.0, 8.0, 6.5],  # Apenas 3 notas
            "frequencia": 85.0
        }
        
        response = client.post("/api/estudantes", json=payload)
        assert response.status_code == 422


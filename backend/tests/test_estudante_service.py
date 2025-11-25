import pytest
from backend.service.estudanteService import EstudanteService
from backend.model.estudante import CriarEstudante, AtualizarEstudante


class TestEstudanteService:
    """Testes unitários para EstudanteService"""

    def test_criar_estudante_sucesso(self, service, estudante_exemplo):
        """Testa criação de estudante com sucesso"""
        estudante = service.criar_estudante(estudante_exemplo)
        
        assert estudante.nome == "João Silva"
        assert estudante.notas == [7.5, 8.0, 6.5, 9.0, 7.0]
        assert estudante.frequencia == 85.0
        assert estudante.id is not None
        assert len(estudante.id) > 0

    def test_criar_estudante_nome_duplicado(self, service, estudante_exemplo):
        """Testa que não permite criar estudante com nome duplicado"""
        service.criar_estudante(estudante_exemplo)
        
        with pytest.raises(ValueError, match="Já existe um estudante com esse nome"):
            service.criar_estudante(estudante_exemplo)

    def test_criar_estudante_nome_case_insensitive(self, service, estudante_exemplo):
        """Testa que validação de nome é case-insensitive"""
        service.criar_estudante(estudante_exemplo)
        
        estudante_maiusculo = CriarEstudante(
            nome="JOÃO SILVA",
            notas=[8.0, 8.0, 8.0, 8.0, 8.0],
            frequencia=80.0
        )
        
        with pytest.raises(ValueError, match="Já existe um estudante com esse nome"):
            service.criar_estudante(estudante_maiusculo)

    def test_listar_estudantes_vazio(self, service):
        """Testa listagem quando não há estudantes"""
        estudantes = service.listar_estudantes()
        assert estudantes == []

    def test_listar_estudantes_com_dados(self, service, estudante_exemplo, estudante_exemplo_2):
        """Testa listagem de múltiplos estudantes"""
        estudante1 = service.criar_estudante(estudante_exemplo)
        estudante2 = service.criar_estudante(estudante_exemplo_2)
        
        estudantes = service.listar_estudantes()
        assert len(estudantes) == 2
        assert estudante1 in estudantes
        assert estudante2 in estudantes

    def test_obter_estudante_por_id_existente(self, service, estudante_exemplo):
        """Testa obter estudante por ID quando existe"""
        estudante_criado = service.criar_estudante(estudante_exemplo)
        estudante_encontrado = service.obter_estudante_por_id(estudante_criado.id)
        
        assert estudante_encontrado is not None
        assert estudante_encontrado.id == estudante_criado.id
        assert estudante_encontrado.nome == estudante_criado.nome

    def test_obter_estudante_por_id_inexistente(self, service):
        """Testa obter estudante por ID quando não existe"""
        estudante = service.obter_estudante_por_id("id-inexistente")
        assert estudante is None

    def test_atualizar_estudante_sucesso(self, service, estudante_exemplo):
        """Testa atualização de estudante com sucesso"""
        estudante_criado = service.criar_estudante(estudante_exemplo)
        
        dados_atualizacao = AtualizarEstudante(
            nome="João Silva Santos",
            notas=[8.0, 8.5, 7.0, 9.5, 8.0],
            frequencia=90.0
        )
        
        estudante_atualizado = service.atualizar_estudante(
            estudante_criado.id, dados_atualizacao
        )
        
        assert estudante_atualizado is not None
        assert estudante_atualizado.id == estudante_criado.id
        assert estudante_atualizado.nome == "João Silva Santos"
        assert estudante_atualizado.notas == [8.0, 8.5, 7.0, 9.5, 8.0]
        assert estudante_atualizado.frequencia == 90.0

    def test_atualizar_estudante_inexistente(self, service, estudante_exemplo):
        """Testa atualização de estudante que não existe"""
        dados_atualizacao = AtualizarEstudante(
            nome="Nome Qualquer",
            notas=[8.0, 8.0, 8.0, 8.0, 8.0],
            frequencia=80.0
        )
        
        estudante = service.atualizar_estudante("id-inexistente", dados_atualizacao)
        assert estudante is None

    def test_atualizar_estudante_nome_duplicado(self, service, estudante_exemplo, estudante_exemplo_2):
        """Testa que não permite atualizar com nome duplicado"""
        estudante1 = service.criar_estudante(estudante_exemplo)
        estudante2 = service.criar_estudante(estudante_exemplo_2)
        
        dados_atualizacao = AtualizarEstudante(
            nome=estudante2.nome,  # Tenta usar nome do estudante2
            notas=[8.0, 8.0, 8.0, 8.0, 8.0],
            frequencia=80.0
        )
        
        with pytest.raises(ValueError, match="Já existe um estudante com esse nome"):
            service.atualizar_estudante(estudante1.id, dados_atualizacao)

    def test_atualizar_estudante_mesmo_nome(self, service, estudante_exemplo):
        """Testa que permite atualizar mantendo o mesmo nome"""
        estudante_criado = service.criar_estudante(estudante_exemplo)
        
        dados_atualizacao = AtualizarEstudante(
            nome=estudante_exemplo.nome,  # Mesmo nome
            notas=[9.0, 9.0, 9.0, 9.0, 9.0],
            frequencia=95.0
        )
        
        estudante_atualizado = service.atualizar_estudante(
            estudante_criado.id, dados_atualizacao
        )
        
        assert estudante_atualizado is not None
        assert estudante_atualizado.nome == estudante_exemplo.nome

    def test_remover_estudante_existente(self, service, estudante_exemplo):
        """Testa remoção de estudante existente"""
        estudante_criado = service.criar_estudante(estudante_exemplo)
        resultado = service.remover_estudante(estudante_criado.id)
        
        assert resultado is True
        assert service.obter_estudante_por_id(estudante_criado.id) is None

    def test_remover_estudante_inexistente(self, service):
        """Testa remoção de estudante que não existe"""
        resultado = service.remover_estudante("id-inexistente")
        assert resultado is False

    def test_calcular_media_estudante(self, service, estudante_exemplo):
        """Testa cálculo de média individual"""
        estudante = service.criar_estudante(estudante_exemplo)
        media = service.calcular_media_estudante(estudante)
        
        # (7.5 + 8.0 + 6.5 + 9.0 + 7.0) / 5 = 7.6
        assert media == 7.6

    def test_calcular_media_turma_vazia(self, service):
        """Testa cálculo de média da turma quando vazia"""
        media = service.calcular_media_turma()
        assert media == 0.0

    def test_calcular_media_turma_com_estudantes(self, service, estudante_exemplo, estudante_exemplo_2):
        """Testa cálculo de média da turma com estudantes"""
        estudante1 = service.criar_estudante(estudante_exemplo)
        estudante2 = service.criar_estudante(estudante_exemplo_2)
        
        media_turma = service.calcular_media_turma()
        
        # Média do estudante1: 7.6
        # Média do estudante2: (8.5 + 9.0 + 7.5 + 8.5 + 9.0) / 5 = 8.5
        # Média da turma: (7.6 + 8.5) / 2 = 8.05
        assert media_turma == 8.05

    def test_calcular_media_turma_por_disciplina_vazia(self, service):
        """Testa cálculo de médias por disciplina quando não há estudantes"""
        medias = service.calcular_media_turma_por_disciplina()
        
        assert len(medias) == 5
        assert all(media["media"] == 0.0 for media in medias)

    def test_calcular_media_turma_por_disciplina(self, service, estudante_exemplo, estudante_exemplo_2):
        """Testa cálculo de médias por disciplina"""
        service.criar_estudante(estudante_exemplo)
        service.criar_estudante(estudante_exemplo_2)
        
        medias = service.calcular_media_turma_por_disciplina()
        
        assert len(medias) == 5
        # Disciplina 1: (7.5 + 8.5) / 2 = 8.0
        assert medias[0]["media"] == 8.0
        assert medias[0]["disciplina"] == "Disciplina 1"

    def test_obter_estudantes_acima_da_media(self, service, estudante_exemplo, estudante_exemplo_2):
        """Testa obtenção de estudantes acima da média"""
        service.criar_estudante(estudante_exemplo)  # Média: 7.6
        estudante2 = service.criar_estudante(estudante_exemplo_2)  # Média: 8.5
        
        # Média da turma: 8.05
        estudantes_acima = service.obter_estudantes_acima_da_media()
        
        assert len(estudantes_acima) == 1
        assert estudantes_acima[0]["id"] == estudante2.id
        assert estudantes_acima[0]["nome"] == estudante2.nome
        assert estudantes_acima[0]["media"] == 8.5

    def test_obter_estudantes_com_baixa_frequencia(self, service, estudante_exemplo, estudante_baixa_frequencia):
        """Testa obtenção de estudantes com frequência baixa"""
        service.criar_estudante(estudante_exemplo)  # 85%
        estudante_baixo = service.criar_estudante(estudante_baixa_frequencia)  # 70%
        
        estudantes_baixa_freq = service.obter_estudantes_com_baixa_frequencia()
        
        assert len(estudantes_baixa_freq) == 1
        assert estudantes_baixa_freq[0]["id"] == estudante_baixo.id
        assert estudantes_baixa_freq[0]["frequencia"] == 70.0

    def test_obter_estudantes_com_baixa_frequencia_customizado(self, service, estudante_exemplo):
        """Testa obtenção com limite customizado"""
        estudante = service.criar_estudante(estudante_exemplo)  # 85%
        
        estudantes = service.obter_estudantes_com_baixa_frequencia(limite=90.0)
        assert len(estudantes) == 1
        assert estudantes[0]["id"] == estudante.id

    def test_gerar_relatorio_completo(self, service, estudante_exemplo, estudante_exemplo_2):
        """Testa geração de relatório completo"""
        service.criar_estudante(estudante_exemplo)
        service.criar_estudante(estudante_exemplo_2)
        
        relatorio = service.gerar_relatorio()
        
        assert relatorio["total_estudantes"] == 2
        assert "media_turma" in relatorio
        assert "medias_por_disciplina" in relatorio
        assert "estudantes_acima_da_media" in relatorio
        assert "estudantes_com_baixa_frequencia" in relatorio
        assert len(relatorio["estudantes"]) == 2


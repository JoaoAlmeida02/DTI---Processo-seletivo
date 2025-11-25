from typing import Any, Dict, List, Optional

from backend.model.estudante import AtualizarEstudante, CriarEstudante, Estudante

TOTAL_DISCIPLINAS = 5


class EstudanteService:
    def __init__(self):
        self.estudantes: Dict[str, Estudante] = {}

    def _nome_em_uso(self, nome: str, ignorar_id: Optional[str] = None) -> bool:
        nome_normalizado = nome.strip().lower()
        for estudante in self.estudantes.values():
            if ignorar_id and estudante.id == ignorar_id:
                continue
            if estudante.nome.strip().lower() == nome_normalizado:
                return True
        return False

    def criar_estudante(self, dados_estudante: CriarEstudante) -> Estudante:
        if self._nome_em_uso(dados_estudante.nome):
            raise ValueError("Já existe um estudante com esse nome.")

        novo_estudante = Estudante(**dados_estudante.dict())
        self.estudantes[novo_estudante.id] = novo_estudante
        return novo_estudante

    def listar_estudantes(self) -> List[Estudante]:
        return list(self.estudantes.values())

    def obter_estudante_por_id(self, estudante_id: str) -> Optional[Estudante]:
        return self.estudantes.get(estudante_id)

    def atualizar_estudante(
        self, estudante_id: str, dados_estudante: AtualizarEstudante
    ) -> Optional[Estudante]:
        if estudante_id not in self.estudantes:
            return None

        if self._nome_em_uso(dados_estudante.nome, ignorar_id=estudante_id):
            raise ValueError("Já existe um estudante com esse nome.")

        estudante_atualizado = Estudante(id=estudante_id, **dados_estudante.dict())
        self.estudantes[estudante_id] = estudante_atualizado
        return estudante_atualizado

    def remover_estudante(self, estudante_id: str) -> bool:
        if estudante_id in self.estudantes:
            del self.estudantes[estudante_id]
            return True
        return False

    def calcular_media_estudante(self, estudante: Estudante) -> float:
        return sum(estudante.notas) / len(estudante.notas)

    def calcular_media_turma_por_disciplina(self) -> List[Dict[str, float]]:
        if not self.estudantes:
            return [
                {"disciplina": f"Disciplina {indice + 1}", "media": 0.0}
                for indice in range(TOTAL_DISCIPLINAS)
            ]

        estudantes = list(self.estudantes.values())
        medias_por_disciplina: List[Dict[str, float]] = []

        for indice_disciplina in range(TOTAL_DISCIPLINAS):
            soma_disciplina = sum(
                estudante.notas[indice_disciplina] for estudante in estudantes
            )
            media_disciplina = soma_disciplina / len(estudantes)
            medias_por_disciplina.append(
                {
                    "disciplina": f"Disciplina {indice_disciplina + 1}",
                    "media": round(media_disciplina, 2),
                }
            )

        return medias_por_disciplina

    def calcular_media_turma(self) -> float:
        if not self.estudantes:
            return 0.0

        soma_medias = sum(
            self.calcular_media_estudante(estudante)
            for estudante in self.estudantes.values()
        )
        return round(soma_medias / len(self.estudantes), 2)

    def obter_estudantes_acima_da_media(self) -> List[Dict[str, Any]]:
        media_turma = self.calcular_media_turma()

        estudantes_acima = []
        for estudante in self.estudantes.values():
            media_estudante = self.calcular_media_estudante(estudante)
            if media_estudante > media_turma:
                estudantes_acima.append(
                    {
                        "id": estudante.id,
                        "nome": estudante.nome,
                        "media": round(media_estudante, 2),
                    }
                )

        return estudantes_acima

    def obter_estudantes_com_baixa_frequencia(
        self, limite: float = 75.0
    ) -> List[Dict[str, Any]]:
        estudantes_com_baixa_frequencia = []

        for estudante in self.estudantes.values():
            if estudante.frequencia < limite:
                estudantes_com_baixa_frequencia.append(
                    {
                        "id": estudante.id,
                        "nome": estudante.nome,
                        "frequencia": estudante.frequencia,
                    }
                )

        return estudantes_com_baixa_frequencia

    def gerar_relatorio(self) -> Dict[str, Any]:
        estudantes = self.listar_estudantes()

        estudantes_com_medias = [
            {
                "id": estudante.id,
                "nome": estudante.nome,
                "notas": estudante.notas,
                "frequencia": estudante.frequencia,
                "media": round(self.calcular_media_estudante(estudante), 2),
            }
            for estudante in estudantes
        ]

        return {
            "total_estudantes": len(estudantes),
            "estudantes": estudantes_com_medias,
            "media_turma": self.calcular_media_turma(),
            "medias_por_disciplina": self.calcular_media_turma_por_disciplina(),
            "estudantes_acima_da_media": self.obter_estudantes_acima_da_media(),
            "estudantes_com_baixa_frequencia": self.obter_estudantes_com_baixa_frequencia(),
        }


estudante_service = EstudanteService()
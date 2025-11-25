from typing import Any, Dict, List, Optional
from uuid import uuid4

from backend.model.estudante import AtualizarEstudante, CriarEstudante, Estudante
from backend.database.db import get_cursor

TOTAL_DISCIPLINAS = 5


class EstudanteService:
    def __init__(self):
        pass  # Não precisa mais do dicionário em memória

    def _nome_em_uso(self, nome: str, ignorar_id: Optional[str] = None) -> bool:
        nome_normalizado = nome.strip().lower()
        
        with get_cursor() as cursor:
            if ignorar_id:
                cursor.execute(
                    """
                    SELECT COUNT(*) as count
                    FROM estudantes
                    WHERE LOWER(TRIM(nome)) = %s AND id != %s
                    """,
                    (nome_normalizado, ignorar_id)
                )
            else:
                cursor.execute(
                    """
                    SELECT COUNT(*) as count
                    FROM estudantes
                    WHERE LOWER(TRIM(nome)) = %s
                    """,
                    (nome_normalizado,)
                )
            
            result = cursor.fetchone()
            return result["count"] > 0

    def _buscar_notas_estudante(self, estudante_id: str) -> List[float]:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT nota
                FROM notas
                WHERE estudante_id = %s
                ORDER BY disciplina
                """,
                (estudante_id,)
            )
            resultados = cursor.fetchall()
            return [float(row["nota"]) for row in resultados]

    def _criar_notas_estudante(self, estudante_id: str, notas: List[float]) -> None:
        with get_cursor() as cursor:
            for disciplina, nota in enumerate(notas, start=1):
                cursor.execute(
                    """
                    INSERT INTO notas (estudante_id, disciplina, nota)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (estudante_id, disciplina)
                    DO UPDATE SET nota = EXCLUDED.nota
                    """,
                    (estudante_id, disciplina, nota)
                )

    def _atualizar_notas_estudante(self, estudante_id: str, notas: List[float]) -> None:
        with get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM notas WHERE estudante_id = %s",
                (estudante_id,)
            )
        self._criar_notas_estudante(estudante_id, notas)

    def _row_para_estudante(self, row: Dict) -> Estudante:
        estudante_id = str(row["id"])
        notas = self._buscar_notas_estudante(estudante_id)
        
        return Estudante(
            id=estudante_id,
            nome=row["nome"],
            notas=notas,
            frequencia=float(row["frequencia"])
        )

    def criar_estudante(self, dados_estudante: CriarEstudante) -> Estudante:
        if self._nome_em_uso(dados_estudante.nome):
            raise ValueError("Já existe um estudante com esse nome.")

        estudante_id = str(uuid4())
        
        with get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO estudantes (id, nome, frequencia)
                VALUES (%s, %s, %s)
                """,
                (estudante_id, dados_estudante.nome, dados_estudante.frequencia)
            )
        
        self._criar_notas_estudante(estudante_id, dados_estudante.notas)
        
        return self.obter_estudante_por_id(estudante_id)

    def listar_estudantes(self) -> List[Estudante]:
        with get_cursor() as cursor:
            cursor.execute("SELECT id, nome, frequencia FROM estudantes ORDER BY nome")
            rows = cursor.fetchall()
            
            estudantes = []
            for row in rows:
                estudantes.append(self._row_para_estudante(row))
            
            return estudantes

    def obter_estudante_por_id(self, estudante_id: str) -> Optional[Estudante]:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT id, nome, frequencia FROM estudantes WHERE id = %s",
                (estudante_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return self._row_para_estudante(row)

    def atualizar_estudante(
        self, estudante_id: str, dados_estudante: AtualizarEstudante
    ) -> Optional[Estudante]:
        estudante_existente = self.obter_estudante_por_id(estudante_id)
        if not estudante_existente:
            return None

        if self._nome_em_uso(dados_estudante.nome, ignorar_id=estudante_id):
            raise ValueError("Já existe um estudante com esse nome.")

        with get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE estudantes
                SET nome = %s, frequencia = %s
                WHERE id = %s
                """,
                (dados_estudante.nome, dados_estudante.frequencia, estudante_id)
            )
        
        # Atualizar notas
        self._atualizar_notas_estudante(estudante_id, dados_estudante.notas)
        
        return self.obter_estudante_por_id(estudante_id)

    def remover_estudante(self, estudante_id: str) -> bool:
        with get_cursor() as cursor:
            cursor.execute("SELECT id FROM estudantes WHERE id = %s", (estudante_id,))
            if not cursor.fetchone():
                return False
            
            cursor.execute("DELETE FROM estudantes WHERE id = %s", (estudante_id,))
            return True

    def calcular_media_estudante(self, estudante: Estudante) -> float:
        if not estudante.notas or len(estudante.notas) == 0:
            return 0.0
        return sum(estudante.notas) / len(estudante.notas)

    def calcular_media_turma_por_disciplina(self) -> List[Dict[str, float]]:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    disciplina,
                    AVG(nota) as media
                FROM notas
                GROUP BY disciplina
                ORDER BY disciplina
                """
            )
            resultados = cursor.fetchall()
            
            medias_dict = {}
            for row in resultados:
                disciplina = int(row["disciplina"])
                media = float(row["media"])
                medias_dict[disciplina] = round(media, 2)
            
            # Retornar em ordem (1 a 5), preenchendo com 0.0 se não houver notas
            medias_por_disciplina = []
            for i in range(1, TOTAL_DISCIPLINAS + 1):
                medias_por_disciplina.append({
                    "disciplina": f"Disciplina {i}",
                    "media": medias_dict.get(i, 0.0)
                })
            
            return medias_por_disciplina

    def calcular_media_turma(self) -> float:
        estudantes = self.listar_estudantes()
        
        if not estudantes:
            return 0.0
        
        soma_medias = sum(
            self.calcular_media_estudante(estudante) for estudante in estudantes
        )
        return round(soma_medias / len(estudantes), 2)

    def obter_estudantes_acima_da_media(self) -> List[Dict[str, Any]]:
        media_turma = self.calcular_media_turma()
        estudantes = self.listar_estudantes()
        
        estudantes_acima = []
        for estudante in estudantes:
            media_estudante = self.calcular_media_estudante(estudante)
            if media_estudante > media_turma:
                estudantes_acima.append({
                    "id": estudante.id,
                    "nome": estudante.nome,
                    "media": round(media_estudante, 2),
                })
        
        return estudantes_acima

    def obter_estudantes_com_baixa_frequencia(
        self, limite: float = 75.0
    ) -> List[Dict[str, Any]]:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nome, frequencia
                FROM estudantes
                WHERE frequencia < %s
                ORDER BY frequencia ASC
                """,
                (limite,)
            )
            resultados = cursor.fetchall()
            
            return [
                {
                    "id": str(row["id"]),
                    "nome": row["nome"],
                    "frequencia": float(row["frequencia"]),
                }
                for row in resultados
            ]

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

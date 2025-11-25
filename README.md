# 📚 Sistema de Gestão de Notas e Frequência  
### Teste Técnico — Desenvolvedor Full Stack  
**Autor:** João Gabriel Santos Andrade Almeida

Este projeto foi desenvolvido como parte do processo seletivo para a vaga de **Estágio/Desenvolvedor Full Stack**.  
O objetivo é criar um sistema onde um professor possa registrar notas de alunos, acompanhar frequência e visualizar indicadores importantes automaticamente.

---

## 🚀 Tecnologias Utilizadas

### **Frontend**
- React
### **Backend**
- Python
---

## 🧠 Funcionalidades

✔ Inserção das notas (0 a 10) das **cinco disciplinas** de cada aluno  
✔ Registro da **frequência (%)**  
✔ Cálculo automático:

- Média individual do aluno  
- Média geral da turma por disciplina  
- Identificação de alunos:
  - Com média **acima da média da turma**
  - Com frequência **abaixo de 75%**

✔ Interface intuitiva para visualização dos resultados  
✔ API limpa e organizada seguindo boas práticas  

---

## 📥 Exemplo de Entrada (resumo do PDF)

---

## ▶️ Executando o backend via terminal

1. **Criar e ativar o ambiente virtual (opcional)**
   cd backend
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   source .venv/bin/activate # Linux/Mac
**Instalar as dependências**
   pip install -r requirements.txt
**Iniciar o servidor FastAPI**
   uvicorn backend.main:app --reload
**Testar as rotas**
   - Docs: http://localhost:8000/docs
   - Exemplos: `GET /api/estudantes`, `POST /api/estudantes`, `GET /api/relatorios/media-turma`

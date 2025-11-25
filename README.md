# 📚 Sistema de Gestão de Notas e Frequência  
### Teste Técnico — Desenvolvedor Full Stack  
**Autor:** João Gabriel Santos Andrade Almeida

Este projeto foi desenvolvido como parte do processo seletivo para a vaga de **Estágio/Desenvolvedor Full Stack**.  
O objetivo é criar um sistema onde um professor possa registrar notas de alunos, acompanhar frequência e visualizar indicadores importantes automaticamente.

---

## 🚀 Tecnologias Utilizadas

### **Frontend**
- React + Vite (JavaScript)
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

## ▶️ Executando o backend (100% local, sem banco)

Toda a persistência é feita em memória usando um dicionário dentro de `backend/service/estudanteService.py`. Ao reiniciar o servidor, os dados são resetados, facilitando os testes locais.

1. **Criar e ativar o ambiente virtual (opcional)**
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows (PowerShell pode exigir execução permitida)
   source .venv/bin/activate # Linux/Mac
2. **Instalar as dependências**
   python -m pip install -r requirements.txt
3. **Iniciar o servidor FastAPI (raiz do projeto)**
   uvicorn main:app --reload
4. **Testar as rotas**
   - Docs: http://127.0.0.1:8000/docs
   - Exemplos: `GET /api/estudantes`, `POST /api/estudantes`, `GET /api/relatorios`

## 🖥️ Frontend React (Vite)

O diretório `frontend/` contém um app React minimalista que consome a API. Para rodar:

1. Instale as dependências:
   cd frontend
   npm install
2. Execute o modo desenvolvimento:
   npm run dev
3. Abra http://127.0.0.1:5173 e utilize a interface (o backend precisa estar ativo em http://127.0.0.1:8000).
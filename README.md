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
✔ Edição de estudantes cadastrados  
✔ Validação de nomes únicos (não permite duplicatas)  
✔ Envio automático de e-mail quando aluno é cadastrado com frequência < 75%  

---

## 📋 Lista de Premissas Assumidas

1. **Persistência em memória**: O sistema utiliza armazenamento em memória (dicionário Python) para facilitar testes locais. Os dados são perdidos ao reiniciar o servidor.

2. **Cinco disciplinas fixas**: Cada estudante possui exatamente 5 notas, representando 5 disciplinas diferentes.

3. **Sistema de notas**: As notas variam de 0 a 10, seguindo o padrão brasileiro.

4. **Frequência percentual**: A frequência é representada como porcentagem (0-100%), onde 75% é o limite mínimo considerado adequado.

5. **Nomes únicos**: Não é permitido cadastrar dois estudantes com o mesmo nome (comparação case-insensitive).

6. **EmailJS como serviço de e-mail**: O sistema utiliza EmailJS para envio de e-mails, que oferece 500 envios gratuitos por dia.

7. **Ambiente de desenvolvimento**: O projeto foi desenvolvido para rodar localmente, com backend em Python/FastAPI e frontend em React/Vite.

---

## 🎯 Decisões de Projeto

### **Arquitetura**

- **Separação Frontend/Backend**: API RESTful (FastAPI) separada do frontend (React), permitindo escalabilidade e manutenção independente.

- **Camadas bem definidas**: 
  - `model/`: Modelos Pydantic para validação e serialização
  - `service/`: Lógica de negócio isolada
  - `controller/`: Endpoints HTTP e tratamento de erros

### **Validações e Regras de Negócio**

- **Validação de nome único**: Implementada no service, considerando case-insensitive e ignorando o próprio estudante durante edição.

- **Validação de notas**: Pydantic valida automaticamente que as notas estão entre 0-10 e que existem exatamente 5 notas.

- **Cálculo de médias**: Média individual (soma das 5 notas / 5) e média por disciplina (soma das notas de todos os alunos em uma disciplina / número de alunos).

### **Interface do Usuário**

- **Formulário único para criar/editar**: O mesmo formulário é usado para ambas operações, mudando dinamicamente o título e ações disponíveis.

- **Feedback visual**: Mensagens de status, popups de confirmação de e-mail e validações em tempo real.

- **Design responsivo**: Interface limpa e moderna, utilizando CSS Grid e Flexbox para layout adaptável.

### **Integração com EmailJS**

- **Template único**: Um único template EmailJS é usado tanto para alertas de frequência baixa quanto para outras notificações futuras.

- **Envio assíncrono**: O envio de e-mail não bloqueia o cadastro do estudante. Se falhar, apenas registra no console.

- **Popup de confirmação**: Usuário recebe feedback visual quando o e-mail é enviado com sucesso.

### **Código e Manutenibilidade**

- **Nomenclatura em português**: Todas as variáveis, funções e endpoints seguem nomenclatura em português para facilitar a compreensão.

- **Tratamento de erros centralizado**: Função `fetchJSON` centraliza o tratamento de erros HTTP.

- **Componentização**: Componente `Media` reutilizável para cálculo e exibição de médias.

---

## 💡 O que mais você achar importante compartilhar sobre o projeto

### **Funcionalidades Extras Implementadas**

1. **Edição de estudantes**: Permite atualizar dados de estudantes já cadastrados, mantendo todas as validações (nome único, notas, frequência).

2. **Médias por disciplina**: Além da média geral da turma, o sistema calcula e exibe a média de cada uma das 5 disciplinas separadamente.

3. **Alertas automáticos**: Sistema envia e-mail automaticamente quando um aluno é cadastrado com frequência abaixo de 75%, com popup de confirmação.

4. **Validação de nomes únicos**: Previne duplicatas de nomes, considerando variações de maiúsculas/minúsculas.

### **Estrutura do Projeto**

```
DTI---Processo-seletivo/
├── backend/
│   ├── controller/      # Endpoints HTTP
│   ├── model/           # Modelos Pydantic
│   ├── service/         # Lógica de negócio
│   └── main.py          # Aplicação FastAPI
├── frontend/
│   ├── src/
│   │   ├── config/      # Configurações (EmailJS)
│   │   ├── App.jsx      # Componente principal
│   │   └── styles.css   # Estilos globais
│   └── package.json
├── requirements.txt     # Dependências Python
└── README.md
```

### **Endpoints da API**

- `POST /api/estudantes` - Criar novo estudante
- `GET /api/estudantes` - Listar todos os estudantes
- `GET /api/estudantes/{id}` - Obter estudante específico
- `PUT /api/estudantes/{id}` - Atualizar estudante
- `DELETE /api/estudantes/{id}` - Remover estudante
- `GET /api/relatorios` - Relatório completo
- `GET /api/relatorios/media-turma` - Média geral da turma
- `GET /api/relatorios/medias-por-disciplina` - Médias por disciplina
- `GET /api/relatorios/estudantes-acima-da-media` - Estudantes acima da média
- `GET /api/relatorios/estudantes-com-baixa-frequencia` - Estudantes com frequência < 75%

### **Variáveis de Ambiente Necessárias**

Para o EmailJS funcionar, crie `frontend/.env.local`:

```
VITE_EMAILJS_SERVICE_ID=service_wxn0nrb
VITE_EMAILJS_TEMPLATE_ID=template_g1mqxdn
VITE_EMAILJS_PUBLIC_KEY=jQz2IxB_AR4IpQnwB
```

### **Observações Importantes**

- O backend não utiliza banco de dados, todos os dados são armazenados em memória.
- O EmailJS precisa ser configurado corretamente para que os alertas de frequência funcionem.
- A validação de nome único é case-insensitive (ex: "João" e "joão" são considerados iguais).
- O sistema envia e-mail apenas no cadastro (não na edição) quando a frequência é < 75%.

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

## ✉️ Configurando o EmailJS para o formulário de contato

1. Crie sua conta em [emailjs.com](https://www.emailjs.com/), adicione um **Email Service** e crie **dois templates**:
   - `FOR_ME`: envia os dados do formulário para o seu e-mail fixo.
   - `FOR_SENDER`: envia a confirmação para o e-mail digitado pelo usuário (`{{email}}` no campo *To email*).
2. Em cada template inclua as variáveis: `{{name}}`, `{{email}}`, `{{message}}`, `{{title}}` e `{{time}}`.
3. Copie `Service ID`, `Template ID For Me`, `Template ID For Sender` e `Public Key`.
4. Tanto o formulário “Contato” quanto o alerta automático de frequência usam esse único template para disparar os e-mails via `@emailjs/browser`.
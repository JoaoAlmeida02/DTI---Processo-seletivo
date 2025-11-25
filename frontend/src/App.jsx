import { useEffect, useMemo, useState } from "react";
import emailjs from "@emailjs/browser";

import EMAILJS_CONFIG from "./config/emailJsConfig";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api";

const NOTAS_INICIAIS = ["", "", "", "", ""];

const initialForm = {
  nome: "",
  frequencia: "",
  notas: NOTAS_INICIAIS,
};

function emailJsDisponivel() {
  return Boolean(
    EMAILJS_CONFIG.SERVICE_ID &&
      EMAILJS_CONFIG.TEMPLATE_ID &&
      EMAILJS_CONFIG.PUBLIC_KEY
  );
}

function Media({ notas }) {
  const media = useMemo(() => {
    if (!Array.isArray(notas) || notas.length === 0) return "--";
    const total = notas.reduce((acc, nota) => acc + nota, 0);
    return (total / notas.length).toFixed(2);
  }, [notas]);

  return <span>{media}</span>;
}

export default function App() {
  const [estudantes, setEstudantes] = useState([]);
  const [relatorio, setRelatorio] = useState(null);
  const [mediasPorDisciplina, setMediasPorDisciplina] = useState([]);
  const [formData, setFormData] = useState(initialForm);
  const [editandoId, setEditandoId] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  async function fetchJSON(path, options) {
    const res = await fetch(`${API_BASE}${path}`, options);
    if (!res.ok) {
      let detail = "Ocorreu um erro inesperado.";
      try {
        const body = await res.json();
        detail = body.detail || JSON.stringify(body);
      } catch {
        detail = res.statusText;
      }
      throw new Error(detail);
    }
    return res.status === 204 ? null : res.json();
  }

  async function carregarEstudantes() {
    const data = await fetchJSON("/estudantes");
    setEstudantes(data);
  }

  async function carregarRelatorio() {
    const data = await fetchJSON("/relatorios");
    setRelatorio(data);
  }

  async function carregarMediasPorDisciplina() {
    const data = await fetchJSON("/relatorios/medias-por-disciplina");
    setMediasPorDisciplina(data.medias_por_disciplina || []);
  }

  async function boot() {
    await Promise.all([
      carregarEstudantes(),
      carregarRelatorio(),
      carregarMediasPorDisciplina(),
    ]);
  }

  useEffect(() => {
    boot().catch((err) => setStatus(err.message));
  }, []);

  function handleInputChange(event, index) {
    if (typeof index === "number") {
      const novasNotas = [...formData.notas];
      novasNotas[index] = event.target.value;
      setFormData((prev) => ({ ...prev, notas: novasNotas }));
    } else {
      const { name, value } = event.target;
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  }

  function iniciarEdicao(estudante) {
    setFormData({
      nome: estudante.nome,
      frequencia: estudante.frequencia.toString(),
      notas: estudante.notas.map((nota) => nota.toString()),
    });
    setEditandoId(estudante.id);
    setStatus("");
  }

  function cancelarEdicao() {
    setFormData(initialForm);
    setEditandoId(null);
    setStatus("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setStatus(editandoId ? "Atualizando estudante..." : "Salvando estudante...");

    const payload = {
      nome: formData.nome,
      frequencia: Number(formData.frequencia),
      notas: formData.notas.map((nota) => Number(nota)),
    };

    try {
      if (editandoId) {
        await fetchJSON(`/estudantes/${editandoId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        setStatus("Estudante atualizado com sucesso!");
      } else {
        await fetchJSON("/estudantes", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        setStatus("Estudante salvo com sucesso!");
      }

      setFormData(initialForm);
      setEditandoId(null);
      await boot();

      if (payload.frequencia < 75 && !editandoId) {
        await enviarAlertaBaixaFrequencia(payload);
      }
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
      setTimeout(() => setStatus(""), 3000);
    }
  }

  async function enviarAlertaBaixaFrequencia(estudante) {
    if (!emailJsDisponivel()) {
      console.warn("EmailJS não configurado. Alerta não enviado.");
      return;
    }

    const time = new Date().toLocaleString();
    const mensagem = `Aluno ${estudante.nome} cadastrado com frequência de ${estudante.frequencia}% (abaixo de 75%).`;

    try {
      await enviarEmailJs({
        name: estudante.nome,
        email: "nao-responder@sistema-escolar.com",
        message: mensagem,
        title: `Alerta: frequência baixa de ${estudante.nome}`,
        time,
        context: "frequencia_baixa",
        frequencia: estudante.frequencia,
        notas: estudante.notas.join(", "),
      });
      window.alert(
        `E-mail de alerta enviado com sucesso!\n\nAluno: ${estudante.nome}\nFrequência: ${estudante.frequencia}%\n\nUm e-mail foi enviado notificando sobre a frequência baixa deste estudante.`
      );
    } catch (error) {
      console.error("Falha ao enviar alerta de frequência baixa:", error);
      window.alert(
        `Erro ao enviar e-mail de alerta.\n\nO estudante foi cadastrado, mas não foi possível enviar a notificação por e-mail.`
      );
    }
  }

  async function removerEstudante(id) {
    if (!window.confirm("Deseja remover este estudante?")) return;
    try {
      await fetchJSON(`/estudantes/${id}`, { method: "DELETE" });
      await boot();
    } catch (error) {
      setStatus(error.message);
    }
  }

  async function enviarEmailJs(payload) {
    if (!emailJsDisponivel()) {
      console.warn("EmailJS não está configurado.");
      return;
    }

    await emailjs.send(
      EMAILJS_CONFIG.SERVICE_ID,
      EMAILJS_CONFIG.TEMPLATE_ID,
      payload,
      EMAILJS_CONFIG.PUBLIC_KEY
    );
  }

  return (
    <div className="app-container">
      <header>
        <h1>Sistema de Gestão Escolar</h1>
      </header>

      <section>
        <h2>{editandoId ? "Editar estudante" : "Novo estudante"}</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Nome
            <input
              name="nome"
              value={formData.nome}
              onChange={handleInputChange}
              required
            />
          </label>

          <label>
            Frequência (%)
            <input
              type="number"
              name="frequencia"
              min="0"
              max="100"
              step="0.1"
              value={formData.frequencia}
              onChange={handleInputChange}
              required
            />
          </label>

          <div className="grade-grid">
            {formData.notas.map((valor, index) => (
              <label key={index}>
                Nota {index + 1}
                <input
                  type="number"
                  min="0"
                  max="10"
                  step="0.1"
                  value={valor}
                  onChange={(event) => handleInputChange(event, index)}
                  required
                />
              </label>
            ))}
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading}>
              {loading
                ? editandoId
                  ? "Atualizando..."
                  : "Salvando..."
                : editandoId
                  ? "Salvar alterações"
                  : "Salvar estudante"}
            </button>
            {editandoId && (
              <button
                type="button"
                onClick={cancelarEdicao}
                disabled={loading}
                className="secondary"
              >
                Cancelar
              </button>
            )}
          </div>
          {status && (
            <span className={`status${status.includes("erro") ? " error" : ""}`}>
              {status}
            </span>
          )}
        </form>
      </section>

      <section>
        <h2>Estudantes cadastrados</h2>
        <table>
          <thead>
            <tr>
              <th>Nome</th>
              <th>Média</th>
              <th>Frequência</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {estudantes.length === 0 && (
              <tr>
                <td colSpan={4}>Nenhum estudante cadastrado.</td>
              </tr>
            )}
            {estudantes.map((estudante) => (
              <tr key={estudante.id}>
                <td>{estudante.nome}</td>
                <td>
                  <Media notas={estudante.notas} />
                </td>
                <td>{estudante.frequencia}%</td>
                <td>
                  <div className="table-actions">
                    <button
                      type="button"
                      onClick={() => iniciarEdicao(estudante)}
                      disabled={editandoId === estudante.id}
                    >
                      Editar
                    </button>
                    <button
                      type="button"
                      className="danger"
                      onClick={() => removerEstudante(estudante.id)}
                      disabled={!!editandoId}
                    >
                      Remover
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Relatórios</h2>
        {relatorio ? (
          <>
            <ul className="relatorio-list">
              <li>Total de estudantes: {relatorio.total_estudantes}</li>
              <li>Média da turma: {relatorio.media_turma}</li>
              <li>
                Estudantes acima da média:{" "}
                {relatorio.estudantes_acima_da_media.length}
              </li>
              <li>
                Frequência &lt; 75%: {relatorio.estudantes_com_baixa_frequencia.length}
              </li>
            </ul>
            {mediasPorDisciplina.length > 0 && (
              <div className="medias-disciplinas">
                <h3>Médias por Disciplina</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Disciplina</th>
                      <th>Média</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mediasPorDisciplina.map((item, index) => (
                      <tr key={index}>
                        <td>{item.disciplina}</td>
                        <td>{item.media.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        ) : (
          <p>Carregando relatórios...</p>
        )}
      </section>
    </div>
  );
}
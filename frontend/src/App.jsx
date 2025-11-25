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

  const mediaNum = parseFloat(media);
  const classeMedia =
    mediaNum >= 7 ? "media-alta" : mediaNum >= 5 ? "media-media" : "media-baixa";

  return (
    <span className={`media-badge ${classeMedia}`}>
      <span className="media-value">{media}</span>
    </span>
  );
}

function FrequenciaBadge({ frequencia }) {
  const classeFreq =
    frequencia >= 75 ? "freq-alta" : frequencia >= 50 ? "freq-media" : "freq-baixa";
  const icone = frequencia >= 75 ? "✓" : frequencia >= 50 ? "⚠" : "✗";

  return (
    <span className={`freq-badge ${classeFreq}`}>
      <span className="freq-icon">{icone}</span>
      <span className="freq-value">{frequencia}%</span>
    </span>
  );
}

function StatCard({ titulo, valor, icone, cor }) {
  return (
    <div className={`stat-card stat-${cor}`}>
      <div className="stat-icon">{icone}</div>
      <div className="stat-content">
        <div className="stat-titulo">{titulo}</div>
        <div className="stat-valor">{valor}</div>
      </div>
    </div>
  );
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

  const estudanteEditando = editandoId
    ? estudantes.find((e) => e.id === editandoId)
    : null;

  return (
    <div className="app-container">
      <header className="main-header">
        <div className="header-content">
          <div className="header-title">
            <h1>
              <span className="header-icon"></span>
              Sistema de Gestão Escolar
            </h1>
            <p className="header-subtitle">
              Gerencie notas, frequência e relatórios dos seus estudantes
            </p>
          </div>
        </div>
      </header>

      <section className="form-section">
        <div className="section-header">
          <h2>
            {editandoId ? (
              <>
                <span className="section-icon">✏️</span>
                Editar estudante
              </>
            ) : (
              <>
                <span className="section-icon">➕</span>
                Novo estudante
              </>
            )}
          </h2>
          {editandoId && estudanteEditando && (
            <div className="edit-indicator">
              Editando: <strong>{estudanteEditando.nome}</strong>
            </div>
          )}
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <label className="form-label-large">
              <span className="label-text">
                <span className="label-icon">👤</span>
                Nome do Estudante
              </span>
              <input
                name="nome"
                value={formData.nome}
                onChange={handleInputChange}
                placeholder="Digite o nome completo"
                required
              />
            </label>

            <label className="form-label-large">
              <span className="label-text">
                <span className="label-icon">📊</span>
                Frequência (%)
              </span>
              <input
                type="number"
                name="frequencia"
                min="0"
                max="100"
                step="0.1"
                value={formData.frequencia}
                onChange={handleInputChange}
                placeholder="0.0 - 100.0"
                required
              />
            </label>
          </div>

          <div className="notas-section">
            <div className="notas-header">
              <span className="notas-icon">📝</span>
              <span className="notas-title">Notas das Disciplinas</span>
            </div>
            <div className="grade-grid">
              {formData.notas.map((valor, index) => (
                <label key={index} className="nota-label">
                  <span className="nota-number">Disciplina {index + 1}</span>
                  <input
                    type="number"
                    min="0"
                    max="10"
                    step="0.1"
                    value={valor}
                    onChange={(event) => handleInputChange(event, index)}
                    placeholder="0.0 - 10.0"
                    required
                    className="nota-input"
                  />
                </label>
              ))}
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? (
                <>
                  <span className="btn-spinner">⏳</span>
                  {editandoId ? "Atualizando..." : "Salvando..."}
                </>
              ) : (
                <>
                  <span className="btn-icon">
                    {editandoId ? "💾" : "✅"}
                  </span>
                  {editandoId ? "Salvar alterações" : "Salvar estudante"}
                </>
              )}
            </button>
            {editandoId && (
              <button
                type="button"
                onClick={cancelarEdicao}
                disabled={loading}
                className="btn-secondary"
              >
                <span className="btn-icon">❌</span>
                Cancelar
              </button>
            )}
          </div>
          {status && (
            <div
              className={`status-message ${
                status.includes("erro") || status.includes("Erro")
                  ? "error"
                  : status.includes("sucesso") || status.includes("Sucesso")
                  ? "success"
                  : "info"
              }`}
            >
              <span className="status-icon">
                {status.includes("erro") || status.includes("Erro")
                  ? "❌"
                  : status.includes("sucesso") || status.includes("Sucesso")
                  ? "✅"
                  : "ℹ️"}
              </span>
              <span>{status}</span>
            </div>
          )}
        </form>
      </section>

      <section className="students-section">
        <div className="section-header">
          <h2>
            <span className="section-icon">👥</span>
            Estudantes Cadastrados
          </h2>
          {estudantes.length > 0 && (
            <div className="students-count">
              {estudantes.length} {estudantes.length === 1 ? "estudante" : "estudantes"}
            </div>
          )}
        </div>
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
                <td colSpan={4} className="empty-state">
                  <div className="empty-content">
                    <span className="empty-icon">📋</span>
                    <p>Nenhum estudante cadastrado ainda.</p>
                    <p className="empty-hint">
                      Use o formulário acima para adicionar o primeiro estudante.
                    </p>
                  </div>
                </td>
              </tr>
            )}
            {estudantes.map((estudante) => (
              <tr key={estudante.id} className="student-row">
                <td className="student-name">
                  <strong>{estudante.nome}</strong>
                </td>
                <td>
                  <Media notas={estudante.notas} />
                </td>
                <td>
                  <FrequenciaBadge frequencia={estudante.frequencia} />
                </td>
                <td>
                  <div className="table-actions">
                    <button
                      type="button"
                      className="btn-edit"
                      onClick={() => iniciarEdicao(estudante)}
                      disabled={editandoId === estudante.id || !!editandoId}
                      title="Editar estudante"
                    >
                      <span className="btn-icon">✏️</span>
                      Editar
                    </button>
                    <button
                      type="button"
                      className="btn-danger"
                      onClick={() => removerEstudante(estudante.id)}
                      disabled={!!editandoId}
                      title="Remover estudante"
                    >
                      <span className="btn-icon">🗑️</span>
                      Remover
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="reports-section">
        <div className="section-header">
          <h2>
            <span className="section-icon">📊</span>
            Relatórios e Estatísticas
          </h2>
        </div>
        {relatorio ? (
          <>
            <div className="stats-grid">
              <StatCard
                titulo="Total de Estudantes"
                valor={relatorio.total_estudantes}
                icone="👥"
                cor="blue"
              />
              <StatCard
                titulo="Média da Turma"
                valor={relatorio.media_turma.toFixed(2)}
                icone="📈"
                cor="green"
              />
              <StatCard
                titulo="Acima da Média"
                valor={relatorio.estudantes_acima_da_media.length}
                icone="⭐"
                cor="yellow"
              />
              <StatCard
                titulo="Frequência &lt; 75%"
                valor={relatorio.estudantes_com_baixa_frequencia.length}
                icone="⚠️"
                cor="red"
              />
            </div>
            {mediasPorDisciplina.length > 0 && (
              <div className="medias-disciplinas">
                <div className="disciplinas-header">
                  <h3>
                    <span className="section-icon">📚</span>
                    Médias por Disciplina
                  </h3>
                  <p className="disciplinas-subtitle">
                    Média geral de cada disciplina da turma
                  </p>
                </div>
                <div className="disciplinas-grid">
                  {mediasPorDisciplina.map((item, index) => {
                    const mediaNum = parseFloat(item.media);
                    const classeMedia =
                      mediaNum >= 7
                        ? "disciplina-alta"
                        : mediaNum >= 5
                        ? "disciplina-media-class"
                        : "disciplina-baixa";
                    return (
                      <div key={index} className={`disciplina-card ${classeMedia}`}>
                        <div className="disciplina-nome">{item.disciplina}</div>
                        <div className="disciplina-media">{item.media.toFixed(2)}</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="loading-state">
            <span className="loading-spinner">⏳</span>
            <p>Carregando relatórios...</p>
          </div>
        )}
      </section>
    </div>
  );
}
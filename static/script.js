// ===== ESTADO =====
let todosJogadores = [];
let formacaoAtual = "4-3-3";
let estadoTime = [];      // por slot: jogador escolhido ou null
let slotAtivo = null;     // índice do slot esperando escolha (ou null)
let timeEstavaCompleto = false;

const FLAGS = {
  "Brasil": "🇧🇷", "Argentina": "🇦🇷", "França": "🇫🇷", "Portugal": "🇵🇹",
  "Bélgica": "🇧🇪", "Espanha": "🇪🇸", "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Alemanha": "🇩🇪",
  "Holanda": "🇳🇱", "Croácia": "🇭🇷", "Uruguai": "🇺🇾", "Noruega": "🇳🇴",
  "Egito": "🇪🇬", "Itália": "🇮🇹",
};

const POS_LABEL = { GK: "GOL", DEF: "ZAG", MID: "MEI", ATK: "ATA" };

// posições (em % do campo) para cada slot, por formação
const FORMACOES = {
  "4-3-3": {
    posicoes: { GK: 1, DEF: 4, MID: 3, ATK: 3 },
    slots: [
      { pos: "GK", x: 50, y: 89 },
      { pos: "DEF", x: 15, y: 68 }, { pos: "DEF", x: 38, y: 70 }, { pos: "DEF", x: 62, y: 70 }, { pos: "DEF", x: 85, y: 68 },
      { pos: "MID", x: 25, y: 46 }, { pos: "MID", x: 50, y: 44 }, { pos: "MID", x: 75, y: 46 },
      { pos: "ATK", x: 20, y: 18 }, { pos: "ATK", x: 50, y: 14 }, { pos: "ATK", x: 80, y: 18 },
    ],
  },
  "4-4-2": {
    posicoes: { GK: 1, DEF: 4, MID: 4, ATK: 2 },
    slots: [
      { pos: "GK", x: 50, y: 89 },
      { pos: "DEF", x: 15, y: 68 }, { pos: "DEF", x: 38, y: 70 }, { pos: "DEF", x: 62, y: 70 }, { pos: "DEF", x: 85, y: 68 },
      { pos: "MID", x: 12, y: 44 }, { pos: "MID", x: 37, y: 46 }, { pos: "MID", x: 63, y: 46 }, { pos: "MID", x: 88, y: 44 },
      { pos: "ATK", x: 35, y: 16 }, { pos: "ATK", x: 65, y: 16 },
    ],
  },
  "3-5-2": {
    posicoes: { GK: 1, DEF: 3, MID: 5, ATK: 2 },
    slots: [
      { pos: "GK", x: 50, y: 89 },
      { pos: "DEF", x: 25, y: 70 }, { pos: "DEF", x: 50, y: 72 }, { pos: "DEF", x: 75, y: 70 },
      { pos: "MID", x: 8, y: 46 }, { pos: "MID", x: 28, y: 44 }, { pos: "MID", x: 50, y: 42 }, { pos: "MID", x: 72, y: 44 }, { pos: "MID", x: 92, y: 46 },
      { pos: "ATK", x: 35, y: 16 }, { pos: "ATK", x: 65, y: 16 },
    ],
  },
};

// ===== DOM =====
const $ = (id) => document.getElementById(id);

const el = {
  orcamentoSlider: $("orcamento-slider"),
  orcamentoValor: $("orcamento-valor"),
  capacidadeBadge: $("capacidade-badge"),
  totalJogadoresBadge: $("total-jogadores-badge"),
  formationGrid: $("formation-grid"),
  formacaoAtualLabel: $("formacao-atual-label"),
  selecaoFilter: $("selecao-filter"),
  btnMontar: $("btn-montar"),
  playersList: $("players-list"),
  pickerHint: $("picker-hint"),
  pickerHintTexto: $("picker-hint-texto"),
  pickerHintCancelar: $("picker-hint-cancelar"),
  fieldWrap: $("field-wrap"),
  fieldSlots: $("field-slots"),
  boxscoreCount: $("boxscore-count"),
  overallMedio: $("overall-medio"),
  gastoValor: $("gasto-valor"),
  orcamentoTotalValor: $("orcamento-total-valor"),
  budgetBarFill: $("budget-bar-fill"),
  sobrouValor: $("sobrou-valor"),
  teamList: $("team-list"),
  btnResetar: $("btn-resetar"),
  btnCompartilhar: $("btn-compartilhar"),
};

// ===== HELPERS =====
function bandeira(selecao) {
  return FLAGS[selecao] || "🏳️";
}

function slotsAtuais() {
  return FORMACOES[formacaoAtual].slots;
}

function posicoesAtuais() {
  return FORMACOES[formacaoAtual].posicoes;
}

function orcamentoAtual() {
  return parseInt(el.orcamentoSlider.value, 10);
}

function gastoAtual() {
  return estadoTime.reduce((soma, j) => soma + (j ? j.preco : 0), 0);
}

function criarLinhaJogador(jogador, usado) {
  return `
    <div class="player-row pos-${jogador.posicao} ${usado ? "used" : ""}" data-id="${jogador.id}">
      <div class="row-overall">${jogador.overall}</div>
      <div class="row-info">
        <div class="row-nome">${jogador.nome}</div>
        <div class="row-meta">${bandeira(jogador.selecao)} ${jogador.selecao} · ${jogador.posicao}</div>
      </div>
      <div class="row-preco">€${jogador.preco}M</div>
    </div>
  `;
}

function criarLinhaBoxScore(pos, jogador) {
  if (!jogador) {
    return `
      <div class="boxscore-row empty">
        <span class="boxscore-pos">${POS_LABEL[pos]}</span>
        <span class="boxscore-name">—</span>
      </div>
    `;
  }
  return `
    <div class="boxscore-row">
      <span class="boxscore-pos">${POS_LABEL[pos]}</span>
      <span class="boxscore-name">${bandeira(jogador.selecao)} ${jogador.nome}</span>
      <span class="boxscore-overall">${jogador.overall}</span>
      <span class="boxscore-price">€${jogador.preco}M</span>
    </div>
  `;
}

function contarAte(elemento, valorFinal, duracaoMs) {
  const inicio = performance.now();
  elemento.classList.add("counting");
  function passo(agora) {
    const progresso = Math.min(1, (agora - inicio) / duracaoMs);
    elemento.textContent = Math.round(progresso * valorFinal);
    if (progresso < 1) {
      requestAnimationFrame(passo);
    } else {
      elemento.classList.remove("counting");
    }
  }
  requestAnimationFrame(passo);
}

function confetti() {
  const cores = ["#c9962f", "#e6552f", "#16a34a", "#2563eb", "#161410"];
  for (let i = 0; i < 60; i++) {
    const peca = document.createElement("div");
    peca.style.position = "fixed";
    peca.style.left = Math.random() * 100 + "vw";
    peca.style.top = "-10px";
    peca.style.width = "8px";
    peca.style.height = "8px";
    peca.style.background = cores[Math.floor(Math.random() * cores.length)];
    peca.style.opacity = "0.9";
    peca.style.borderRadius = Math.random() > 0.5 ? "50%" : "0";
    peca.style.zIndex = "9999";
    peca.style.pointerEvents = "none";
    peca.style.transition = `transform ${1.2 + Math.random()}s ease-in, opacity 1.6s ease-in`;
    document.body.appendChild(peca);
    requestAnimationFrame(() => {
      peca.style.transform = `translateY(${80 + Math.random() * 20}vh) rotate(${Math.random() * 360}deg)`;
      peca.style.opacity = "0";
    });
    setTimeout(() => peca.remove(), 2400);
  }
}

// ===== SELEÇÃO MANUAL (escolher jogador por posição, estilo 7a0) =====
function abrirPicker(idx) {
  slotAtivo = idx;
  const pos = slotsAtuais()[idx].pos;
  el.pickerHint.style.display = "flex";
  el.pickerHintTexto.textContent = `Escolhendo ${POS_LABEL[pos]} — clique num jogador da lista`;
  renderPlayersList();
  el.playersList.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function fecharPicker() {
  slotAtivo = null;
  el.pickerHint.style.display = "none";
  renderPlayersList();
}

function primeiroSlotVazio(pos) {
  const slots = slotsAtuais();
  for (let i = 0; i < slots.length; i++) {
    if (slots[i].pos === pos && !estadoTime[i]) return i;
  }
  return -1;
}

function escalarJogador(idx, jogador) {
  const precoAntigo = estadoTime[idx] ? estadoTime[idx].preco : 0;
  const novoGasto = gastoAtual() - precoAntigo + jogador.preco;
  if (novoGasto > orcamentoAtual()) {
    alert(`Orçamento insuficiente! Faltam €${novoGasto - orcamentoAtual()}M para escalar ${jogador.nome}.`);
    return;
  }
  estadoTime[idx] = jogador;
  fecharPicker();
  renderCampo();
}

function removerDoSlot(idx) {
  estadoTime[idx] = null;
  if (slotAtivo === idx) {
    slotAtivo = null;
    el.pickerHint.style.display = "none";
  }
  renderCampo();
}

function aoClicarJogador(jogador) {
  const idsUsados = new Set(estadoTime.filter(Boolean).map((j) => j.id));
  if (idsUsados.has(jogador.id)) return;

  if (slotAtivo !== null) {
    if (slotsAtuais()[slotAtivo].pos !== jogador.posicao) return;
    escalarJogador(slotAtivo, jogador);
    return;
  }

  const idx = primeiroSlotVazio(jogador.posicao);
  if (idx === -1) {
    alert(`Todas as vagas de ${POS_LABEL[jogador.posicao]} já estão preenchidas. Clique numa posição no campo para substituir.`);
    return;
  }
  escalarJogador(idx, jogador);
}

// ===== RENDER: lista de jogadores disponíveis =====
function renderPlayersList() {
  const filtroSelecao = el.selecaoFilter.value;
  let lista = filtroSelecao ? todosJogadores.filter((j) => j.selecao === filtroSelecao) : todosJogadores;
  if (slotAtivo !== null) {
    const pos = slotsAtuais()[slotAtivo].pos;
    lista = lista.filter((j) => j.posicao === pos);
  }
  const idsUsados = new Set(estadoTime.filter(Boolean).map((j) => j.id));
  el.playersList.innerHTML = lista.map((j) => criarLinhaJogador(j, idsUsados.has(j.id))).join("");
}

// ===== RENDER: campo, box score e orçamento (a partir de estadoTime) =====
function renderCampo() {
  const slots = slotsAtuais();
  const orcamento = orcamentoAtual();

  el.fieldSlots.innerHTML = "";
  el.teamList.innerHTML = "";
  let preenchidos = 0;

  slots.forEach((slot, idx) => {
    const jogador = estadoTime[idx];
    el.teamList.insertAdjacentHTML("beforeend", criarLinhaBoxScore(slot.pos, jogador));

    const div = document.createElement("div");
    div.className = "field-slot" + (jogador ? " filled" : " empty");
    div.dataset.idx = idx;
    div.style.left = slot.x + "%";
    div.style.top = slot.y + "%";

    if (jogador) {
      preenchidos += 1;
      div.innerHTML = `
        <button class="slot-remove" data-idx="${idx}" title="Remover">×</button>
        <div class="slot-circle">${jogador.overall}</div>
        <div class="slot-name">${jogador.nome}</div>
        <div class="slot-price">€${jogador.preco}M</div>
      `;
    } else {
      div.innerHTML = `
        <div class="slot-circle slot-placeholder">+</div>
        <div class="slot-name">${POS_LABEL[slot.pos]}</div>
      `;
    }
    if (slotAtivo === idx) div.classList.add("active");
    el.fieldSlots.appendChild(div);
  });

  el.boxscoreCount.textContent = `${preenchidos}/${slots.length}`;

  const overallTotal = estadoTime.reduce((soma, j) => soma + (j ? j.overall : 0), 0);
  const overallMedio = preenchidos ? Math.round(overallTotal / preenchidos) : 0;
  contarAte(el.overallMedio, overallMedio, 500);

  const gasto = gastoAtual();
  el.gastoValor.textContent = `${gasto}M€`;
  el.orcamentoTotalValor.textContent = `/ ${orcamento}M€`;
  el.sobrouValor.textContent = `${orcamento - gasto}M€`;

  const pct = Math.min(100, Math.round((gasto / orcamento) * 100));
  el.budgetBarFill.style.width = pct + "%";
  el.budgetBarFill.classList.toggle("over-budget", gasto > orcamento);

  renderPlayersList();

  const completoAgora = preenchidos === slots.length;
  if (completoAgora && !timeEstavaCompleto) {
    confetti();
  }
  timeEstavaCompleto = completoAgora;
}

// ===== AÇÕES =====
async function carregarJogadores() {
  const resp = await fetch("/api/jogadores");
  todosJogadores = await resp.json();
  el.totalJogadoresBadge.textContent = todosJogadores.length;
  renderPlayersList();
}

function resetEstadoTime() {
  estadoTime = slotsAtuais().map(() => null);
  slotAtivo = null;
  timeEstavaCompleto = false;
  el.pickerHint.style.display = "none";
}

function selecionarFormacao(formacao) {
  if (formacao === formacaoAtual) return;
  formacaoAtual = formacao;
  el.formacaoAtualLabel.textContent = formacao;
  el.formationGrid.querySelectorAll(".formation-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.formacao === formacao);
  });
  resetEstadoTime();
  renderCampo();
}

async function montarTime() {
  const orcamento = orcamentoAtual();
  const selecao = el.selecaoFilter.value || undefined;

  el.btnMontar.disabled = true;
  el.fieldWrap.classList.add("pulse");

  const resp = await fetch("/api/montar-time", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ orcamento, posicoes: posicoesAtuais(), selecao }),
  });
  const resultado = await resp.json();

  const slots = slotsAtuais();
  const porPosicao = {};
  resultado.jogadores.forEach((j) => {
    (porPosicao[j.posicao] = porPosicao[j.posicao] || []).push(j);
  });
  estadoTime = slots.map((slot) => (porPosicao[slot.pos] || []).shift() || null);
  slotAtivo = null;
  el.pickerHint.style.display = "none";

  setTimeout(() => el.fieldWrap.classList.remove("pulse"), 600);
  renderCampo();

  el.btnMontar.disabled = false;
}

function resetar() {
  resetEstadoTime();
  renderCampo();
}

function compartilhar() {
  const escalados = estadoTime.filter(Boolean);
  if (!escalados.length) {
    alert("Escale pelo menos um jogador primeiro para compartilhar!");
    return;
  }
  const overallTotal = escalados.reduce((s, j) => s + j.overall, 0);
  const overallMedio = Math.round(overallTotal / escalados.length);
  const gasto = gastoAtual();
  const linhas = escalados.map((j) => `${bandeira(j.selecao)} ${j.nome} (${j.overall})`);
  const texto =
    `⚡ Dream Team Builder — Copa 2026\n` +
    `Overall médio: ${overallMedio} | Gasto: €${gasto}M\n\n` +
    linhas.join("\n");

  if (navigator.clipboard) {
    navigator.clipboard.writeText(texto).then(() => alert("Time copiado para a área de transferência!"));
  } else {
    alert(texto);
  }
}

// ===== EVENTOS =====
el.orcamentoSlider.addEventListener("input", () => {
  el.orcamentoValor.textContent = el.orcamentoSlider.value;
  el.capacidadeBadge.textContent = el.orcamentoSlider.value;
  el.orcamentoTotalValor.textContent = `/ ${el.orcamentoSlider.value}M€`;
  const orcamento = orcamentoAtual();
  const gasto = gastoAtual();
  const pct = Math.min(100, Math.round((gasto / orcamento) * 100));
  el.budgetBarFill.style.width = pct + "%";
  el.budgetBarFill.classList.toggle("over-budget", gasto > orcamento);
  el.sobrouValor.textContent = `${orcamento - gasto}M€`;
});

el.formationGrid.addEventListener("click", (e) => {
  const btn = e.target.closest(".formation-btn");
  if (btn) selecionarFormacao(btn.dataset.formacao);
});

el.selecaoFilter.addEventListener("change", renderPlayersList);

el.playersList.addEventListener("click", (e) => {
  const row = e.target.closest(".player-row");
  if (!row || row.classList.contains("used")) return;
  const jogador = todosJogadores.find((j) => j.id === parseInt(row.dataset.id, 10));
  if (jogador) aoClicarJogador(jogador);
});

el.fieldSlots.addEventListener("click", (e) => {
  const removeBtn = e.target.closest(".slot-remove");
  if (removeBtn) {
    removerDoSlot(parseInt(removeBtn.dataset.idx, 10));
    return;
  }
  const slotDiv = e.target.closest(".field-slot");
  if (slotDiv) abrirPicker(parseInt(slotDiv.dataset.idx, 10));
});

el.pickerHintCancelar.addEventListener("click", fecharPicker);

el.btnMontar.addEventListener("click", montarTime);
el.btnResetar.addEventListener("click", resetar);
el.btnCompartilhar.addEventListener("click", compartilhar);

// ===== INIT =====
resetEstadoTime();
renderCampo();
carregarJogadores();

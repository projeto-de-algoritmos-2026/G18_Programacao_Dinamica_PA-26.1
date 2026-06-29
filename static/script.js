// ===== ESTADO =====
let todosJogadores = [];
let timeAtual = null;
let formacaoAtual = "4-3-3";

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
  formationGrid: $("formation-grid"),
  formacaoAtualLabel: $("formacao-atual-label"),
  selecaoFilter: $("selecao-filter"),
  btnMontar: $("btn-montar"),
  playersList: $("players-list"),
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

function criarLinhaJogador(jogador) {
  return `
    <div class="player-row pos-${jogador.posicao}">
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

// ===== RENDER: lista de jogadores disponíveis =====
function renderPlayersList() {
  const filtro = el.selecaoFilter.value;
  const lista = filtro ? todosJogadores.filter((j) => j.selecao === filtro) : todosJogadores;
  el.playersList.innerHTML = lista.map(criarLinhaJogador).join("");
}

// ===== AÇÕES =====
async function carregarJogadores() {
  const resp = await fetch("/api/jogadores");
  todosJogadores = await resp.json();
  renderPlayersList();
}

function posicoesAtuais() {
  return FORMACOES[formacaoAtual].posicoes;
}

function selecionarFormacao(formacao) {
  formacaoAtual = formacao;
  el.formacaoAtualLabel.textContent = formacao;
  el.formationGrid.querySelectorAll(".formation-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.formacao === formacao);
  });
}

async function montarTime() {
  const orcamento = parseInt(el.orcamentoSlider.value, 10);
  const selecao = el.selecaoFilter.value || undefined;

  el.btnMontar.disabled = true;
  el.fieldWrap.classList.add("pulse");

  const resp = await fetch("/api/montar-time", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ orcamento, posicoes: posicoesAtuais(), selecao }),
  });
  const resultado = await resp.json();
  timeAtual = resultado;

  setTimeout(() => el.fieldWrap.classList.remove("pulse"), 600);
  renderTime(resultado, orcamento);

  el.btnMontar.disabled = false;
}

function renderTime(resultado, orcamento) {
  const slots = FORMACOES[formacaoAtual].slots;
  const jogadoresPorPosicao = {};
  resultado.jogadores.forEach((j) => {
    (jogadoresPorPosicao[j.posicao] = jogadoresPorPosicao[j.posicao] || []).push(j);
  });

  el.fieldSlots.innerHTML = "";
  el.teamList.innerHTML = "";
  let delay = 0;
  let preenchidos = 0;

  slots.forEach((slot) => {
    const jogador = (jogadoresPorPosicao[slot.pos] || []).shift();

    el.teamList.insertAdjacentHTML("beforeend", criarLinhaBoxScore(slot.pos, jogador));

    if (!jogador) return;
    preenchidos += 1;

    const div = document.createElement("div");
    div.className = "field-slot";
    div.style.left = slot.x + "%";
    div.style.top = slot.y + "%";
    div.innerHTML = `
      <div class="slot-circle">${jogador.overall}</div>
      <div class="slot-name">${jogador.nome}</div>
      <div class="slot-price">€${jogador.preco}M</div>
    `;
    el.fieldSlots.appendChild(div);
    setTimeout(() => div.classList.add("filled"), delay);
    delay += 150;
  });

  el.boxscoreCount.textContent = `${preenchidos}/${slots.length}`;

  const overallMedio = resultado.jogadores.length
    ? Math.round(resultado.overall_total / resultado.jogadores.length)
    : 0;
  contarAte(el.overallMedio, overallMedio, 800);

  el.gastoValor.textContent = `${resultado.gasto}M€`;
  el.orcamentoTotalValor.textContent = `/ ${orcamento}M€`;
  el.sobrouValor.textContent = `${resultado.sobrou}M€`;

  const pct = Math.min(100, Math.round((resultado.gasto / orcamento) * 100));
  el.budgetBarFill.style.width = pct + "%";
  el.budgetBarFill.classList.toggle("over-budget", resultado.gasto > orcamento);

  if (preenchidos === slots.length) {
    setTimeout(confetti, delay);
  }
}

function resetar() {
  timeAtual = null;
  el.fieldSlots.innerHTML = "";
  el.teamList.innerHTML = "";
  el.boxscoreCount.textContent = `0/${FORMACOES[formacaoAtual].slots.length}`;
  el.overallMedio.textContent = "0";
  el.gastoValor.textContent = "0M€";
  el.orcamentoTotalValor.textContent = `/ ${el.orcamentoSlider.value}M€`;
  el.sobrouValor.textContent = "0M€";
  el.budgetBarFill.style.width = "0%";
  el.budgetBarFill.classList.remove("over-budget");
}

function compartilhar() {
  if (!timeAtual || !timeAtual.jogadores.length) {
    alert("Monte um time primeiro para compartilhar!");
    return;
  }
  const overallMedio = Math.round(timeAtual.overall_total / timeAtual.jogadores.length);
  const linhas = timeAtual.jogadores.map((j) => `${bandeira(j.selecao)} ${j.nome} (${j.overall})`);
  const texto =
    `⚡ Dream Team Builder — Copa 2026\n` +
    `Overall médio: ${overallMedio} | Gasto: €${timeAtual.gasto}M\n\n` +
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
});

el.formationGrid.addEventListener("click", (e) => {
  const btn = e.target.closest(".formation-btn");
  if (btn) selecionarFormacao(btn.dataset.formacao);
});

el.selecaoFilter.addEventListener("change", renderPlayersList);

el.btnMontar.addEventListener("click", montarTime);
el.btnResetar.addEventListener("click", resetar);
el.btnCompartilhar.addEventListener("click", compartilhar);

// ===== INIT =====
resetar();
carregarJogadores();

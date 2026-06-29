from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# DADOS DOS JOGADORES — Copa do Mundo 2026 (preço em milhões de euros)
players = [
    # GOLEIROS
    {"id": 1,  "nome": "Alisson",         "selecao": "Brasil",     "posicao": "GK",  "overall": 88, "preco": 25},
    {"id": 2,  "nome": "Courtois",        "selecao": "Bélgica",    "posicao": "GK",  "overall": 90, "preco": 30},
    {"id": 3,  "nome": "De Gea",          "selecao": "Espanha",    "posicao": "GK",  "overall": 84, "preco": 18},
    {"id": 4,  "nome": "M. Neuer",        "selecao": "Alemanha",   "posicao": "GK",  "overall": 85, "preco": 20},
    {"id": 5,  "nome": "Donnarumma",      "selecao": "Itália",     "posicao": "GK",  "overall": 88, "preco": 26},

    # DEFENSORES
    {"id": 6,  "nome": "Marquinhos",      "selecao": "Brasil",     "posicao": "DEF", "overall": 87, "preco": 28},
    {"id": 7,  "nome": "Militão",         "selecao": "Brasil",     "posicao": "DEF", "overall": 86, "preco": 25},
    {"id": 8,  "nome": "Gvardiol",        "selecao": "Croácia",    "posicao": "DEF", "overall": 87, "preco": 28},
    {"id": 9,  "nome": "Rúben Dias",      "selecao": "Portugal",   "posicao": "DEF", "overall": 88, "preco": 30},
    {"id": 10, "nome": "Van Dijk",        "selecao": "Holanda",    "posicao": "DEF", "overall": 89, "preco": 32},
    {"id": 11, "nome": "Theo Hernández",  "selecao": "França",     "posicao": "DEF", "overall": 86, "preco": 26},
    {"id": 12, "nome": "Cancelo",         "selecao": "Portugal",   "posicao": "DEF", "overall": 85, "preco": 24},
    {"id": 13, "nome": "Trent A-A",       "selecao": "Inglaterra", "posicao": "DEF", "overall": 87, "preco": 29},

    # MEIO-CAMPISTAS
    {"id": 14, "nome": "Casemiro",        "selecao": "Brasil",     "posicao": "MID", "overall": 86, "preco": 25},
    {"id": 15, "nome": "Rodri",           "selecao": "Espanha",    "posicao": "MID", "overall": 91, "preco": 38},
    {"id": 16, "nome": "Kevin De Bruyne", "selecao": "Bélgica",    "posicao": "MID", "overall": 91, "preco": 38},
    {"id": 17, "nome": "Pedri",           "selecao": "Espanha",    "posicao": "MID", "overall": 88, "preco": 30},
    {"id": 18, "nome": "Bellingham",      "selecao": "Inglaterra", "posicao": "MID", "overall": 90, "preco": 36},
    {"id": 19, "nome": "Luka Modrić",     "selecao": "Croácia",    "posicao": "MID", "overall": 87, "preco": 22},
    {"id": 20, "nome": "Fede Valverde",   "selecao": "Uruguai",    "posicao": "MID", "overall": 87, "preco": 28},
    {"id": 21, "nome": "Tchouaméni",      "selecao": "França",     "posicao": "MID", "overall": 85, "preco": 24},
    {"id": 22, "nome": "Gavi",            "selecao": "Espanha",    "posicao": "MID", "overall": 87, "preco": 28},
    {"id": 23, "nome": "Vitinha",         "selecao": "Portugal",   "posicao": "MID", "overall": 85, "preco": 22},

    # ATACANTES
    {"id": 24, "nome": "Neymar Jr",          "selecao": "Brasil",     "posicao": "ATK", "overall": 89, "preco": 35},
    {"id": 25, "nome": "Vinicius Jr",        "selecao": "Brasil",     "posicao": "ATK", "overall": 92, "preco": 45},
    {"id": 26, "nome": "Rodrygo",            "selecao": "Brasil",     "posicao": "ATK", "overall": 86, "preco": 26},
    {"id": 27, "nome": "Messi",              "selecao": "Argentina", "posicao": "ATK", "overall": 94, "preco": 50},
    {"id": 28, "nome": "Cristiano Ronaldo",  "selecao": "Portugal",   "posicao": "ATK", "overall": 90, "preco": 35},
    {"id": 29, "nome": "Mbappé",             "selecao": "França",     "posicao": "ATK", "overall": 93, "preco": 48},
    {"id": 30, "nome": "Haaland",            "selecao": "Noruega",    "posicao": "ATK", "overall": 92, "preco": 46},
    {"id": 31, "nome": "Salah",              "selecao": "Egito",      "posicao": "ATK", "overall": 90, "preco": 36},
    {"id": 32, "nome": "Saka",               "selecao": "Inglaterra", "posicao": "ATK", "overall": 87, "preco": 30},
    {"id": 33, "nome": "Leroy Sané",         "selecao": "Alemanha",   "posicao": "ATK", "overall": 86, "preco": 26},
]


def knapsack_time(jogadores, orcamento):
    """Knapsack 0/1: maximiza overall somado sem exceder o orçamento."""
    n = len(jogadores)
    W = orcamento
    if n == 0 or W <= 0:
        return [], 0

    # dp[i][w] = maior overall somado usando os i primeiros jogadores com orçamento w
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        preco = jogadores[i - 1]["preco"]
        overall = jogadores[i - 1]["overall"]
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]
            if preco <= w:
                dp[i][w] = max(dp[i][w], overall + dp[i - 1][w - preco])

    # backtracking para descobrir quais jogadores foram selecionados
    selecionados = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selecionados.append(jogadores[i - 1])
            w -= jogadores[i - 1]["preco"]

    return selecionados, dp[n][W]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/jogadores", methods=["GET"])
def api_jogadores():
    return jsonify(players)


@app.route("/api/montar-time", methods=["POST"])
def api_montar_time():
    data = request.get_json(force=True) or {}
    orcamento = int(data.get("orcamento", 250))
    posicoes = data.get("posicoes", {"GK": 1, "DEF": 4, "MID": 3, "ATK": 3})
    selecao = data.get("selecao")  # filtro opcional por seleção

    pool = players
    if selecao:
        pool = [p for p in pool if p["selecao"] == selecao]

    total_vagas = sum(posicoes.values()) or 1

    time_final = []
    gasto_total = 0
    overall_total = 0

    for posicao, vagas in posicoes.items():
        if vagas <= 0:
            continue
        candidatos = [p for p in pool if p["posicao"] == posicao]
        orcamento_posicao = int(orcamento * (vagas / total_vagas))

        melhores = []
        orc_restante = orcamento_posicao
        candidatos_restantes = candidatos
        # repete o knapsack "vagas" vezes para preencher cada posição com o
        # melhor jogador possível dentro da fração de orçamento dela
        for _ in range(vagas):
            if not candidatos_restantes or orc_restante <= 0:
                break
            selecionados, _ = knapsack_time(candidatos_restantes, orc_restante)
            if not selecionados:
                break
            escolhido = max(selecionados, key=lambda p: p["overall"])
            melhores.append(escolhido)
            orc_restante -= escolhido["preco"]
            candidatos_restantes = [p for p in candidatos_restantes if p["id"] != escolhido["id"]]

        time_final.extend(melhores)
        gasto_total += sum(p["preco"] for p in melhores)
        overall_total += sum(p["overall"] for p in melhores)

    return jsonify({
        "jogadores": time_final,
        "overall_total": overall_total,
        "gasto": gasto_total,
        "sobrou": orcamento - gasto_total,
    })


if __name__ == "__main__":
    app.run(debug=True)

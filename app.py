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


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

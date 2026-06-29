from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# DADOS DOS JOGADORES — Copa do Mundo 2026 (preço em milhões de euros)
# Cada seleção tem goleiro(s), defesa, meio-campo e ataque completos,
# com opções baratas em todas as posições, para qualquer seleção poder
# ser escalada com qualquer orçamento.
players = [
    # ===== BRASIL =====
    {"nome": "Alisson",          "selecao": "Brasil", "posicao": "GK",  "overall": 88, "preco": 25},
    {"nome": "Ederson",          "selecao": "Brasil", "posicao": "GK",  "overall": 86, "preco": 22},
    {"nome": "Bento",            "selecao": "Brasil", "posicao": "GK",  "overall": 78, "preco": 8},
    {"nome": "Marquinhos",       "selecao": "Brasil", "posicao": "DEF", "overall": 87, "preco": 28},
    {"nome": "Militão",          "selecao": "Brasil", "posicao": "DEF", "overall": 86, "preco": 25},
    {"nome": "Danilo",           "selecao": "Brasil", "posicao": "DEF", "overall": 82, "preco": 14},
    {"nome": "Alex Sandro",      "selecao": "Brasil", "posicao": "DEF", "overall": 80, "preco": 12},
    {"nome": "Bremer",           "selecao": "Brasil", "posicao": "DEF", "overall": 84, "preco": 18},
    {"nome": "Wendell",          "selecao": "Brasil", "posicao": "DEF", "overall": 76, "preco": 6},
    {"nome": "Casemiro",         "selecao": "Brasil", "posicao": "MID", "overall": 86, "preco": 25},
    {"nome": "Lucas Paquetá",    "selecao": "Brasil", "posicao": "MID", "overall": 84, "preco": 20},
    {"nome": "Bruno Guimarães",  "selecao": "Brasil", "posicao": "MID", "overall": 85, "preco": 22},
    {"nome": "André",            "selecao": "Brasil", "posicao": "MID", "overall": 78, "preco": 10},
    {"nome": "Andreas Pereira",  "selecao": "Brasil", "posicao": "MID", "overall": 77, "preco": 9},
    {"nome": "Neymar Jr",        "selecao": "Brasil", "posicao": "ATK", "overall": 89, "preco": 35},
    {"nome": "Vinicius Jr",      "selecao": "Brasil", "posicao": "ATK", "overall": 92, "preco": 45},
    {"nome": "Rodrygo",          "selecao": "Brasil", "posicao": "ATK", "overall": 86, "preco": 26},
    {"nome": "Endrick",          "selecao": "Brasil", "posicao": "ATK", "overall": 82, "preco": 16},
    {"nome": "Raphinha",         "selecao": "Brasil", "posicao": "ATK", "overall": 84, "preco": 20},
    {"nome": "Richarlison",      "selecao": "Brasil", "posicao": "ATK", "overall": 83, "preco": 18},
    {"nome": "Gabriel Martinelli", "selecao": "Brasil", "posicao": "ATK", "overall": 83, "preco": 19},

    # ===== ARGENTINA =====
    {"nome": "Dibu Martínez",    "selecao": "Argentina", "posicao": "GK",  "overall": 88, "preco": 24},
    {"nome": "Gerónimo Rulli",   "selecao": "Argentina", "posicao": "GK",  "overall": 78, "preco": 10},
    {"nome": "Cuti Romero",      "selecao": "Argentina", "posicao": "DEF", "overall": 86, "preco": 24},
    {"nome": "Lisandro Martínez", "selecao": "Argentina", "posicao": "DEF", "overall": 84, "preco": 20},
    {"nome": "Nicolás Tagliafico", "selecao": "Argentina", "posicao": "DEF", "overall": 79, "preco": 10},
    {"nome": "Nahuel Molina",    "selecao": "Argentina", "posicao": "DEF", "overall": 80, "preco": 12},
    {"nome": "Enzo Fernández",   "selecao": "Argentina", "posicao": "MID", "overall": 85, "preco": 24},
    {"nome": "Mac Allister",     "selecao": "Argentina", "posicao": "MID", "overall": 85, "preco": 24},
    {"nome": "Rodrigo De Paul",  "selecao": "Argentina", "posicao": "MID", "overall": 83, "preco": 16},
    {"nome": "Leandro Paredes",  "selecao": "Argentina", "posicao": "MID", "overall": 78, "preco": 9},
    {"nome": "Giovani Lo Celso", "selecao": "Argentina", "posicao": "MID", "overall": 80, "preco": 11},
    {"nome": "Messi",            "selecao": "Argentina", "posicao": "ATK", "overall": 94, "preco": 50},
    {"nome": "Julián Álvarez",   "selecao": "Argentina", "posicao": "ATK", "overall": 88, "preco": 30},
    {"nome": "Lautaro Martínez", "selecao": "Argentina", "posicao": "ATK", "overall": 88, "preco": 30},
    {"nome": "Ángel Di María",   "selecao": "Argentina", "posicao": "ATK", "overall": 84, "preco": 14},
    {"nome": "Nico González",   "selecao": "Argentina", "posicao": "ATK", "overall": 80, "preco": 12},

    # ===== FRANÇA =====
    {"nome": "Mike Maignan",     "selecao": "França", "posicao": "GK",  "overall": 86, "preco": 20},
    {"nome": "Brice Samba",      "selecao": "França", "posicao": "GK",  "overall": 78, "preco": 8},
    {"nome": "Theo Hernández",   "selecao": "França", "posicao": "DEF", "overall": 86, "preco": 26},
    {"nome": "William Saliba",   "selecao": "França", "posicao": "DEF", "overall": 86, "preco": 22},
    {"nome": "Jules Koundé",     "selecao": "França", "posicao": "DEF", "overall": 85, "preco": 20},
    {"nome": "Ibrahima Konaté",  "selecao": "França", "posicao": "DEF", "overall": 83, "preco": 16},
    {"nome": "Benjamin Pavard",  "selecao": "França", "posicao": "DEF", "overall": 80, "preco": 12},
    {"nome": "Tchouaméni",       "selecao": "França", "posicao": "MID", "overall": 85, "preco": 24},
    {"nome": "N'Golo Kanté",     "selecao": "França", "posicao": "MID", "overall": 85, "preco": 18},
    {"nome": "Eduardo Camavinga", "selecao": "França", "posicao": "MID", "overall": 84, "preco": 20},
    {"nome": "Antoine Griezmann", "selecao": "França", "posicao": "MID", "overall": 88, "preco": 26},
    {"nome": "Warren Zaïre-Emery", "selecao": "França", "posicao": "MID", "overall": 80, "preco": 14},
    {"nome": "Mbappé",           "selecao": "França", "posicao": "ATK", "overall": 93, "preco": 48},
    {"nome": "Ousmane Dembélé",  "selecao": "França", "posicao": "ATK", "overall": 86, "preco": 22},
    {"nome": "Marcus Thuram",    "selecao": "França", "posicao": "ATK", "overall": 85, "preco": 20},
    {"nome": "Bradley Barcola",  "selecao": "França", "posicao": "ATK", "overall": 81, "preco": 14},
    {"nome": "Randal Kolo Muani", "selecao": "França", "posicao": "ATK", "overall": 82, "preco": 15},

    # ===== PORTUGAL =====
    {"nome": "Diogo Costa",      "selecao": "Portugal", "posicao": "GK",  "overall": 85, "preco": 18},
    {"nome": "Rui Patrício",     "selecao": "Portugal", "posicao": "GK",  "overall": 80, "preco": 9},
    {"nome": "Rúben Dias",       "selecao": "Portugal", "posicao": "DEF", "overall": 88, "preco": 30},
    {"nome": "Cancelo",          "selecao": "Portugal", "posicao": "DEF", "overall": 85, "preco": 24},
    {"nome": "Nélson Semedo",    "selecao": "Portugal", "posicao": "DEF", "overall": 79, "preco": 10},
    {"nome": "António Silva",    "selecao": "Portugal", "posicao": "DEF", "overall": 82, "preco": 14},
    {"nome": "Diogo Dalot",      "selecao": "Portugal", "posicao": "DEF", "overall": 80, "preco": 11},
    {"nome": "Gonçalo Inácio",   "selecao": "Portugal", "posicao": "DEF", "overall": 80, "preco": 12},
    {"nome": "Bruno Fernandes",  "selecao": "Portugal", "posicao": "MID", "overall": 87, "preco": 26},
    {"nome": "Vitinha",          "selecao": "Portugal", "posicao": "MID", "overall": 85, "preco": 22},
    {"nome": "João Palhinha",    "selecao": "Portugal", "posicao": "MID", "overall": 84, "preco": 18},
    {"nome": "Bernardo Silva",   "selecao": "Portugal", "posicao": "MID", "overall": 88, "preco": 28},
    {"nome": "João Neves",       "selecao": "Portugal", "posicao": "MID", "overall": 81, "preco": 14},
    {"nome": "Cristiano Ronaldo", "selecao": "Portugal", "posicao": "ATK", "overall": 90, "preco": 35},
    {"nome": "João Félix",       "selecao": "Portugal", "posicao": "ATK", "overall": 83, "preco": 18},
    {"nome": "Rafael Leão",      "selecao": "Portugal", "posicao": "ATK", "overall": 85, "preco": 22},
    {"nome": "Gonçalo Ramos",    "selecao": "Portugal", "posicao": "ATK", "overall": 82, "preco": 16},
    {"nome": "Diogo Jota",       "selecao": "Portugal", "posicao": "ATK", "overall": 85, "preco": 20},

    # ===== BÉLGICA =====
    {"nome": "Courtois",         "selecao": "Bélgica", "posicao": "GK",  "overall": 90, "preco": 30},
    {"nome": "Koen Casteels",    "selecao": "Bélgica", "posicao": "GK",  "overall": 78, "preco": 8},
    {"nome": "Jan Vertonghen",   "selecao": "Bélgica", "posicao": "DEF", "overall": 79, "preco": 8},
    {"nome": "Wout Faes",        "selecao": "Bélgica", "posicao": "DEF", "overall": 78, "preco": 9},
    {"nome": "Arthur Theate",    "selecao": "Bélgica", "posicao": "DEF", "overall": 78, "preco": 9},
    {"nome": "Timothy Castagne", "selecao": "Bélgica", "posicao": "DEF", "overall": 79, "preco": 10},
    {"nome": "Kevin De Bruyne",  "selecao": "Bélgica", "posicao": "MID", "overall": 91, "preco": 38},
    {"nome": "Youri Tielemans",  "selecao": "Bélgica", "posicao": "MID", "overall": 83, "preco": 16},
    {"nome": "Amadou Onana",     "selecao": "Bélgica", "posicao": "MID", "overall": 82, "preco": 14},
    {"nome": "Leandro Trossard",  "selecao": "Bélgica", "posicao": "MID", "overall": 82, "preco": 15},
    {"nome": "Axel Witsel",      "selecao": "Bélgica", "posicao": "MID", "overall": 78, "preco": 8},
    {"nome": "Romelu Lukaku",    "selecao": "Bélgica", "posicao": "ATK", "overall": 86, "preco": 22},
    {"nome": "Jérémy Doku",      "selecao": "Bélgica", "posicao": "ATK", "overall": 83, "preco": 18},
    {"nome": "Loïs Openda",      "selecao": "Bélgica", "posicao": "ATK", "overall": 83, "preco": 18},
    {"nome": "Charles De Ketelaere", "selecao": "Bélgica", "posicao": "ATK", "overall": 79, "preco": 11},

    # ===== ESPANHA =====
    {"nome": "De Gea",           "selecao": "Espanha", "posicao": "GK",  "overall": 84, "preco": 18},
    {"nome": "Unai Simón",       "selecao": "Espanha", "posicao": "GK",  "overall": 83, "preco": 14},
    {"nome": "Robin Le Normand", "selecao": "Espanha", "posicao": "DEF", "overall": 82, "preco": 16},
    {"nome": "Aymeric Laporte",  "selecao": "Espanha", "posicao": "DEF", "overall": 83, "preco": 15},
    {"nome": "Daniel Carvajal",  "selecao": "Espanha", "posicao": "DEF", "overall": 84, "preco": 18},
    {"nome": "Marc Cucurella",   "selecao": "Espanha", "posicao": "DEF", "overall": 80, "preco": 12},
    {"nome": "Jesús Navas",      "selecao": "Espanha", "posicao": "DEF", "overall": 76, "preco": 6},
    {"nome": "Rodri",            "selecao": "Espanha", "posicao": "MID", "overall": 91, "preco": 38},
    {"nome": "Pedri",            "selecao": "Espanha", "posicao": "MID", "overall": 88, "preco": 30},
    {"nome": "Gavi",             "selecao": "Espanha", "posicao": "MID", "overall": 87, "preco": 28},
    {"nome": "Fabián Ruiz",      "selecao": "Espanha", "posicao": "MID", "overall": 82, "preco": 14},
    {"nome": "Mikel Merino",     "selecao": "Espanha", "posicao": "MID", "overall": 80, "preco": 12},
    {"nome": "Lamine Yamal",     "selecao": "Espanha", "posicao": "ATK", "overall": 87, "preco": 24},
    {"nome": "Álvaro Morata",    "selecao": "Espanha", "posicao": "ATK", "overall": 83, "preco": 18},
    {"nome": "Nico Williams",    "selecao": "Espanha", "posicao": "ATK", "overall": 84, "preco": 20},
    {"nome": "Ferran Torres",    "selecao": "Espanha", "posicao": "ATK", "overall": 81, "preco": 14},

    # ===== INGLATERRA =====
    {"nome": "Jordan Pickford",  "selecao": "Inglaterra", "posicao": "GK",  "overall": 82, "preco": 14},
    {"nome": "Aaron Ramsdale",   "selecao": "Inglaterra", "posicao": "GK",  "overall": 78, "preco": 9},
    {"nome": "Trent A-A",        "selecao": "Inglaterra", "posicao": "DEF", "overall": 87, "preco": 29},
    {"nome": "John Stones",      "selecao": "Inglaterra", "posicao": "DEF", "overall": 85, "preco": 20},
    {"nome": "Marc Guéhi",       "selecao": "Inglaterra", "posicao": "DEF", "overall": 80, "preco": 12},
    {"nome": "Luke Shaw",        "selecao": "Inglaterra", "posicao": "DEF", "overall": 81, "preco": 13},
    {"nome": "Kyle Walker",      "selecao": "Inglaterra", "posicao": "DEF", "overall": 83, "preco": 16},
    {"nome": "Bellingham",       "selecao": "Inglaterra", "posicao": "MID", "overall": 90, "preco": 36},
    {"nome": "Declan Rice",      "selecao": "Inglaterra", "posicao": "MID", "overall": 86, "preco": 22},
    {"nome": "Conor Gallagher",  "selecao": "Inglaterra", "posicao": "MID", "overall": 79, "preco": 10},
    {"nome": "Phil Foden",       "selecao": "Inglaterra", "posicao": "MID", "overall": 87, "preco": 26},
    {"nome": "Kobbie Mainoo",    "selecao": "Inglaterra", "posicao": "MID", "overall": 80, "preco": 12},
    {"nome": "Saka",             "selecao": "Inglaterra", "posicao": "ATK", "overall": 87, "preco": 30},
    {"nome": "Harry Kane",       "selecao": "Inglaterra", "posicao": "ATK", "overall": 91, "preco": 34},
    {"nome": "Cole Palmer",      "selecao": "Inglaterra", "posicao": "ATK", "overall": 85, "preco": 22},
    {"nome": "Ivan Toney",       "selecao": "Inglaterra", "posicao": "ATK", "overall": 81, "preco": 14},
    {"nome": "Anthony Gordon",   "selecao": "Inglaterra", "posicao": "ATK", "overall": 80, "preco": 12},

    # ===== ALEMANHA =====
    {"nome": "M. Neuer",         "selecao": "Alemanha", "posicao": "GK",  "overall": 85, "preco": 20},
    {"nome": "ter Stegen",       "selecao": "Alemanha", "posicao": "GK",  "overall": 87, "preco": 22},
    {"nome": "Antonio Rüdiger",  "selecao": "Alemanha", "posicao": "DEF", "overall": 85, "preco": 18},
    {"nome": "Jonathan Tah",     "selecao": "Alemanha", "posicao": "DEF", "overall": 82, "preco": 14},
    {"nome": "David Raum",       "selecao": "Alemanha", "posicao": "DEF", "overall": 79, "preco": 10},
    {"nome": "Nico Schlotterbeck", "selecao": "Alemanha", "posicao": "DEF", "overall": 81, "preco": 13},
    {"nome": "Joshua Kimmich",   "selecao": "Alemanha", "posicao": "MID", "overall": 87, "preco": 24},
    {"nome": "Ilkay Gündogan",   "selecao": "Alemanha", "posicao": "MID", "overall": 85, "preco": 20},
    {"nome": "Jamal Musiala",    "selecao": "Alemanha", "posicao": "MID", "overall": 87, "preco": 26},
    {"nome": "Florian Wirtz",    "selecao": "Alemanha", "posicao": "MID", "overall": 86, "preco": 24},
    {"nome": "Robert Andrich",   "selecao": "Alemanha", "posicao": "MID", "overall": 78, "preco": 9},
    {"nome": "Leroy Sané",       "selecao": "Alemanha", "posicao": "ATK", "overall": 86, "preco": 26},
    {"nome": "Kai Havertz",      "selecao": "Alemanha", "posicao": "ATK", "overall": 84, "preco": 20},
    {"nome": "Niclas Füllkrug",  "selecao": "Alemanha", "posicao": "ATK", "overall": 81, "preco": 14},
    {"nome": "Serge Gnabry",     "selecao": "Alemanha", "posicao": "ATK", "overall": 82, "preco": 15},
    {"nome": "Deniz Undav",      "selecao": "Alemanha", "posicao": "ATK", "overall": 79, "preco": 11},

    # ===== HOLANDA =====
    {"nome": "Bart Verbruggen",  "selecao": "Holanda", "posicao": "GK",  "overall": 79, "preco": 10},
    {"nome": "Justin Bijlow",    "selecao": "Holanda", "posicao": "GK",  "overall": 77, "preco": 8},
    {"nome": "Van Dijk",         "selecao": "Holanda", "posicao": "DEF", "overall": 89, "preco": 32},
    {"nome": "Jurrien Timber",   "selecao": "Holanda", "posicao": "DEF", "overall": 83, "preco": 16},
    {"nome": "Nathan Aké",       "selecao": "Holanda", "posicao": "DEF", "overall": 82, "preco": 14},
    {"nome": "Denzel Dumfries",  "selecao": "Holanda", "posicao": "DEF", "overall": 83, "preco": 16},
    {"nome": "Lutsharel Geertruida", "selecao": "Holanda", "posicao": "DEF", "overall": 79, "preco": 10},
    {"nome": "Frenkie de Jong",  "selecao": "Holanda", "posicao": "MID", "overall": 87, "preco": 26},
    {"nome": "Tijjani Reijnders", "selecao": "Holanda", "posicao": "MID", "overall": 82, "preco": 15},
    {"nome": "Xavi Simons",      "selecao": "Holanda", "posicao": "MID", "overall": 84, "preco": 19},
    {"nome": "Marten de Roon",   "selecao": "Holanda", "posicao": "MID", "overall": 76, "preco": 7},
    {"nome": "Teun Koopmeiners", "selecao": "Holanda", "posicao": "MID", "overall": 82, "preco": 15},
    {"nome": "Memphis Depay",    "selecao": "Holanda", "posicao": "ATK", "overall": 84, "preco": 20},
    {"nome": "Cody Gakpo",       "selecao": "Holanda", "posicao": "ATK", "overall": 84, "preco": 20},
    {"nome": "Donyell Malen",    "selecao": "Holanda", "posicao": "ATK", "overall": 81, "preco": 14},

    # ===== CROÁCIA =====
    {"nome": "Dominik Livaković", "selecao": "Croácia", "posicao": "GK",  "overall": 83, "preco": 16},
    {"nome": "Ivica Ivušić",     "selecao": "Croácia", "posicao": "GK",  "overall": 74, "preco": 5},
    {"nome": "Gvardiol",         "selecao": "Croácia", "posicao": "DEF", "overall": 87, "preco": 28},
    {"nome": "Josip Stanišić",   "selecao": "Croácia", "posicao": "DEF", "overall": 78, "preco": 9},
    {"nome": "Borna Sosa",       "selecao": "Croácia", "posicao": "DEF", "overall": 78, "preco": 9},
    {"nome": "Josip Šutalo",     "selecao": "Croácia", "posicao": "DEF", "overall": 79, "preco": 10},
    {"nome": "Domagoj Vida",     "selecao": "Croácia", "posicao": "DEF", "overall": 76, "preco": 6},
    {"nome": "Luka Modrić",      "selecao": "Croácia", "posicao": "MID", "overall": 87, "preco": 22},
    {"nome": "Mateo Kovačić",    "selecao": "Croácia", "posicao": "MID", "overall": 85, "preco": 20},
    {"nome": "Marcelo Brozović", "selecao": "Croácia", "posicao": "MID", "overall": 83, "preco": 15},
    {"nome": "Lovro Majer",      "selecao": "Croácia", "posicao": "MID", "overall": 80, "preco": 12},
    {"nome": "Luka Sučić",       "selecao": "Croácia", "posicao": "MID", "overall": 79, "preco": 11},
    {"nome": "Andrej Kramarić",  "selecao": "Croácia", "posicao": "ATK", "overall": 83, "preco": 16},
    {"nome": "Ante Budimir",     "selecao": "Croácia", "posicao": "ATK", "overall": 79, "preco": 10},
    {"nome": "Bruno Petković",   "selecao": "Croácia", "posicao": "ATK", "overall": 79, "preco": 10},

    # ===== URUGUAI =====
    {"nome": "Sergio Rochet",    "selecao": "Uruguai", "posicao": "GK",  "overall": 78, "preco": 9},
    {"nome": "José María Giménez", "selecao": "Uruguai", "posicao": "DEF", "overall": 84, "preco": 18},
    {"nome": "Ronald Araújo",    "selecao": "Uruguai", "posicao": "DEF", "overall": 85, "preco": 20},
    {"nome": "Mathías Olivera",  "selecao": "Uruguai", "posicao": "DEF", "overall": 80, "preco": 12},
    {"nome": "Guillermo Varela", "selecao": "Uruguai", "posicao": "DEF", "overall": 77, "preco": 8},
    {"nome": "Fede Valverde",    "selecao": "Uruguai", "posicao": "MID", "overall": 87, "preco": 28},
    {"nome": "Manuel Ugarte",    "selecao": "Uruguai", "posicao": "MID", "overall": 81, "preco": 14},
    {"nome": "Rodrigo Bentancur", "selecao": "Uruguai", "posicao": "MID", "overall": 83, "preco": 16},
    {"nome": "Nicolás de la Cruz", "selecao": "Uruguai", "posicao": "MID", "overall": 79, "preco": 10},
    {"nome": "Nahitan Nández",   "selecao": "Uruguai", "posicao": "MID", "overall": 80, "preco": 12},
    {"nome": "Darwin Núñez",     "selecao": "Uruguai", "posicao": "ATK", "overall": 85, "preco": 22},
    {"nome": "Luis Suárez",      "selecao": "Uruguai", "posicao": "ATK", "overall": 84, "preco": 16},
    {"nome": "Facundo Pellistri", "selecao": "Uruguai", "posicao": "ATK", "overall": 78, "preco": 10},

    # ===== NORUEGA =====
    {"nome": "Ørjan Nyland",     "selecao": "Noruega", "posicao": "GK",  "overall": 75, "preco": 5},
    {"nome": "Stian Gregersen",  "selecao": "Noruega", "posicao": "DEF", "overall": 76, "preco": 7},
    {"nome": "Leo Østigård",     "selecao": "Noruega", "posicao": "DEF", "overall": 76, "preco": 7},
    {"nome": "Birger Meling",    "selecao": "Noruega", "posicao": "DEF", "overall": 75, "preco": 6},
    {"nome": "Fredrik Bjørkan",  "selecao": "Noruega", "posicao": "DEF", "overall": 74, "preco": 5},
    {"nome": "Martin Ødegaard",  "selecao": "Noruega", "posicao": "MID", "overall": 87, "preco": 26},
    {"nome": "Sander Berge",     "selecao": "Noruega", "posicao": "MID", "overall": 79, "preco": 10},
    {"nome": "Morten Thorsby",   "selecao": "Noruega", "posicao": "MID", "overall": 77, "preco": 8},
    {"nome": "Kristian Thorstvedt", "selecao": "Noruega", "posicao": "MID", "overall": 78, "preco": 9},
    {"nome": "Fredrik Aursnes",  "selecao": "Noruega", "posicao": "MID", "overall": 78, "preco": 9},
    {"nome": "Haaland",          "selecao": "Noruega", "posicao": "ATK", "overall": 92, "preco": 46},
    {"nome": "Alexander Sørloth", "selecao": "Noruega", "posicao": "ATK", "overall": 81, "preco": 14},
    {"nome": "Ola Solbakken",    "selecao": "Noruega", "posicao": "ATK", "overall": 76, "preco": 7},

    # ===== EGITO =====
    {"nome": "Mohamed El Shenawy", "selecao": "Egito", "posicao": "GK",  "overall": 77, "preco": 8},
    {"nome": "Ahmed Hegazi",     "selecao": "Egito", "posicao": "DEF", "overall": 78, "preco": 9},
    {"nome": "Mohamed Abdelmonem", "selecao": "Egito", "posicao": "DEF", "overall": 76, "preco": 7},
    {"nome": "Ayman Ashraf",     "selecao": "Egito", "posicao": "DEF", "overall": 75, "preco": 6},
    {"nome": "Rami Rabia",       "selecao": "Egito", "posicao": "DEF", "overall": 76, "preco": 7},
    {"nome": "Mohamed Elneny",   "selecao": "Egito", "posicao": "MID", "overall": 78, "preco": 9},
    {"nome": "Hamdi Fathi",      "selecao": "Egito", "posicao": "MID", "overall": 76, "preco": 7},
    {"nome": "Emam Ashour",      "selecao": "Egito", "posicao": "MID", "overall": 78, "preco": 9},
    {"nome": "Mohamed Magdy (Afsha)", "selecao": "Egito", "posicao": "MID", "overall": 78, "preco": 9},
    {"nome": "Akram Tawfik",     "selecao": "Egito", "posicao": "MID", "overall": 75, "preco": 6},
    {"nome": "Salah",            "selecao": "Egito", "posicao": "ATK", "overall": 90, "preco": 36},
    {"nome": "Mostafa Mohamed",  "selecao": "Egito", "posicao": "ATK", "overall": 79, "preco": 11},
    {"nome": "Omar Marmoush",    "selecao": "Egito", "posicao": "ATK", "overall": 82, "preco": 15},
    {"nome": "Trezeguet (M. Hassan)", "selecao": "Egito", "posicao": "ATK", "overall": 78, "preco": 10},

    # ===== ITÁLIA =====
    {"nome": "Donnarumma",       "selecao": "Itália", "posicao": "GK",  "overall": 88, "preco": 26},
    {"nome": "Alex Meret",       "selecao": "Itália", "posicao": "GK",  "overall": 80, "preco": 12},
    {"nome": "Giovanni Di Lorenzo", "selecao": "Itália", "posicao": "DEF", "overall": 83, "preco": 15},
    {"nome": "Alessandro Bastoni", "selecao": "Itália", "posicao": "DEF", "overall": 84, "preco": 18},
    {"nome": "Federico Dimarco", "selecao": "Itália", "posicao": "DEF", "overall": 82, "preco": 14},
    {"nome": "Riccardo Calafiori", "selecao": "Itália", "posicao": "DEF", "overall": 81, "preco": 13},
    {"nome": "Nicolò Barella",   "selecao": "Itália", "posicao": "MID", "overall": 86, "preco": 22},
    {"nome": "Jorginho",         "selecao": "Itália", "posicao": "MID", "overall": 81, "preco": 13},
    {"nome": "Davide Frattesi",  "selecao": "Itália", "posicao": "MID", "overall": 80, "preco": 12},
    {"nome": "Sandro Tonali",    "selecao": "Itália", "posicao": "MID", "overall": 84, "preco": 18},
    {"nome": "Lorenzo Pellegrini", "selecao": "Itália", "posicao": "MID", "overall": 81, "preco": 14},
    {"nome": "Federico Chiesa",  "selecao": "Itália", "posicao": "ATK", "overall": 84, "preco": 18},
    {"nome": "Moise Kean",       "selecao": "Itália", "posicao": "ATK", "overall": 80, "preco": 12},
    {"nome": "Mateo Retegui",    "selecao": "Itália", "posicao": "ATK", "overall": 81, "preco": 13},
    {"nome": "Gianluca Scamacca", "selecao": "Itália", "posicao": "ATK", "overall": 80, "preco": 12},
]

# atribui um id sequencial e estável para cada jogador
for indice, jogador in enumerate(players, start=1):
    jogador["id"] = indice


NEG = float("-inf")


def _tabela_posicao(jogadores, vagas, W):
    """Knapsack 0/1 com limite de itens: dp[i][k][w] = maior overall
    somado escolhendo EXATAMENTE k jogadores distintos entre os i
    primeiros candidatos dessa posição, com custo total <= w. A
    dimensão k é o que diferencia esse knapsack do clássico — sem ela,
    o algoritmo poderia gastar tudo em poucos jogadores caros e deixar
    vagas vazias mesmo havendo opções baratas. Manter a dimensão i (em
    vez de só atualizar uma tabela 2D in-place) é o que permite
    recuperar exatamente quais jogadores foram escolhidos por
    backtracking, sem o risco de reaproveitar o mesmo jogador duas
    vezes em vagas diferentes.
    """
    n = len(jogadores)
    dp = [[[0] * (W + 1) for _ in range(vagas + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for k in range(1, vagas + 1):
            for w in range(W + 1):
                dp[i][k][w] = NEG

    for i in range(1, n + 1):
        preco, overall = jogadores[i - 1]["preco"], jogadores[i - 1]["overall"]
        for k in range(vagas + 1):
            for w in range(W + 1):
                melhor = dp[i - 1][k][w]
                if k > 0 and preco <= w and dp[i - 1][k - 1][w - preco] != NEG:
                    candidato = dp[i - 1][k - 1][w - preco] + overall
                    if candidato > melhor:
                        melhor = candidato
                dp[i][k][w] = melhor

    return dp


def _recupera_selecionados(dp, jogadores, vagas, w):
    selecionados = []
    i, k = len(jogadores), vagas
    while i > 0 and k > 0:
        preco, overall = jogadores[i - 1]["preco"], jogadores[i - 1]["overall"]
        if (
            preco <= w
            and dp[i - 1][k - 1][w - preco] != NEG
            and dp[i - 1][k - 1][w - preco] + overall == dp[i][k][w]
        ):
            selecionados.append(jogadores[i - 1])
            k -= 1
            w -= preco
        i -= 1
    return selecionados


def _combina_orcamento(f, g, W):
    """Convolução (max, +): combina duas posições que disputam o mesmo
    orçamento total, testando toda divisão possível w1 + w2 <= w entre
    elas. Sem essa combinação, dividir o orçamento por posição de forma
    fixa e proporcional deixa "sobras" presas numa posição barata (ex.
    goleiro) que não podem ser usadas para cobrir uma posição cara (ex.
    ataque), e o time acaba incompleto mesmo havendo orçamento total
    suficiente.
    """
    h = [NEG] * (W + 1)
    divisao = [0] * (W + 1)
    for w in range(W + 1):
        melhor, melhor_w1 = NEG, 0
        for w1 in range(w + 1):
            if f[w1] == NEG or g[w - w1] == NEG:
                continue
            valor = f[w1] + g[w - w1]
            if valor > melhor:
                melhor, melhor_w1 = valor, w1
        h[w] = melhor
        divisao[w] = melhor_w1
    return h, divisao


def montar_time(pool, posicoes, orcamento):
    """Escala o time inteiro maximizando o overall total dentro de um
    único orçamento compartilhado entre todas as posições."""
    W = max(orcamento, 0)
    grupos = []
    for posicao, vagas in posicoes.items():
        if vagas <= 0:
            continue
        candidatos = [p for p in pool if p["posicao"] == posicao]
        dp = _tabela_posicao(candidatos, vagas, W)
        grupos.append((candidatos, vagas, dp, dp[len(candidatos)][vagas]))

    if not grupos:
        return [], 0, 0

    total = grupos[0][3]
    divisoes = []
    for _, _, _, dp_row in grupos[1:]:
        total, divisao = _combina_orcamento(total, dp_row, W)
        divisoes.append(divisao)

    if total[W] == NEG:
        return [], 0, 0

    # recupera quanto do orçamento coube a cada posição, de trás para frente
    n = len(grupos)
    orcamento_por_grupo = [0] * n
    w_restante = W
    for i in range(n - 1, 0, -1):
        w1 = divisoes[i - 1][w_restante]
        orcamento_por_grupo[i] = w_restante - w1
        w_restante = w1
    orcamento_por_grupo[0] = w_restante

    time_final, overall_total, gasto_total = [], 0, 0
    for (candidatos, vagas, dp, _dp_row), w_grupo in zip(grupos, orcamento_por_grupo):
        selecionados = _recupera_selecionados(dp, candidatos, vagas, w_grupo)
        time_final.extend(selecionados)
        overall_total += sum(p["overall"] for p in selecionados)
        gasto_total += sum(p["preco"] for p in selecionados)

    return time_final, overall_total, gasto_total


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

    time_final, overall_total, gasto_total = montar_time(pool, posicoes, orcamento)

    return jsonify({
        "jogadores": time_final,
        "overall_total": overall_total,
        "gasto": gasto_total,
        "sobrou": orcamento - gasto_total,
    })


if __name__ == "__main__":
    app.run(debug=True)

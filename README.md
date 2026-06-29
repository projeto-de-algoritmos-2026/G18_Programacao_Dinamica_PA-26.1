# G18\_Programacao\_Dinamica\_PA-26.1

**Número da Lista**: 18<br>
**Conteúdo da Disciplina**: Programação Dinâmica<br>

## Alunos

| Matrícula | Aluno |
| -- | -- |
| 202016382 | Guilherme Meister Correa |
| 202063462 | Samuel Alves Silva |

## Sobre

Este projeto implementa o **Problema da Mochila (Knapsack 0/1)** aplicado a um cenário de futebol — montar a melhor seleção possível para a Copa do Mundo 2026 dentro de um orçamento limitado.

Um catálogo com mais de 220 jogadores (goleiros, defensores, meio-campistas e atacantes) das 14 maiores seleções, cada um com **overall** (nota) e **preço** (em milhões de euros), é usado como entrada. A interface é inspirada no jogo viral **7a0 (Sete a Zero)**: o usuário pode escolher manualmente cada jogador, posição por posição, clicando na lista ou diretamente no campo — ou apertar **SUGESTÃO AUTOMÁTICA** para que o algoritmo de **programação dinâmica** monte a escalação que maximiza o overall total sem ultrapassar o orçamento, deixando o orçamento fluir livremente entre as posições (veja [Outros](#outros)).

O resultado é exibido em uma interface web interativa (Flask + JS), com:

| Elemento | Descrição |
|---|---|
| Painel de controles | Slider de orçamento, escolha de formação, filtro por seleção e lista clicável de jogadores |
| Campo tático | Os 11 slots da formação, preenchidos manualmente ou pela sugestão automática |
| Box score | Overall médio do time, gasto total, valor restante e lista dos titulares |

## Apresentação

[![Apresentação em Vídeo](https://img.youtube.com/vi/2fCs750-sRM/0.jpg)](https://youtu.be/2fCs750-sRM)

## Screenshots

*(adicione aqui prints da aplicação rodando, ex.: `assets/dream-team.png`)*

## Instalação

**Linguagem**: Python 3.8+<br>
**Dependências**: `Flask`

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G18_Programacao_Dinamica_PA-26.1.git
cd G18_Programacao_Dinamica_PA-26.1
pip install flask
```

## Uso

Execute o servidor Flask na raiz do repositório:

```bash
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador. Na interface:

1. Ajuste o **orçamento** (em milhões de euros) usando o slider.
2. Escolha a **formação** (4-3-3, 4-4-2 ou 3-5-2).
3. (Opcional) **Filtre por seleção** para montar um time apenas com jogadores de um país.
4. **Escolha manualmente**: clique num jogador da lista para escalá-lo na primeira vaga livre da posição dele, ou clique numa posição já preenchida no campo para substituir o titular. Clique no **×** de um slot para esvaziá-lo.
5. Ou clique em **⚡ SUGESTÃO AUTOMÁTICA** para que o algoritmo monte a melhor escalação dentro do orçamento de uma vez.
6. Use **RESETAR** para limpar o time montado e **COMPARTILHAR** para copiar a escalação como texto.

## Outros

### Como funciona a Programação Dinâmica (Knapsack 0/1)

```
knapsack_time(jogadores, orcamento):
    dp[i][w] = maior overall somado usando os i primeiros jogadores
               com orçamento w

    para cada jogador i (1..n):
        para cada orçamento w (0..W):
            dp[i][w] = dp[i-1][w]                                  # não pega o jogador i
            se preco[i] <= w:
                dp[i][w] = max(dp[i][w], overall[i] + dp[i-1][w-preco[i]])  # pega o jogador i

    backtracking em dp para recuperar quais jogadores foram selecionados
```

- **Subestrutura ótima**: a melhor escolha entre os i primeiros jogadores depende apenas da melhor escolha entre os i−1 primeiros.
- **Subproblemas sobrepostos**: `dp[i][w]` é reaproveitado por várias combinações de jogadores e orçamentos, por isso a tabela evita recomputação.
- **Complexidade**: O(n · W), onde n é o número de jogadores e W é o orçamento (capacidade da mochila).

No `app.py`, o orçamento total é dividido proporcionalmente entre as posições da formação (GK, DEF, MID, ATK) e o knapsack é resolvido posição a posição, escolhendo a cada rodada o jogador de maior overall dentro do conjunto ótimo retornado, até preencher todas as vagas.

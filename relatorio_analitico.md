# Relatório Analítico – Análise de Redes

---


## 1. Distribuição de graus

**Pergunta:**  
Qual é a distribuição de graus de ambos os grafos? Essa distribuição apresenta características típicas de redes complexas?

**Resposta:**  
[Inserir texto explicativo]  
[Inserir histogramas e gráficos de distribuição]

---

## 2. Componentes conexas

**Pergunta:**  
Quantas componentes conexas (grafo não-direcionado) e fortemente conexas (grafo direcionado) existem? Qual a distribuição de ordem dessas componentes (número de vértices)? O que essa distribuição indica sobre as características do problema?

**Resposta:**  
[Inserir texto explicativo]  
[Inserir gráficos ou tabelas com os tamanhos das componentes]

---

## 3. Centralidade de grau (grafo direcionado)

**Pergunta:**  
Quais são os 10 diretores mais influentes perante a métrica de centralidade de grau? O que essa métrica representa nesse contexto?

**Resposta:**  
```python
dg_centrality = dg.degree_centrality(1) # 1 para indegree, 2 para outdegree, 0 para total degree
print("Top 10 diretores mais influentes(direcionado):") #diretores é indg devido as especificações do TDE
for node, value in sorted(dg_centrality.items(), key=lambda x: x[1], reverse=True)[:10]: # o que muda é o [:10] que limita a 10 os resultados
    print(f"{node} - {value:.4f}")
```

| Rank| Diretor             | $C_{\text{Grau}}^{\text{In}}$ |
| ---- | ------------------- | ----------------------------- |
| 1    | MARTIN SCORSESE     | 0.0021                        |
| 2    | STEVEN SPIELBERG    | 0.0021                        |
| 3    | JOSEPH KANE         | 0.0019                        |
| 4    | DON MICHAEL PAUL    | 0.0018                        |
| 5    | DIBAKAR BANERJEE    | 0.0016                        |
| 6    | STEVE BRILL         | 0.0016                        |
| 7    | ROBERT RODRIGUEZ    | 0.0016                        |
| 8    | CATHY GARCIA-MOLINA | 0.0016                        |
| 9    | PAUL HOEN           | 0.0015                        |
| 10   | RON HOWARD          | 0.0015                        |

Cada aresta aponta de um ator para o diretor que o dirigiu, esse é o motivo pelo qual somente o grau de entrada de um nó é puxado, para indicar quantos atores estiveram sob a direção desse diretor. (Se tem ao menos um, mesmo que o diretor tenha atuado em algum filme julguei que ele pode ser considerado um direc. Não é exclusivo ser um **ou** outro)

Diretores que tem a centralidade de grau maior conectam mais atores e comunidades de atores entre si, como se fosse um "dente-de-leão".

![exemplo de imagem que representa as conexões em formato de dente-de-leão](./img/centGrauDirec.png)

Na tabela se mostram os atores que tem maior grau e a imagem é uma representação das conexões de diretores.

---

## 4. Centralidade de intermediação (grafo direcionado)

**Pergunta:**  
Quais são os 10 diretores mais influentes perante a métrica de centralidade de intermediação? O que essa métrica representa nesse contexto?

**Resposta:**  

Neste caso, os diretores mais influentes perante a métrica de centralidade de intermediação são os que mais atuaram também como atores, ou que atuaram como atores em filmes com um grande elenco, pois como os diretores são os pontos finais de todos os caminhos do grafo direcionado, as pessoas que atuam apenas como diretores não intermediam nenhum caminho, e quando atuam como intermediário, é porque atuam também como atores. Essa justificativa é perceptível no fato de o maior grau ser atribuído a James Franco, que além de diretor, também é ator, por exemplo, como Harry Osborn em Homem-Aranha (2002)
 
| Rank| Diretor             | $C_{\text{Grau}}^{\text{In}}$ |
| ---- | ------------------- | ----------------------------- |
| 1    | JAMES FRANCO     | 0.00000077                        |
| 2    | JON FAVREAU    | 0.00000063                        |
| 3    | FRANK OZ         | 0.00000047                        |
| 4    | MAHESH MANJREKAR    | 0.00000040                        |
| 5    | ELIZABETH BANKS    | 0.00000039                        |
| 6    | JIM HENSON         | 0.00000037                        |
| 7    | SETH ROGEN    | 0.00000036                        |
| 8    | BRIAN HENSON | 0.00000035                        |
| 9    | RAJAT KAPOOR           | 0.00000031                        |
| 10   | GAUTHAM VASUDEV MENON         | 0.00000031                        |

---

## 5. Centralidade de proximidade (grafo direcionado)

**Pergunta:**  
Quais são os 10 diretores mais influentes perante a métrica de centralidade de proximidade? O que essa métrica representa nesse contexto?

**Resposta:**  
[Inserir texto explicativo]  
[Inserir tabela e gráfico]

---

## 6. Centralidade de grau (grafo não-direcionado)

**Pergunta:**  
Quais são os 10 atores/atrizes mais influentes perante a métrica de centralidade de grau? O que essa métrica representa nesse contexto?

**Resposta:**  
```python
print("Top 10 diretores/atores mais influentes(nao direcionado):")
for node, value in sorted(udg_centrality.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{node} - {value:.4f}")
```
| Rank | Ator       | $C_{\text{Grau}}$ |
| ---- | ----------------- | ----------------- |
| 1    | ANUPAM KHER       | 0.0076            |
| 2    | DANNY TREJO       | 0.0056            |
| 3    | AMITABH BACHCHAN  | 0.0053            |
| 4    | PARESH RAWAL      | 0.0052            |
| 5    | MORGAN FREEMAN    | 0.0051            |
| 6    | JOHN GOODMAN      | 0.0051            |
| 7    | SAMUEL L. JACKSON | 0.0050            |
| 8    | PAUL GIAMATTI     | 0.0048            |
| 9    | FRED ARMISEN      | 0.0047            |
| 10   | SHAH RUKH KHAN    | 0.0047            |

Toda vez que dois atores atuam no mesmo título e é uma participação em conjunto a aresta é gerada.
A centralidade é calculada e normalizada com base nos cálculos apresentados nos slides da semana 14.


Os atores com valores altos, são considerado o centro do grafo, em que se é possível conectar muitos artistas de diferentes segmentos, essa lista revela quem seria o possível "contato" a se ter para conseguir uma possível recomendação em um projeto.

Na tabela se mostram os atores que tem maior grau.


---

## 7. Centralidade de intermediação (grafo não-direcionado)

**Pergunta:**  
Quais são os 10 atores/atrizes mais influentes perante a métrica de centralidade de intermediação? O que essa métrica representa nesse contexto?

**Resposta:**  
Nesse caso, pode-se presumir que quanto maior o grau de intermediação, maior a participação desse ator em filmes de diferentes nichos, pois atuam como intermediários entre vários clusters de diferentes nichos de filmes, maximizando a quantidade de caminhos possíveis em que são intermediários.

| Rank| Ator             | $C_{\text{Grau}}^{\text{In}}$ |
| ---- | ------------------- | ----------------------------- |
| 1    | ANUPAM KHER     | 0.05014588                        |
| 2    | BEN KINGSLEY    | 0.02042305                        |
| 3    | OM PURI         | 0.01714077                        |
| 4    | IKO UWAIS    | 0.01039387                        |
| 5    | PRIYANKA CHOPRA    | 0.01021152                        |
| 6    | MADHAVAN         | 0.01021152                        |
| 7    | DANNY GLOVER    | 0.00984683                        |
| 8    | ALFRED MOLINA | 0.00984683                        |
| 9    | STEVE BLUM           | 0.00948213                        |
| 10   | ERNEST BORGNINE         | 0.00911743                        |

---

## 8. Centralidade de proximidade (grafo não-direcionado)

**Pergunta:**  
Quais são os 10 atores/atrizes mais influentes perante a métrica de centralidade de proximidade? O que essa métrica representa nesse contexto?

**Resposta:**  
[Inserir texto explicativo]  
[Inserir tabela e gráfico]

---

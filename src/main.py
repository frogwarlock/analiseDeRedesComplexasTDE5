import csv
from directed_graph import DirectedGraph
from undirected_graph import UndirectedGraph
import os

def normalize_name(name):
    return name.strip().upper()

def load_data(path):
    data = []
    with open(path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['director'].strip() == '' or row['cast'].strip() == '':
                continue
            directors = [normalize_name(d) for d in row['director'].split(',')]
            actors = [normalize_name(a) for a in row['cast'].split(',')]
            data.append((directors, actors))
    return data

dg = DirectedGraph()
udg = UndirectedGraph()

dataset = load_data('../dados/netflix_amazon_disney_titles.csv')

for directors, actors in dataset:
    for director in directors:
        for actor in actors:
            dg.add_edge(actor, director)

    for i in range(len(actors)):
        for j in range(i + 1, len(actors)):
            udg.add_edge(actors[i], actors[j])

def save_centrality_to_file(centrality, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("Node - Centrality")

        for node, value in sorted(centrality.items(), key=lambda x: x[1], reverse=True):
            #esse for percorre o dicionário e com base no valor de centralidade,
            #os nós são ordenados em descrescente
            file.write(f"\n{node} - {value:.4f}")


udg_centrality = udg.degree_centrality()
dg_centrality = dg.degree_centrality(1) # 1 para indegree, 2 para outdegree, 0 para total degree

print("Directed Graph:")
print("Order:", dg.order)
print("Size:", dg.size)
print("Top 10 diretores mais influentes(direcionado):") #diretores é indg devido as especificações do TDE
for node, value in sorted(dg_centrality.items(), key=lambda x: x[1], reverse=True)[:10]: # o que muda é o [:10] que limita a 10 os resultados
    print(f"{node} - {value:.4f}")
    save_centrality_to_file(dg_centrality, "../resultados/diretores_centralidade_grafo_direcionado.txt")

print()
print("Undirected Graph:")
print("Order:", udg.order)
print("Size:", udg.size)
print("Top 10 diretores/atores mais influentes(nao direcionado):")
for node, value in sorted(udg_centrality.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{node} - {value:.4f}")
    save_centrality_to_file(udg_centrality, "../resultados/diretores_atores_centralidade_grafo_nao_direcionado.txt")
print()

print("Betweenness de Quentin Tarantino: {:.7f}".format(dg.betweenness("QUENTIN TARANTINO")))

print()


def save_mst_to_file(mst_edges, total_cost, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"Custo total da MST: {total_cost}\n")
        file.write("Arestas:\n")
        for u, v, w in mst_edges:
            file.write(f"{u} - {v} (peso {w})\n")

ator = "BOB ODENKIRK"
mst_edges, mst_cost = udg.mst_from_node(ator)

if mst_edges:
    save_mst_to_file(mst_edges, mst_cost, "../resultados/mst_bob_odenkirk.txt")
else:
    print(f"O vértice {ator} não existe no grafo.")


sccs = dg.kosaraju_scc()

with open("../resultados/componentes_fortemente_conexas.txt", "w", encoding="utf-8") as f:
    f.write(f"Quantidade de componentes fortemente conexas: {len(sccs)}\n\n")
    for i, comp in enumerate(sccs, 1):
        f.write(f"Componente {i}: tamanho = {len(comp)}\n")

components = udg.count_connected_components()

with open("../resultados/componentes_conexas.txt", "w", encoding="utf-8") as f:
    f.write(f"Quantidade de componentes conexas: {len(components)}\n\n")
    for i, comp in enumerate(components, 1):
        f.write(f"Componente {i}: tamanho = {len(comp)}\n")

dg.plot_component_size_distribution()

udg.plot_component_size_distribution()

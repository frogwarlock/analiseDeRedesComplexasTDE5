

import csv
from directed_graph import DirectedGraph
from undirected_graph import UndirectedGraph

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

print("Directed Graph:")
print("Order:", dg.order)
print("Size:", dg.size)
print()
print("Undirected Graph:")
print("Order:", udg.order)
print("Size:", udg.size)

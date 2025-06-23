import heapq
import random
import math
from collections import defaultdict
import matplotlib.pyplot as plt

class UndirectedGraph:
    def __init__(self):
        self.order = 0
        self.size = 0
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = [(0, 0)]
            self.order += 1

    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.nodes:
            self.add_node(node1)
        if node2 not in self.nodes:
            self.add_node(node2)

        i1 = self._edge_exists(node1, node2)
        i2 = self._edge_exists(node2, node1)

        if i1 == -1:
            self.nodes[node1].append((node2, weight))
            self.nodes[node2].append((node1, weight))
            self.nodes[node1][0] = (self.nodes[node1][0][0] + 1, self.nodes[node1][0][1] + 1)
            self.nodes[node2][0] = (self.nodes[node2][0][0] + 1, self.nodes[node2][0][1] + 1)
            self.size += 1
        else:
            new_weight = self.nodes[node1][i1][1] + 1
            self.nodes[node1][i1] = (node2, new_weight)
            self.nodes[node2][i2] = (node1, new_weight)

    def _edge_exists(self, source, target):
        if source not in self.nodes:
            return -1
        for i in range(1, len(self.nodes[source])):
            if self.nodes[source][i][0] == target:
                return i
        return -1

    def degree(self, node):
        return self.nodes[node][0][1]

    def degree_centrality(self):
        scale = 1 / (self.order - 1)
        return {node: self.degree(node) * scale for node in self.nodes}

    def degree_distribution(self):
        return [self.degree(node) for node in self.nodes]

    def plot_degree_distribution(self, title="Distribuição de Grau"):
        degrees = self.degree_distribution()
        plt.figure()
        plt.hist(degrees, bins=50, edgecolor='black')
        plt.title(title)
        plt.xlabel("Grau")
        plt.ylabel("Frequência")
        plt.yscale("log")
        plt.grid(True)
        plt.show()

    def count_connected_components(self):
        visited = set()
        components = []

        for node in self.nodes:
            if node not in visited:
                component = []
                self._dfs(node, visited, component)
                components.append(component)

        return components

    def _dfs(self, start, visited, component):
        stack = [start]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                component.append(current)
                for i in range(1, len(self.nodes[current])):
                    neighbor = self.nodes[current][i][0]
                    if neighbor not in visited:
                        stack.append(neighbor)

    def plot_component_size_distribution(self):
        components = self.count_connected_components()
        sizes = [len(c) for c in components]
        plt.figure()
        plt.hist(sizes, bins=50, edgecolor='black')
        plt.title("Distribuição do Tamanho das Componentes Conexas")
        plt.xlabel("Tamanho da componente")
        plt.ylabel("Frequência")
        plt.yscale("log")
        plt.grid(True)
        plt.show()


    def degree_distribution(self):
        return [self.nodes[v][0][0] for v in self.nodes]

    def betweenness(self, u):
        cb = 0
        for s in self.nodes:
            if s != u:
                stack = []
                P = defaultdict(list)
                sigma = defaultdict(int)
                sigma[s] = 1
                d = defaultdict(lambda: float('inf'))
                d[s] = 0
                heap = [(0, s)]

                while heap:
                    d_v, v = heapq.heappop(heap)
                    if d[v] >= d_v:
                        stack.append(v)
                        for w, weight in self.nodes[v][1:]:
                            new_weight = d[v] + weight
                            if d[w] > new_weight:
                                d[w] = new_weight
                                sigma[w] = sigma[v]
                                P[w] = [v]
                                heapq.heappush(heap, (new_weight, w))
                            elif d[w] == new_weight:
                                sigma[w] += sigma[v]
                                P[w].append(v)

                delta = defaultdict(float)

                while stack:
                    w = stack.pop()
                    for v in P[w]:
                        if sigma[w] != 0:
                            coeff = (sigma[v] / sigma[w]) * (1 + delta[w])
                            delta[v] += coeff
                    if w != s and w == u:
                        cb += delta[w] / 2

        return cb / ((self.order - 1) * (self.order - 2) / 2)

    def mst_from_node(self, start):
        if start not in self.nodes:
            return None, 0

        visited = set()
        mst_edges = []
        total_cost = 0

        heap = []
        visited.add(start)
        for neighbor, weight in self.nodes[start][1:]:
            heapq.heappush(heap, (weight, start, neighbor))

        while heap:
            weight, u, v = heapq.heappop(heap)
            if v not in visited:
                visited.add(v)
                mst_edges.append((u, v, weight))
                total_cost += weight
                for neighbor, w in self.nodes[v][1:]:
                    if neighbor not in visited:
                        heapq.heappush(heap, (w, v, neighbor))

        return mst_edges, total_cost

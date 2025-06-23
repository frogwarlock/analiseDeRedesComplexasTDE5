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
    
    def _dijkstra(self, source, early_stop_sum=None):
        infinito = float('inf')
        dist = {v: infinito for v in self.nodes}
        dist[source] = 0
        heap = [(0, source)]
        settled_sum = 0.0

        while heap:
            d_u, u = heapq.heappop(heap)
            if d_u > dist[u]:
                continue
            settled_sum += d_u
            if early_stop_sum is not None and settled_sum > early_stop_sum:
                return None
            for nbr, w in self.nodes[u][1:]:
                nd = d_u + w
                if nd < dist[nbr]:
                    dist[nbr] = nd
                    heapq.heappush(heap, (nd, nbr))
        return dist

    def topk_closeness(self, k):
        heap = []
        worst = 0.0
        for node in self.nodes:
            early = None
            if len(heap) == k and worst > 0:
                early = (self.order - 1) ** 2 / ((self.order - 1) * worst)
            dist = self._dijkstra(node, early)
            if dist is None:
                continue
            reachable = [d for v, d in dist.items() if v != node and d < float('inf')]
            R = len(reachable)
            centrality = 0.0
            if R > 0:
                total = sum(reachable)
                if total > 0:
                    centrality = (R / (self.order - 1)) * (R / total)
            if len(heap) < k:
                heapq.heappush(heap, (centrality, node))
            elif centrality > heap[0][0]:
                heapq.heapreplace(heap, (centrality, node))
            if len(heap) == k:
                worst = heap[0][0]
        return sorted([(n, c) for c, n in heap], key=lambda x: x[1], reverse=True)


    def closeness(self, u):

        if u not in self.nodes:
            raise KeyError(f"Vértice {u} não existe")

        distancias = self._dijkstra(u)

        lista_alcancaveis = []
        for vertice, d in distancias.items():
            if vertice != u and d < float('inf'):
                lista_alcancaveis.append(d)

        R = len(lista_alcancaveis)
        if R == 0:
            return 0.0

        soma_distancias = 0.0
        for d in lista_alcancaveis:
            soma_distancias += d

        if soma_distancias == 0:
            return 0.0

        fator1 = R / (self.order - 1)
        fator2 = R / soma_distancias
        centralidade = fator1 * fator2

        return centralidade

    def count_connected_components(self):
        visited = set()
        count = 0
        for v in self.nodes:
            if v not in visited:
                self._dfs(v, visited)
                count += 1
        return count
        

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

    def dijkstra(self, start):
        distances = defaultdict(lambda: float('inf'))
        distances[start] = 0

        heap = [(0, start)]

        while heap:
            current_distance, current_node = heapq.heappop(heap)

            if current_distance <= distances[current_node]:
                for neighbor, weight in self.nodes[current_node][1:]:
                    distance = current_distance + weight

                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        heapq.heappush(heap, (distance, neighbor))

        return distances
    
    def diameter_approx(self):
        result = 0

        while result <= 2:
            v = random.choice(list(self.nodes.keys()))
            distances = list(self.dijkstra(v).values())
            d1 = max(distances)
            distances.remove(d1)
            d2 = max(distances)
            result = d1 + d2

        return result

    def dijkstra_brandes(self, source):
        dist = defaultdict(lambda: float('inf'))
        dist[source] = 0

        sigma = defaultdict(int)
        sigma[source] = 1

        pred = defaultdict(list)
        
        heap = [(0, source)]

        while heap:
            d, u = heapq.heappop(heap)

            if d <= dist[u]:
                for v, weight in self.nodes[u][1:]:
                    alt = dist[u] + weight

                    if alt < dist[v]:
                        dist[v] = alt
                        sigma[v] = sigma[u]
                        pred[v] = [u]
                        heapq.heappush(heap, (alt, v))
                    elif alt == dist[v]:
                        sigma[v] += sigma[u]
                        pred[v].append(u)

        return dist, sigma, pred
    
    def sample_shortest_path(self, pred, sigma, u, v, b, R):
        t = v

        while t != u:
            predecessors = pred[t]
            sigmas = [sigma[p] for p in predecessors]
            total = sum(sigmas)
            r = random.uniform(0, total)
            acc = 0

            for i in range(len(predecessors)):
                acc += sigmas[i]
                if r <= acc:
                    t = predecessors[i]
                    if t != u:
                        b[t] += 1 / R
                    break
        
        return b
    
    def estimate_all_betweenness(self, R):
        V = list(self.nodes.keys())
        b = defaultdict(float)

        for _ in range(R):
            u, v = random.sample(V, 2)
            _, sigma, pred = self.dijkstra_brandes(u)

            if sigma[v] != 0:
                b = self.sample_shortest_path(pred, sigma, u, v, b, R)

        return b
    
    def estimate_top_k_betweenness(self, K, epsilon=0.1, delta=0.1, c=0.5, c_prime=0.5):
        VD = self.diameter_approx()

        delta1 = 1 - math.sqrt(1 - delta)
        r1 = int((c / epsilon**2) * (math.floor(math.log2(VD - 2)) + 1 + math.log(1 / delta1)))
        b1 = self.estimate_all_betweenness(r1)
        top_k_values = sorted(b1.values(), reverse=True)[:K]
        l1 = max(top_k_values[-1] - epsilon, epsilon / 2)

        r2 = int((c_prime / (epsilon**2 * l1)) * ((math.floor(math.log2(VD - 2)) + 1) * math.log(1 / l1) + math.log(1 / delta1)))
        b2 = self.estimate_all_betweenness(r2)

        if "ANUPAM KHER" in b2:
            print("Centralidade de intermediação de Anupam Kher (não-direcionado): {:.8f}".format(b2["ANUPAM KHER"]))

        top_k_values2 = sorted(b2.values(), reverse=True)[:K]
        l2 = top_k_values2[-1] / (1 + epsilon)

        top_k_set = {v: b for v, b in b2.items() if b / (1 - epsilon) >= l2}
        
        top_k_set = [(key, value) for key, value in top_k_set.items()]
        return sorted(top_k_set, key=lambda x: x[1], reverse=True)[:K]

    def __str__(self):
        text = ""
        for key, value in self.nodes.items():
            text += f"{key}: {value}\n"
        
        return text
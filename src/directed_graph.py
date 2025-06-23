import heapq
from collections import defaultdict
import matplotlib.pyplot as plt

class DirectedGraph:
    def __init__(self):
        self.order = 0
        self.size = 0
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = [(0, 0)]
            self.order += 1

    def add_edge(self, source, target, weight=1):
        if source not in self.nodes:
            self.add_node(source)
        if target not in self.nodes:
            self.add_node(target)

        index = self._edge_exists(source, target)

        if index == -1:
            self.nodes[source].append((target, weight))
            self.size += 1
            self.nodes[source][0] = (self.nodes[source][0][0], self.nodes[source][0][1] + 1)
            self.nodes[target][0] = (self.nodes[target][0][0] + 1, self.nodes[target][0][1])
        else:
            new_weight = self.nodes[source][index][1] + 1
            self.nodes[source][index] = (target, new_weight)

    def _edge_exists(self, source, target):
        if source not in self.nodes:
            return -1
        for i in range(1, len(self.nodes[source])):
            if self.nodes[source][i][0] == target:
                return i
        return -1

    def indegree(self, node):
        return self.nodes[node][0][0]

    def outdegree(self, node):
        return self.nodes[node][0][1]

    def degree(self, node):
        return self.indegree(node) + self.outdegree(node)

    
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
            early_stop = None

            if len(heap) == k and worst > 0:
                early_stop = (self.order - 1) ** 2 / ((self.order - 1) * worst)

            dist = self._dijkstra(node, early_stop)

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

        dist = self._dijkstra(u)

        reachable = [d for v, d in dist.items() if v != u and d < float('inf')]
        R = len(reachable)
        if R == 0:
            return 0.0

        total_dist = sum(reachable)
        if total_dist == 0:
            return 0.0

        return (R / (self.order - 1)) * (R / total_dist)

    def degree_centrality(self, type=0):
        scale = 1 / (self.order - 1)

        if type == 1:
            return {node: self.indegree(node) * scale for node in self.nodes}

        if type == 2:
            return {node: self.outdegree(node) * scale for node in self.nodes}

        scale_total = 1 / (2 * (self.order - 1))
        return {node: self.degree(node) * scale_total for node in self.nodes}

    def get_weight(self, source, target):
        index = self._edge_exists(source, target)
        if index != -1:
            return self.nodes[source][index][1]


    def degree_distribution(self):
        return [self.nodes[v][0][0] + self.nodes[v][0][1] for v in self.nodes]

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
                        cb += delta[w]

        return cb / ((self.order - 1) * (self.order - 2))

    def kosaraju_scc(self):
        stack = []
        visited = set()

        def dfs_fill(v):
            visited.add(v)
            for neighbor, _ in self.nodes[v][1:]:
                if neighbor not in visited:
                    dfs_fill(neighbor)
            stack.append(v)

        def dfs_component(v, transposed, component):
            component.append(v)
            visited.add(v)
            for neighbor, _ in transposed[v][1:]:
                if neighbor not in visited:
                    dfs_component(neighbor, transposed, component)

        for node in self.nodes:
            if node not in visited:
                dfs_fill(node)

        transposed = {node: [(0, 0)] for node in self.nodes}
        for u in self.nodes:
            for v, w in self.nodes[u][1:]:
                transposed[v].append((u, w))
                transposed[v][0] = (transposed[v][0][0], transposed[v][0][1] + 1)
                transposed[u][0] = (transposed[u][0][0] + 1, transposed[u][0][1])

        visited.clear()
        components = []

        while stack:
            node = stack.pop()
            if node not in visited:
                component = []
                dfs_component(node, transposed, component)
                components.append(component)

        return components

    def plot_component_size_distribution(self):
        components = self.kosaraju_scc()
        sizes = [len(comp) for comp in components]
        plt.figure()
        plt.hist(sizes, bins=50, edgecolor='black')
        plt.title("Distribuição do Tamanho das Componentes Fortemente Conexas")
        plt.xlabel("Tamanho da componente")
        plt.ylabel("Frequência")
        plt.yscale("log")
        plt.grid(True)
        plt.show()


    def top_K_betweenness(self, K):
        cb = {v: 0.0 for v in self.nodes}

        for s in self.nodes:
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
                            heapq.heappush(heap, (new_weight, w))
                            sigma[w] = sigma[v]
                            P[w] = [v]
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

                if w != s:
                    cb[w] += delta[w]

        heap = []
        return_list = []

        for key, value in cb.items():
            heapq.heappush(heap, (-value, key))

        for _ in range(K):
            t = heapq.heappop(heap)
            return_list.append((-t[0] / ((self.order - 1) * (self.order - 2)), t[1]))

        return return_list

    def __str__(self):
        text = ""
        for key, value in self.nodes.items():
            text += f"{key}: {value[1:]}\n"

        return text
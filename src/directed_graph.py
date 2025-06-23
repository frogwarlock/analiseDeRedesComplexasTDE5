import heapq
from collections import defaultdict

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
    
    def degree_centrality(self, type=0):
        scale = 1 / (self.order - 1)
        
        if type == 1:
            return {node: self.indegree(node) * scale
                    for node in self.nodes}
        
        if type == 2:
            return {node: self.outdegree(node) * scale
                    for node in self.nodes}
            
        scale_total =  1 / (2 * (self.order - 1))
        return {node: self.degree(node) * scale_total
                for node in self.nodes}

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
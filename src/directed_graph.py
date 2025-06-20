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

    def get_weight(self, source, target):
        index = self._edge_exists(source, target)
        if index != -1:
            return self.nodes[source][index][1]

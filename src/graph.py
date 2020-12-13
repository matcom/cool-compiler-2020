from collections import defaultdict

# clase para representar el grafo que se forma con los tipos
# y sus relaciones de herencia
class Graph:
    def __init__(self, vertex):
        self.graph = defaultdict(list)
        self.vertex_id = []
        self.vertex = vertex
        self.visited = []

    def addNewEdge(self, item):
        self.graph[item] = []

    def addEdge(self, begin, end):
        self.graph[begin].append(end)

    def dfs(self, vertex):
        self.vertex_id = list(self.graph.keys())
        self.visited = [False] * len(self.vertex_id)

        self.dfs_util(vertex)
        return self.visited.count(False) == 0

    def dfs_util(self, vertex):
        self.visited[self.vertex_id.index(vertex)] = True

        for x in self.graph[vertex]:
            if not self.visited[self.vertex_id.index(x)]:
                self.dfs_util(x)

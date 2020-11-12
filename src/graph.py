from collections import defaultdict


class Graph:
    def __init__(self, vertex):
        self.graph = defaultdict(list)
        self.vertex_id = []
        self.vertex = vertex

    def addNewEdge(self, item):
        self.graph[item] = []

    def addEdge(self, begin, end):
        self.graph[begin].append(end)

    def dfs(self, vertex):
        self.vertex_id = list(self.graph.keys())
        visited = [False] * len(self.vertex_id)

        self.dfs_util(vertex, visited)
        return visited.count(False) == 0

    def dfs_util(self, vertex, visited):
        visited[self.vertex_id.index(vertex)] = True

        for x in self.graph[vertex]:
            if not visited[self.vertex_id.index(x)]:
                self.dfs_util(x, visited)

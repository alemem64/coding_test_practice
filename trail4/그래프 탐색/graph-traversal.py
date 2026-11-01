import sys
sys.setrecursionlimit(10**6)   # 재귀 깊이 제한 늘리기

n, m = map(int, input().split())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

visited = [False] * (n + 1)

def dfs(v):
    visited[v] = True
    for nxt in graph[v]:
        if not visited[nxt]:
            dfs(nxt)

dfs(1)
print(sum(visited) - 1)   # 방문한 정점 수 - 1번 자신
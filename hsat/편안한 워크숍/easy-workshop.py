N, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

INF = float('inf')

# dp[i][j] = 길이 l짜리 등산로가 (i,j)에서 끝날 때, 인접 높이 차 최댓값의 최솟값
# 길이 1: 어느 칸이든 시작 가능, 차이 없음 → 0
dp = [[0]*N for _ in range(N)]

# 길이 2, 3, ..., K 순서로 한 층씩 계산
for l in range(2, K+1):
    ndp = [[INF]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if dp[i][j] == INF:
                continue
            for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
                ni, nj = i+di, j+dj
                if 0<=ni<N and 0<=nj<N and arr[ni][nj] > arr[i][j]:
                    cand = max(dp[i][j], arr[ni][nj]-arr[i][j])
                    if cand < ndp[ni][nj]:
                        ndp[ni][nj] = cand
    dp = ndp

ans = min(min(row) for row in dp)
print(ans if ans != INF else -1)
n = int(input())
grid = [list(map(int, input().split())) for _ in range(n)]

# Please write your code here.

ans = 0

for si in range(n-2):
    for sj in range(n-2):
        coin = 0
        for di in range(3):
            for dj in range(3):
                ni, nj = si+di, sj+dj
                coin += grid[ni][nj]
        if coin > ans:
            ans = coin

print(ans)
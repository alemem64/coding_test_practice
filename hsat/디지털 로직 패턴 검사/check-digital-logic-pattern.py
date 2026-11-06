S = input().strip()
K, M = map(int, input().split())
n = len(S)

ans = 0
cnt = {}
for i in range(n-K+1):
    p = int(S[i:i+K],2)
    
    cnt[p] = cnt.get(p,0) + 1

    if cnt[p] >= M:
        ans = 1
        break

print(ans)
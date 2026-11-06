S = input().strip()
K, M = map(int, input().split())
n = len(S)

cnt = {}
ans = 0
for i in range(n - K + 1):
    x = int(S[i:i+K], 2)        # ← 이 줄만 바뀜: 패턴을 이진수 숫자로
    cnt[x] = cnt.get(x, 0) + 1
    if cnt[x] >= M:
        ans = 1
        break

print(ans)
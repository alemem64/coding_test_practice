import random

S = input().strip()
K, M = map(int, input().split())
n = len(S)

MOD = (1 << 61) - 1
B = random.randint(10**5, MOD - 1)   # 랜덤 base로 충돌 방지
BK = pow(B, K, MOD)                  # 윈도우에서 빠지는 글자에 곱할 B^K

cnt = {}
h = 0
ans = 0
for i in range(n):
    h = (h * B + int(S[i]) + 1) % MOD              # 새 글자 추가
    if i >= K:
        h = (h - (int(S[i-K]) + 1) * BK) % MOD     # 맨 앞 글자 제거
    if i >= K - 1:                                 # 길이 K 윈도우 완성
        cnt[h] = cnt.get(h, 0) + 1
        if cnt[h] >= M:
            ans = 1
            break

print(ans)
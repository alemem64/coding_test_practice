from collections import deque

def myprint(arr):
    print('#'*20)
    for lst in arr:
        print(*lst,sep=' ')
    print('#'*20)

def select_attacker(k,arr,aarr):
    cand = []
    for ci in range(N):
        for cj in range(M):
            # 죽었으면 건너뛰기
            if arr[ci][cj] <= 0: continue
            cand.append([arr[ci][cj],aarr[ci][cj],ci+cj,cj,(ci,cj)])
    cand.sort(key=lambda x: (x[0],-x[1],-x[2],-x[3]))
    ai,aj = cand[0][4]

    # 공격력 증가
    arr[ai][aj] += N + M

    # 이번 턴에 공격
    aarr[ai][aj] = k

    return ai,aj

def select_target(arr,arrr,si,sj):
    cand = []
    for ci in range(N):
        for cj in range(M):
            # 죽었거나 공격자면 건너뛰기
            if arr[ci][cj] <= 0 or (si,sj) == (ci,cj): continue
            cand.append([arr[ci][cj],aarr[ci][cj],ci+cj,cj,(ci,cj)])
    cand.sort(key=lambda x: (-x[0],x[1],x[2],x[3]))
    return cand[0][4]

def laser(si,sj,ei,ej):
    # 이전 칸 위치
    v = [[0]*M for _ in range(N)]
    v[si][sj] = (si,sj)

    q = deque()
    q.append((si,sj))

    while q:
        ci,cj = q.popleft()

        # 대상 발견시 공격 진행
        if (ci,cj) == (ei,ej):
            # 대상은 공격자만큼 피해
            arr[ei][ej] -= arr[si][sj]
            harr[ei][ej] = 1

            # 경로의 포탑은 공격자 공격력 절반만큼 공격 받음
            while True:
                ci,cj = v[ci][cj]
                if (ci,cj) == (si,sj): break
                arr[ci][cj] -= arr[si][sj] // 2
                harr[ci][cj] = 1

            return True

        # 우하좌상
        for di,dj in ((0,1),(1,0),(0,-1),(-1,0)):
            ni,nj = ci+di,cj+dj

            if ni < 0: ni = N-1 # 격자 위로
            if ni > N-1: ni = 0 # 격자 아래로
            if nj < 0: nj = M-1 # 격자 왼쪽
            if nj > M-1: nj = 0 # 격자 오른쪽

            # 격자내, 미방문, 부서진 포탑 아님
            if 0<=ni<=N-1 and 0<=nj<=M-1 and v[ni][nj] == 0 and arr[ni][nj] >=1:
                v[ni][nj] = (ci,cj)
                q.append((ni,nj))

    # 경로가 없다면 포탄 공격
    return False

def shoot(si,sj,ei,ej):
    # 대상은 공격자만큼 피해
    arr[ei][ej] -= arr[si][sj]
    harr[ei][ej] = 1

    # 주위 8칸에 대해서 피해 절반
    for di,dj in ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)):
        ni,nj = ei+di,ej+dj


        if ni < 0: ni = N-1 # 격자 위로
        if ni > N-1: ni = 0 # 격자 아래로
        if nj < 0: nj = M-1 # 격자 왼쪽
        if nj > M-1: nj = 0 # 격자 오른쪽

        # 공격자는 공격 안 받음
        if (ni,nj) == (si,sj):
            continue
        # print('포탄',ni,nj)

        if 0<=ni<=N-1 and 0<=nj<=M-1:
            arr[ni][nj] -= arr[si][sj] // 2
            harr[ni][nj] = 1
        else: print('범위 초과',ni,nj,ei,ej,di,dj)

def repair():
    # 공격 안 했고 공격 안 받았으면서 살아 있는 포탑 1 증가
    for ci in range(N):
        for cj in range(M):
            if aarr[ci][cj] != k and harr[ci][cj] == 0 and arr[ci][cj] >=1:
                arr[ci][cj] += 1



###########

N,M,K = map(int,input().split())

arr = [list(map(int,input().split())) for _ in range(N)]

# 공격한 turn을 포탑별로 가짐
aarr = [[0]*M for _ in range(N)]

# print('초기')
# myprint(arr)

# K번 반복
for k in range(1,K+1):
    # 공격 받았으면 1 안 받으면 0
    harr = [[0]*M for _ in range(N)]

    # 살아남은 포탑이 1개면 즉시 중지
    survived = []
    for ci in range(N):
        for cj in range(M):
            if arr[ci][cj] >=1:
                survived.append(arr[ci][cj])
    if len(survived) <= 1: break

    # 1. 공격자 선정
    si,sj = select_attacker(k,arr,aarr)

    # 2. 공격 대상 선정
    ei,ej = select_target(arr,aarr,si,sj)

    # 3. 레이저 공격
    attacked = laser(si,sj,ei,ej)
    

    # 4. 포탄 공격
    if not attacked:
        shoot(si,sj,ei,ej)

    # print('공격 이후')
    # myprint(arr)

    # 포탑 정비
    repair()

    # print('정비 이후')
    # print('공격자',si,sj,'대상',ei,ej,'레이저',attacked)
    # myprint(arr)

# myprint(arr)

best = 0
for ci in range(N):
    for cj in range(M):
        if best < arr[ci][cj]:
            best = arr[ci][cj]

print(best)

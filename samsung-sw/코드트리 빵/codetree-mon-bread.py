from collections import deque

def myprint(arr):
    # print('#'*30)
    tarr = [lst[:] for lst in arr]
    for idx in range(1,m+1):
        i,j = plst[idx]
        if 0<=i<=n-1 and 0<=j<=n-1:
            tarr[i][j] = f'({idx})'
    for i in range(n):
        for j in range(n):
            if barr[i][j] == 1:
                tarr[i][j] = f'[{tarr[i][j]}]'
    for lst in tarr:
        print(*lst,sep=' ')
    print('#'*30)

def myprint2(arr):
    for lst in arr:
        print(*lst,sep=' ')
    print('#'*30)


def cal_dist(si,sj,ei,ej):
    v = [[-1]*n for _ in range(n)]
    v[si][sj] = 0
    q = deque()
    q.append((si,sj))

    while q:
        ci,cj = q.popleft()

        # 도착지 도달시 이동횟수 반환
        if (ci,cj) == (ei,ej):
            return v[ci][cj]

        # 상좌우하
        for di,dj in ((-1,0),(0,-1),(0,1),(1,0)):
            ni,nj = ci+di,cj+dj

            # 격자내 미방문 장애물 없다면
            if 0<=ni<=n-1 and 0<=nj<=n-1 and v[ni][nj] == -1 and barr[ni][nj] == 0:
                v[ni][nj] = v[ci][cj] +1
                q.append((ni,nj))
    
    # print(f'{t}번째에서 {si,sj}에서 {ei,ej}로 이동 불가')
    return float('inf')

#####################
n,m = map(int,input().split())

# 편의점 좌표 리스트
clst = [[] for _ in range(m+1)]

# 빈공간 0, 편의점 1,2,3..., 베이스 -1
arr = [list(map(lambda x: -int(x),input().split())) for _ in range(n)]
for idx in range(1,m+1):
    i,j = map(int,input().split())
    arr[i-1][j-1] = idx
    clst[idx] = [i-1,j-1]

# 베이스캠프 리스트
blst = []
for i in range(n):
    for j in range(n):
        if arr[i][j] == -1:
            blst.append((i,j))

# 못 지나가는 공간이면 1 지나갈 수 있으면 0
barr = [[0]*n for _ in range(n)]

# 격자내 사람 위치 n,n이면 격자 밖
plst = [[n,n] for _ in range(m+1)]

# 사람별 도착했으면 1 아니면 0
arrived = [0]*(m+1)

# m명의 사람 위치
# print(plst)

# myprint(arr)
t = 0
while True:
    barrier_q = []

    # 1분씩 시간이 늘어남
    t += 1

    # 1. 격자내 사람들 편의점으로 1칸 이동
    for idx in range(1,m+1):
        si,sj = plst[idx]
        ei,ej = clst[idx]
        
        # 격자 밖 사람과 도착한 사람은 건너뛰기
        if 0<=si<=n-1 and 0<=sj<=n-1 and arrived[idx] == 0:
            cd = cal_dist(si,sj,ei,ej)
            for di,dj in ((-1,0),(0,-1),(0,1),(1,0)):
                ni,nj = si+di,sj+dj 
                if 0<=ni<=n-1 and 0<=nj<=n-1 and barr[ni][nj] == 0:
                    dist = cal_dist(ni,nj,ei,ej)
                    # print(f'{idx} 사람 {si,sj}에서 {ei,ej}로 가기 위해 {ni,nj}로 이동. 방향{di,dj}, 거리{dist},기준거리{cd}')
                    if cd > dist:
                        # print(f'{idx} 사람 {si,sj}에서 {ei,ej}로 가기 위해 {ni,nj}로 이동. 방향{di,dj}, 거리{dist}')
                        break
        else: continue

        # ni,nj로 이동하기
        plst[idx] = [ni,nj]

        # 2. 편의점 도착시 해당 편의점 못 지나감
        if (ni,nj) == (ei,ej):
            arrived[idx] = 1
            # barr[ni][nj] = 1
            barrier_q.append((ni,nj))
    for bi,bj in barrier_q:
        barr[bi][bj] = 1

    # 3. 베이스에 들어가기
    if t <= m:
        # 해당 사람이 가고자 하는 편의점 찾기
        ei,ej = clst[t]

        # 베이스캠프마다 거리 가장 가까운 걸 고르기
        cand = []
        for ci,cj in blst:
            # 베이스가 이동 불가능한 곳이라면 건너뛰기
            if barr[ci][cj] == 1: continue

            dist = cal_dist(ci,cj,ei,ej)
            cand.append((dist,ci,cj))
        cand.sort()

        # if t==4:
        #     print(cand)
            
        si,sj = cand[0][1], cand[0][2]

        # 해당 베이스에 사람 넣고 해당 베이스 못 지나감
        plst[t] = [si,sj]
        barr[si][sj] = 1
        # barrier_q.append((si,sj))

    # # 4. 이동 불가능한 곳을 barr에 업데이트
    # for bi,bj in barrier_q:
    #     barr[bi][bj] = 1

    # print(plst)
    # myprint2(barr)
    # myprint(arr)
    
    # 모두 도착하면
    if arrived.count(1) == m:
        break

print(t)
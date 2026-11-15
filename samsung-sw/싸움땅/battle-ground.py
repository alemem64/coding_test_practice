def myprint(arr):
    for lst in arr:
        print(*lst,sep=' ')
    print('#'*30)

def move_losser(idx,ci,cj):
    # 자기가 가진 총 바닥에 두기.
    garr[ci][cj].append(glst[idx])
    glst[idx] = 0

    # 원래 가던 방향으로 이동. 이동할 칸에 다른 플레이어 또는 격자밖이면 오른쪽 90도 회전, 빈칸 보이는 순간에 이동
    ci,cj = plst[idx]
    di,dj = dirc[dlst[idx]]
    ni,nj = ci+di,cj+dj

    while True:
        if not 0<=ni<=N-1 or not 0<=nj<=N-1 or parr[ni][nj] > 0:
            dlst[idx] = (dlst[idx] + 1) % 4
            di,dj = dirc[dlst[idx]]
            ni,nj = ci+di,cj+dj
        else:
            break
    # 이동
    plst[idx] = [ni,nj]

    # 해당 칸에 총 있으면 가장 센 총 얻고 나머지 바닥에 두기
    if sum(garr[ni][nj]) > 0:
        garr[ni][nj].sort()
        glst[idx] = garr[ni][nj].pop()

def update_parr(plst):
    tarr = [[0]*N for _ in range(N)]
    for idx in range(1,M+1):
        pi,pj = plst[idx]
        tarr[pi][pj] = idx
    parr = tarr
    return parr

###################

N,M,K = map(int,input().split())

tarr = [list(map(int,input().split())) for _ in range(N)]

# 각 칸에 여러개의 총 리스트
garr = [[[]]*N for _ in range(N)]
for i in range(N):
    for j in range(N):
        garr[i][j] = [tarr[i][j]]

# 사람 좌표
plst = [0]*(M+1)

# 사람 번호
parr = [[0]*N for _ in range(N)]

# 상우하좌 방향
dlst = [0]*(M+1)
dirc = ((-1,0),(0,1),(1,0),(0,-1))

# 초기 능력치
slst = [0]*(M+1)

# 사람마다 가지고 있는 총
glst = [0]*(M+1)

# 라운드에서의 점수
alst = [0]*(M+1)

for idx in range(1,M+1):
    i,j,d,s = map(int,input().split())
    plst[idx] = [i-1,j-1]
    dlst[idx] = d
    slst[idx] = s
    parr[i-1][j-1] = idx

# myprint(parr)

# K번의 라운드에 대해서
for k in range(K):

    # 1. 각 플레이어 순으로 향하고 있는 방향으로 한 칸 이동. 격자 밖이면 정반대 방향으로
    for idx in range(1,M+1):
        ci,cj = plst[idx]
        di,dj = dirc[dlst[idx]]
        ni,nj = ci+di,cj+dj
        # 격자밖 반대 이동
        if not 0<=ni<=N-1 or not 0<=nj<=N-1:
            dlst[idx] = (dlst[idx] + 2) % 4
            ni,nj = ci-di,cj-dj
        
        # 이동
        plst[idx] = [ni,nj]


        # 2. 이동했는데 사람이 없으면서 총이 있다면
        if parr[ni][nj] == 0 and sum(garr[ni][nj]) >= 1:
            # 2.1. 바닥 총과 가지고 있는 총 중 더 강한 총 획득, 나머지들 바닥에 두기
            cand = []
            # 총을 가지고 있다면 후보에 추가
            if glst[idx]: cand.append(glst[idx])
            for gun in garr[ni][nj]:
                cand.append(gun)
            cand.sort()

            # 가장 강한 총 획득
            glst[idx] = cand.pop()
            garr[ni][nj] = cand

        # 3. 이동했는데 플레이어가 있으면 싸움
        if parr[ni][nj] > 0:

            # 3.1. 초기능력치, 총공격력 합 -> 초기 능력
            p1s, p1g = slst[idx],glst[idx]
            p2 = parr[ni][nj]
            p2s, p2g = slst[p2], glst[p2]

            cand = []
            cand.append((p1s+p1g,p1s,idx))
            cand.append((p2s+p2g,p2s,p2))
            cand.sort(reverse=True)

            winner = cand[0][2]
            losser = cand[1][2]

            # 3.2. 진사람
            parr = update_parr(plst)
            move_losser(losser,ni,nj)
            

            # 3.3. 이긴 사람
            # 초기 능력+총 공격의 차만큼 점수 얻기
            score = cand[0][0] - cand[1][0]
            alst[winner] += score

            # 떨어진 총과 가지고 있는 총 중 더 센 총 얻고 나머지 바닥에 두기
            cand = []
            for gun in garr[ni][nj]:
                cand.append(gun)
            cand.append(glst[winner])
            cand.sort()
            glst[winner] = cand.pop()
            garr[ni][nj] = cand
    
        # 4. parr 위치 업데이트
        parr = update_parr(plst)

        # if k == 1 and (idx == 3 or idx == 4):
        #     print('승리',winner, '패배',losser)
        #     print('점수',alst)
        #     print('사람',plst)
        #     print('능력',slst)
        #     print('총',glst)
        #     myprint(parr)
        #     myprint(garr)

print(*alst[1:],sep=' ')
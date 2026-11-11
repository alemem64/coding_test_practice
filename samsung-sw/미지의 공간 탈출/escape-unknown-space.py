from collections import deque

# sk3d,si3d,sj3d = find_start_3d(tarr,marr)
def find_start_3d(tarr,marr):
    for i in range(M):
        for j in range(M):
            if tarr[4][i][j] == 2:
                return 4, i, j 

def find_3d_base(marr):
    for i in range(N):
        for j in range(N):
            if marr[i][j] == 3:
                return i, j

# ek3d,ei3d,ej3d,si,sj = find_end_3d_start_2d(tarr,marr)
def find_end_3d_start_2d(tarr,marr):
    bi, bj = find_3d_base(marr)
    for i in range(bi,bi+M):
        for j in range(bj,bj+M):
            if marr[i-1][j] == 0: # 상에서 찾음
                return 3, M-1, (M-1)-(j-bj), i-1,j
            elif marr[i+1][j] == 0: #하에서 찾음
                return 2, M-1, j-bj, i+1,j
            elif marr[i][j-1] == 0: # 좌
                return 1, M-1, i-bi, i,j-1
            elif marr[i][j+1] == 0: # 우
                return 0, M-1, (M-1)-(i-bi),i,j+1

def find_end_2d(marr):
    for i in range(N):
        for j in range(N):
            if marr[i][j] == 4:
                marr[i][j] = 0
                return i,j


# dist = bfs_3d(sk3d,si3d,sj3d,ek3d,ei3d,ej3d)
def bfs_3d(sk,si,sj,ek,ei,ej):
    v = [[[0]*M for _ in range(M)] for _ in range(5)]
    v[sk][si][sj] = 1
    q = deque()
    q.append((sk,si,sj))

    left_nxt   = {0:2,2:1,1:3,3:0}
    right_nxt = {0:3,3:1,1:2,2:0}

    while q:
        ck,ci,cj = q.popleft()

        # 목적지 도착
        if (ck,ci,cj) == (ek,ei,ej):
            return v[ck][ci][cj]

        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            
            ni,nj = ci+di,cj+dj

            if ni<0: # 위로 이동시
                if ck == 4: nk,ni,nj = 3,0,(M-1)-cj
                elif ck == 3: nk,ni,nj = 4,0,(M-1)-cj
                elif ck == 2: nk,ni,nj = 4,M-1,cj
                elif ck == 1: nk,ni,nj = 4,cj,0
                elif ck == 0: nk,ni,nj = 4,(M-1)-cj,M-1
            elif ni>=M: # 아래로 이동시
                if ck == 4: nk,ni,nj = 2,0,cj
                else: continue
            elif nj<0: # 좌로 이동
                if ck == 4: nk,ni,nj = 1,0,ci
                else : nk,ni,nj = left_nxt[ck], ci, (M-1)
            elif nj>=M: # 우로 이동
                if ck == 4: nk,ni,nj = 0,0,(M-1)-ci
                else: nk,ni,nj = right_nxt[ck],ci,0
            else: # 범위 내
                nk = ck
            # 미방문, 장애물 아니라면
            if v[nk][ni][nj] == 0 and tarr[nk][ni][nj] == 0:
                v[nk][ni][nj] = v[ck][ci][cj] + 1
                q.append((nk,ni,nj))
    return -1

def make_error(marr,elst,ei,ej):
    v = [[float('inf')] * N for _ in range(N)]
    
    # 동서남북
    di = [0,0,1,-1]
    dj = [1,-1,0,0]

    for wi,wj,wd,wv in elst:

        # 초기 위치에 1 표시
        v[wi][wj] = 1

        ci,cj = wi,wj

        # 최대 N 칸 이동하면서 배수만큼 칸에 표시
        for mul in range(1,N+1):
            ni,nj = ci+di[wd],cj+dj[wd]

            # ### 범위내, 장애물 x, 탈출구 x, 빈 공간이면 확산
            if 0<=ni<=N-1 and 0<=nj<=N-1 and marr[ni][nj] == 0 and (ni,nj) != (ei,ej):
                if v[ni][nj] > mul * wv:
                    v[ni][nj] = mul * wv
                    ci,cj = ni,nj 

            # 확산 못하면 멈춤
            else: break
    return v

def bfs_2d(dist,v,si,sj,ei,ej):
    v[si][sj] = dist
    q = deque()
    q.append((si,sj))

    while q:
        ci,cj = q.popleft()

        # 도착시
        if (ci,cj) == (ei,ej):
            return v[ci][cj]

        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            # 격자내, v 값보다 작을 때,장애물 x, 
            ni,nj = ci+di, cj+dj
            if 0<=ni<=N-1 and 0<=nj<=N-1 and marr[ni][nj]==0 and v[ni][nj] > v[ci][cj]+1:
                v[ni][nj] = v[ci][cj] + 1
                q.append((ni,nj))

    return -1


#####################

N, M, F = map(int, input().split())
marr = [list(map(int, input().split())) for _ in range(N)]

# 시간의 벽. 0 동, 1 서, 2 남, 3 북, 4 윗
tarr = [[list(map(int,input().split())) for _ in range(M)] for _ in range(5)]

# 이상현상. i, j, d, v
elst = [list(map(int,input().split())) for _ in range(F)]


# 시작위치: tarr[4] 의 2로 표시된 칸
# 종료위치: marr의 4로 표시된 칸
# 시간벽: marr의 3으로 된 칸
# marr, tarr 이어지는 출구는 하나
# 이상현상: v 배수턴 마다 d 방향으로 한 칸 확산. 사라지지 않음
    # 장애물 아니고 탈출구 아닌 빈공간으로만 확산. 확산 불가시 멈춤
    # 모든 이상현상 동시에 독립적 확산
    # 방향 동0, 서1, 남2, 북3
# 이동:
    # 매턴 상하좌우 한 칸
    # 장애물 1, 이상현상 피해서 4까지 도달.
    # 탈출 불가시 -1 출력, 최소 턴수 출력
    # 이상현상 이후 타임머신 이동

# 1. 3d bfs

# 1.1. 3d에서 시작 종료 좌표 찾기

sk3d,si3d,sj3d = find_start_3d(tarr,marr)

ek3d,ei3d,ej3d,si,sj = find_end_3d_start_2d(tarr,marr)

ei,ej = find_end_2d(marr)

# 1.2. 3d에서 bfs하기

dist = bfs_3d(sk3d,si3d,sj3d,ek3d,ei3d,ej3d)

if dist == -1:
    print(dist)
else: # 경로 있다면
    # 2. 시간 이상 현상을 벽으로 표시
    v = make_error(marr,elst,ei,ej)

    # 3. 2d bfs

    dist = bfs_2d(dist,v,si,sj,ei,ej)

    print(dist)
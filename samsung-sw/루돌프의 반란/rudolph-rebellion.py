from collections import deque

def myprint(arr):
    for lst in arr:
        print(*lst,sep=' ')
    print("#"*30)

# 산타 기절, 충돌, 상호작용
def move_santa(m,sn,si,sj,di,dj,mul):

    # 다음 턴에 일어나도록 기절
    wakeup_turn[sn] = m+2

    # 산타 mul만큼 점수 얻기
    score[sn] += mul

    # di,dj로 mul-1만큼 이동
    ni,nj = si+di*(mul-1), sj+dj*(mul-1)
    # 격자 내라면 이동
    if 0<=ni<=N-1 and 0<=nj<=N-1:
        arr[si][sj] = 0
        arr[ni][nj] = sn
        slst[sn] = [ni,nj]
    # 격자 밖이면 탈락
    else:
        alive[sn] = 0
        arr[si][sj] = 0
        return

    # 상호작용
    q = deque()
    q.append(sn)

    while q:

        cn = q.popleft()
        # 꺼낸 산타 1칸 이동
        ci,cj = slst[cn]
        ni,nj = ci+di,cj+dj

        # 격자 내라면 1칸 이동
        if 0<=ni<=N-1 and 0<=nj<=N-1:
            # 다른 산타 번호
            nn = arr[ni][nj]

            # 현재 산타 이동
            arr[ci][cj] = 0
            arr[ni][nj] = cn
            slst[cn] = [ni,nj]

            # 1칸 이동했는데 다른 산타가 있다면 다른 산타를 q에 추가
            if nn >= 1:
                q.append(nn)
        
        # 이동했는데 격자 밖이면 탈락
        else:
            alive[cn] = 0
            arr[ci][cj] = 0

    # 탈락하지 않은 산타 arr 업데이트
    for idx in range(1,P+1):
        if alive[idx] == 1:
            si,sj = slst[idx]
            arr[si][sj] = idx


    return

####################

N,M,P,C,D = map(int,input().split())
arr = [[0]*N for _ in range(N)]

ri,rj = map(lambda x: int(x) -1 ,input().split())
arr[ri][rj] = -1

slst = [[] for _ in range(P+1)]

for idx in range(1,P+1):
    n,i,j = map(int,input().split())
    slst[n] = [i-1,j-1]
    arr[i-1][j-1] = n

# 살아 있으면 1, 탈락했으면 0
alive = [1] * (P+1)

# 깨어날 턴 번호를 산타별로 저장
wakeup_turn = [1] * (P+1)

# 산타별 점수 저장
score = [0] * (P+1)

# print('초기상태')
# myprint(arr)

# M개의 턴에 대해서
for m in range(1,M+1):

    # 모든 산타 탈락시 게임 종료
    if alive.count(0) == P: break

    # 1. 루돌프 움직임

    
    cand = []
    # 가장 가까운 산타 찾기
    for idx in range(1,P+1):
        # 탈락했으면 넘어가기
        if alive[idx] == 0: continue
        
        si,sj = slst[idx]
        
        dist = (ri-si)**2 + (rj-sj)**2
        cand.append([dist,si,sj])
    cand.sort(key=lambda x: (x[0],-x[1],-x[2]))
    # print(cand)

    # 가장 가까운 산타
    _,si,sj = cand[0]

    # 8방향 중 가장 가까워지는 방향 선택
    m_dist = 2*N**2
    m_dir = (0,0)
    # 상우하좌 대각선
    for di,dj in ((-1,0),(0,1),(1,0),(0,-1),(-1,-1),(-1,1),(1,-1),(1,1)):
        ni,nj = ri+di,rj+dj
        dist = (si-ni)**2 + (sj-nj)**2
        if m_dist > dist:
            m_dist = dist
            m_dir = (di,dj)

    # 루돌프 한 칸 돌진
    di,dj = m_dir
    ni,nj = ri+di,rj+dj
    sn = arr[ni][nj]

    # 해당 칸에 산타 있으면 기절,충돌,상호작용
    if arr[ni][nj] >=1:
        move_santa(m,sn,ni,nj,di,dj,C)

    # 루돌프 좌표 갱신
    arr[ri][rj] = 0
    ri+=di
    rj+=dj
    arr[ri][rj] = -1

    # print('루돌프 이동')
    # myprint(arr)
    
    # 2. 산타 움직임
    
    # 순서대로 산타 움직임
    for idx in range(1,P+1):
        # 탈락했거나 기절했으면 건너뛰기
        if alive[idx] == 0 or wakeup_turn[idx] > m: continue
        # print("도달")

        # 기준 거리
        si,sj = slst[idx]
        cdist = (ri-si)**2 + (rj-sj)**2

        m_dist = 2*N**2
        m_dir = [0,0]
        # 상우하좌 방향에 대해서
        for di,dj in ((-1,0),(0,1),(1,0),(0,-1)):
            ni,nj = si+di,sj+dj
            dist = (ri-ni)**2 + (rj-nj)**2
            # print("거리 계산",ni,nj,cdist,dist,arr[ni][nj])
            # 격자내이고 거리가 가까워지고 산타가 없는 칸이면 후보에 추가
            if 0<=ni<=N-1 and 0<=nj<=N-1 and cdist>dist and arr[ni][nj] <= 0:
                if m_dist > dist:
                    m_dist = dist
                    m_dir = [di,dj]
        # 움직일 수 있다면
        if m_dist != 2*N**2:
            di,dj = m_dir
            ni,nj = si+di,sj+dj

            # 산타 좌표 갱신
            arr[si][sj] = 0
            arr[ni][nj] = idx
            slst[idx] = [ni,nj]

            # 이동한 칸에 루돌프 있으면 산타 움직이기
            if (ni,nj) == (ri,rj):
                move_santa(m,idx,ni,nj,-di,-dj,D)
                arr[ni][nj] = -1
    # 살아있으면 점수 1추가
    for idx in range(1,P+1):
        if alive[idx] == 1:
            score[idx] +=1

    # print(m,"턴", wakeup_turn)
    # print(slst)
    # print(alive)
    # print('산타 이동')
    # print(score)
    # myprint(arr)


print(*score[1:],sep=' ')
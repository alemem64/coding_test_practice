from collections import deque

def bfs(hi,hj,pi,pj,rarr):

    v = [[0]*N for _ in range(N)]

    v[hi][hj] = [hi,hj] # 이전 위치 저장

    q = deque()
    q.append([hi,hj])

    while q:
        ci, cj = q.popleft()

        # 공원이면 path 반환
        if (ci,cj) == (pi,pj):
            path = [[pi,pj]]
            while (ci, cj) != (hi, hj):
                ci, cj = v[ci][cj]
                path.append([ci,cj])
            return path[::-1]

        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = ci+di, cj+dj

            # 격자 내, 미방문, 도로이면 이동 가능
            if 0<=ni<=N-1 and 0<=nj<=N-1 and v[ni][nj] == 0 and rarr[ni][nj] == 0:
                v[ni][nj] = [ci,cj]
                q.append([ni,nj])

    # 경로 없으면 종료
    return -1

def make_sight(d1,i,mi,mj):
    # 방향
    sset = set()
    di, dj = d1[i]
    ci, cj = di+mi,dj+mj
    side = 1


    # 격자 밖으로 나갈시 종료
    while 0<=ci<=N-1 and 0<=cj<=N-1:
        # sset에 시야 추가

        # 상하 -> i 고정, j 시작부터 끝까지 추가
        if i == 0 or i == 1:
            for idx in range(cj-side, cj+side+1):
                # 나간 idx는 종료
                if 0<=idx<=N-1: 
                    sset.add((ci, idx))
                else: continue

        # 좌우 -> j 고정, i 시작부터 끝까지 추가
        elif i == 2 or i == 3:
            for idx in range(ci-side,ci+side+1):
                # 나간 idx는 종료
                if 0<=idx<=N-1: 
                    sset.add((idx, cj))
                else: continue

        # 다음 칸으로 이동
        ci, cj = ci+di, cj+dj
        side+=1

    return sset

def hide_sight(sset, wlst, d1, i, mi, mj):
    # 시야 내에 들어온 각 전사들에 대해서
    for w in wlst:
        if (w[0], w[1]) not in sset:
            continue
        di,dj = d1[i]
        ci, cj = w[0]+di, w[1]+dj

        side = 1
        
        # 격자 밖으로 나가면 종료
        while 0<=ci<=N-1 and 0<=cj<=N-1:
            # 상하 -> ci 고정 cj가 mj보다 작으면 cj-side 부터 cj+1까지
                    # cj가 mj보다 크면 cj부터 cj+side+1까지
                    # 같으면 cj만
            if i == 0 or i == 1:
                if cj < mj:
                    for idx in range(cj-side,cj+1):
                        if (ci,idx) in sset:
                            sset.remove((ci,idx))
                elif cj > mj:
                    for idx in range(cj,cj+side+1):
                        if (ci,idx) in sset:
                            sset.remove((ci,idx))
                else:
                    if (ci,cj) in sset:
                        sset.remove((ci,cj))
            
            # 좌우 -> cj고정 ci가 mi보다 작으면 ci-side부터 ci+1까지
                    # ci가 mi보다 크면 ci부터 ci+side+1까지
                    # 같으면 ci만
            else:
                if ci < mi:
                    for idx in range(ci-side,ci+1):
                        if (idx,cj) in sset:
                            sset.remove((idx,cj))
                elif ci > mi:
                    for idx in range(ci,ci+side+1):
                        if (idx,cj) in sset:
                            sset.remove((idx,cj))
                else:
                    if (ci,cj) in sset:
                        sset.remove((ci,cj))


            # 다음 칸으로 이동
            ci, cj = ci+di, cj+dj
            side+=1

    return sset

# def wbfs(si,sj,sset,dir,mi,mj):

    # v = [[0]*N for _ in range(N)]

    # v[si][sj] = [si,sj]

    # q = deque()
    # q.append([si,sj])

    # while q:
    #     ci, cj = q.popleft()
    #     # 메두사 도달 또는 시야 내 도달 시 첫 칸 이동 반환
    #     if (ci,cj) == (mi,mj) or (ci,cj) in sset:
    #         path = [[ci,cj]]
    #         while (ci,cj) != (si,sj):
    #             ci,cj = v[ci][cj]
    #             path.append([ci,cj])
            
    #         path = path[::-1]
    #         print("시작", si,sj, "종료", mi,mj)
    #         print("경로", path)

    #         return path[0]
        
    #     # 네방향, 격자 내, 미방문, 시야 밖이면 이동 가능
    #     for di, dj in dir:
    #         ni, nj = ci+di, cj+dj
    #         if 0<=ni<=N-1 and 0<=nj<=N-1 and v[ni][nj] ==0 and (ni,nj) not in sset:
    #             v[ni][nj] = [ci,cj]
    #             q.append([ni,nj])

def wbfs(si,sj,sset,dir,mi,mj):
    dist = abs(si-mi) + abs(sj-mj)

    # 네 방향, 격자내, 시야 밖, 거리 줄어들면 이동
    for di, dj in dir:
        ni, nj = si+di, sj+dj
        if 0<=ni<=N-1 and 0<=nj<=N-1 and (ni,nj) not in sset and dist > abs(ni-mi) + abs(nj-mj):
            return ni, nj, True
    return si,sj,False
    

######################

N, M = map(int,input().split())
hi, hj, pi, pj = map(int, input().split())
tlst = list(map(int, input().split()))
wlst = [0] * M

# 움직일 수 있으면 m 가 0 없으면 1
# wlst: [[r,c, m], [r,c,m], ...]
for i in range(len(tlst)):
    if i % 2 == 1: continue
    wlst[int(i/2)] = [tlst[i], tlst[i+1], 0]

# 도로 배열
rarr = [list(map(int, input().split())) for _ in range(N)]

# 메두사 초기 위치
mi, mj = hi, hj

# 최단 경로 저장
path = bfs(hi,hj,pi,pj,rarr)

t = 1

# 매턴마다
while True:

    # 모든 전사들 움직임 가능으로 표시
    for w in wlst:
        w[2] = 0

    # 정답: [이동, 돌, 공격]
    ans = [0] * 3

    # 1. 메두사 이동: 도로만을 따라 최단 경로로 집에서 공원까지.
        # 이동 칸에 전사 -> 공격 받고 사라짐
        # 여러 최단 경로시 상하좌우
        # 경로 없으면 -1 출력
        # 도로 0 도로 아니면 1

    # 경로 없을 시 -1 출력 후 종료
    if path == -1:
        print(-1)
        break

    # 공원 도착시 0 출력 후 종료
    if path[t] == [pi, pj]:
        print(0)
        break
    
    mi, mj = path[t]

    # 경로에 전사 있으면 전사 죽음
    tlst = []
    for w in wlst:
        if [mi,mj] != [w[0],w[1]]:
            tlst.append(w)
    wlst = tlst


    # 2. 메두사 시선 상하좌우 중 전사를 가장 많이 볼 수 있는 방향, 상하좌우 우선 순위 중 하나 선택
        # 시야: 왼쪽 대각부터 오른쪽 대각
        # 전사가 직선 방향에 -> 한 줄 가려짐, 대각 방향에 -> 삼각형 모양 퍼지며 가려짐
        # 시야 내 전사는 해당 턴에 움직이지 못하고 다음 턴에 풀림. 같은 칸 전사 모두 돌로

    # 상하좌우
    d1 = ((-1,0), (1,0), (0,-1), (0,1))

    # 좌우상하
    d2 = ((0,-1),(0,1),(-1,0),(1,0))
    

    # 2.1. 상하좌우 반복
    cmax = 0
    cmaxdir = 0
    for i in range(4):

        # 2.2. 시야 set에 기본 시야 추가
        sset = make_sight(d1,i,mi,mj)

        # 2.3. 전사들에 의한 가려진 시야 제거
        sset = hide_sight(sset, wlst, d1, i, mi, mj)

        # 2.4. 시야 set에 in인 전사 수 세고 max 표시
        wc = 0
        for w in wlst:
            if (w[0],w[1]) in sset:
                wc += 1
        if cmax < wc:
            cmax = wc
            cmaxdir = i


    # 2.5. 가장 전사 수 많은 방향 선택
    # 2.6. 해당 시야 내 전사들 m을 1로 표시
    sset = make_sight(d1,cmaxdir,mi,mj)
    sset = hide_sight(sset,wlst,d1,cmaxdir,mi,mj)


    for w in wlst:
        if (w[0],w[1]) in sset:
            w[2] = 1
            # 돌이 된 수
            ans[1] += 1
    
    # 3. 전사 이동: 돌 아닌 전사 이동. 전사 같은 칸 공유 가능
        # 첫 번째 이동: 메두사와 거리 가까운 한 칸. 상하자우 우선 순위
        # 두 번째 이동: 좌우상하 우선순위
        # 격자 바깥 x, 메두사 시야 내 x
        # 메두사 도착시 움직이지 않음
    # print("이동 전", wlst)

    for w in wlst:
        if w[2] == 1: continue # 돌인 전사는 건너뛰기
        # 시작이 메두사 좌표라면 건너뛰기
        if (w[0], w[1]) == (mi,mj): continue
        # print("이동1 전",w[0],w[1])
        w[0], w[1], moved = wbfs(w[0], w[1],sset,d1,mi,mj)
        # print("이동1 후",w[0],w[1])
        if moved: ans[0]+=1

        if (w[0], w[1]) == (mi,mj): continue
        # print("이동2 전",w[0],w[1])
        w[0], w[1], moved = wbfs(w[0], w[1],sset,d2,mi,mj)
        # print("이동2 후",w[0],w[1])
        if moved: ans[0]+=1

    # print("공겨 전",wlst)
    # print("메두사", mi,mj)

    # 4. 전사 공격
        # 메두사 칸에 도달시 전사 공격 이후 전사만 모두 사라짐
    tlst = []
    for w in wlst:
        if (w[0],w[1]) != (mi,mj):
            tlst.append(w)
        else: ans[2] +=1
    wlst = tlst
    # print("공격 후",wlst)


    # 5. 출력
        # 메두사가 공원에 도착시 0 출력 및 종료
        # 모든 전사 이동 거리 합 | 돌이 된 전사 수 | 공격한 전사 수
    print(*ans,sep=" ")

    t +=1

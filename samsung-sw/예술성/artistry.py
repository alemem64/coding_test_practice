from collections import deque

def myprint(arr):
    for lst in arr:
        print(*lst, sep=' ')
    print('#'*30)

def get_group(si,sj):
    v = [[0]*N for _ in range(N)]
    v[si][sj] = 1
    q = deque()
    q.append((si,sj))
    gidx = arr[si][sj]
    gset = set()
    gset.add((si,sj))

    while q:
        ci,cj = q.popleft()

        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj

            # 격자내, 미방문, 같은 번호이면
            if 0<=ni<=N-1 and 0<=nj<=N-1 and v[ni][nj] == 0 and gidx == arr[ni][nj]:
                q.append((ni,nj))
                v[ni][nj] = 1
                gset.add((ni,nj))

    return gset,gidx

def cal_adj(si,sj,sidx,eidx,eset):
    v = [[0]*N for _ in range(N)]
    v[si][sj] = 1
    q = deque()
    q.append((si,sj))

    score = 0

    while q:
        ci,cj = q.popleft()

        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj

            # 격자내, 미방문, 내 번호이면
            if 0<=ni<=N-1 and 0<=nj<=N-1 and v[ni][nj] == 0 and sidx == arr[ni][nj]:
                q.append((ni,nj))
                v[ni][nj] = 1
            # 격자내, 미방문,eidx 번호이면서 해당 그룹에 포함이면 인접 점수 추가
            elif 0<=ni<=N-1 and 0<=nj<=N-1 and v[ni][nj] == 0 and eidx == arr[ni][nj] and (ni,nj) in eset:
                score += 1

    return score

def cal_score():
    # 1. 그룹마다 포함된 set을 만들기
    group = []
    score = 0

    for si in range(N):
        for sj in range(N):
            # 이미 그룹에 포함되면 건너뛰기
            exist = False
            if group:
                for gset,gidx in group:
                    if (si,sj) in gset:
                        exist = True
                        break
            if exist: continue

            # 시작 좌표에서의 그룹 더하기
            group.append(get_group(si,sj))

    # for i in range(len(group)):
    #     print(list(group[i][0])[0])
    # 2. 가능한 조합에 대해서 조화로움 계산하기
    for i in range(len(group)-1):
        for j in range(i+1,len(group)):

            n_adj = 0
            for ci,cj in group[i][0]:
                for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                    ni,nj = ci+di, cj+dj
                    if (ni,nj) in group[j][0]:
                        n_adj += 1
            




            # if i == j: continue
            # si,sj = list(group[i][0])[0]
            sidx = group[i][1]
            eidx = group[j][1]

            # # 시작 위치에서 시작해 맞닿은 변 수 계산
            # n_adj = cal_adj(si,sj,sidx,eidx,group[j][0])
            # if cal_adj == 0: continue

            point = (len(group[i][0])+len(group[j][0]))*sidx*eidx*n_adj
            # # print(point,sidx,eidx)

            score += point

    return score

def rotate():
    tarr = [lst[:] for lst in arr]
    # 십자가 반시계 90도
    si = sj = (N-1) // 2

    for idx in range(N):
        tarr[idx][sj] = arr[sj][N-1-idx]
        tarr[si][idx] = arr[idx][si]

    # 나머지 구역 시계 90도 회전
    for ci,cj in ((0,0),(si+1,0),(0,si+1),(si+1,si+1)):
        for i in range(si):
            for j in range(si):
                tarr[ci+i][cj+j] = arr[ci+si-1-j][cj+i]

    
    return tarr


###########

N = int(input())
arr = [list(map(int,input().split())) for _ in range(N)]

ans = 0

# 1. 초기 예술 점수 구하기

ans += cal_score()

# 2. 한 번 회전
for _ in range(3):
    arr = rotate()
    ans += cal_score()

print(ans)
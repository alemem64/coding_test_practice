from collections import deque

def arr_input(q):
    sj,si,ej,ei = map(int, input().split())
    for i in range(si,ei):
        for j in range(sj,ej):
            arr[i][j] = q
            
def bfs(v, si, sj):
    
    q = deque()
    q.append([si,sj])
    sn = arr[si][sj]
    v[si][sj] = sn                     ### 방문 표시
    rlst = []
    rlst.append(sn)
    rlst.append([si,sj])           ### 시작 칸 안 넣음
            
    while q:
        ci, cj = q.popleft()
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = ci+di, cj+dj
            # 영역내, 같은 미생물, 미방문
            if 0<=ni<N and 0<=nj<N and arr[ni][nj] == sn and v[ni][nj] ==0:
                q.append([ni,nj])
                v[ni][nj] = sn
                rlst.append([ni,nj])
    return rlst
                    
            
def group():
    v = [[0]*N for _ in range(N)]
    glst = []
    for si in range(N):
        for sj in range(N):
            if arr[si][sj] > 0 and v[si][sj] ==0:
                tlst = bfs(v,si,sj)
                glst.append(tlst)
    return glst

def del_sort(glst):
    del_set = set()
    for i in range(len(glst) -1):
        for j in range(i+1, len(glst)):
            if glst[i][0] == glst[j][0]:
                del_set.add(i)
                del_set.add(j)
    
    # 지우는 건 뒤부터
    for i in range(len(glst)-1,-1,-1):          ### glst에서 돌며 지울 항목은 pop
        if i in del_set:
            glst.pop(i)
                
    glst.sort(key= lambda x: (-len(x), x[0]))
    
    # 상대 좌표 0,0 기준으로 옮기기: 좌표에서 최소 si, sj를 찾고 모든 좌표에서 si, sj 빼기
    for lst in glst:
        si, sj = N, N
        for ci, cj in lst[1:]:
            si = min(si, ci)
            sj = min(sj,cj)
            
        for idx in range(1, len(lst)) :
            lst[idx][0] -= si
            lst[idx][1] -=sj
    return glst

def check(narr, lst):
    for sj in range(N):
        for si in range(N):
            # 경계 벗어나지 않음, 다른 미생물과 겹치지 않음 -> 가능한 시작 좌표
            for ci, cj in lst:
                ni, nj = si+ci, sj+cj
                if ni>=N or nj>=N or narr[ni][nj] != 0:
                    break
            else: return si, sj                     ### for에 붙은 else: break 없이 종료될 경우 실행. 안 되는 조건 단 하나라도 없다면 실행
    return (-1,-1)
    
def move(glst):
    narr = [[0]*N for _ in range(N)]
    
    for lst in glst:
        sn = lst[0]
        # 옮길 수 있는 기준 위치, (-1,-1) 이면 둘 수 없음
        si, sj = check(narr, lst[1:])
        if (si, sj) != (-1,-1):
            for ci, cj in lst[1:]:
                narr[si+ci][sj+cj] = sn
    return narr

def bfs_adj(v,si,sj):
    # 자기 영역 개수 return
    
    q = deque()
    q.append([si,sj])
    v[si][sj] = 1
    cnt = 1
    
    while q:
        ci, cj = q.popleft()
        # 네 방향, 범위내, ### 미방문 같은 미생물
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = ci+di, cj+dj
            if 0<=ni<N and 0<=nj<N and v[ni][nj] == 0 and arr[si][sj] == arr[ni][nj]:
                q.append([ni,nj])
                v[ni][nj] = 1
                cnt +=1
    return cnt
                
    
def bfs_score(v,si,sj,arr):
    mycnt = 1
    cnts = []
    v[si][sj] = 1
    q = deque()
    q.append([si, sj])
    w = [[0]*N for _ in range(N)]
    
    while q:
        ci, cj = q.popleft()
        # 네 방향, 범위내, 미방문, 같은 미생물이면 mycnt+=1, 다른 미생물이면 따로 bfs
        for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di, cj+dj
            if 0<=ni<N and 0<=nj<N and v[ni][nj] == 0:
                if arr[si][sj] == arr[ni][nj]:
                    q.append([ni, nj])
                    v[ni][nj] = 1
                    mycnt +=1
                elif arr[ni][nj] > 0 and w[ni][nj] == 0: # 다른 미생물이면 cnt 구하기 ### 미방문 w
                    tcnt = bfs_adj(w,ni,nj)
                    cnts.append(tcnt)

    score = 0
    for cnt in cnts:
        score += mycnt*cnt
    return score

def score(arr):
    ans = 0
    v = [[0]*N for _ in range(N)]

    for si in range(N):
        for sj in range(N):
            # 미방문, 미생물일 때 bfs, 두 영역 넓이 구하기
            if v[si][sj] == 0 and arr[si][sj] > 0:
                t = bfs_score(v, si, sj, arr)
                ans += t

    return ans
##################

N, Q = map(int, input().split())

arr = [ [0]*N for _ in range(N)]


for q in range(1, Q+1):
    # 1. 미생물 투입
    arr_input(q)
    # print(arr)
    
    # 2. 미생물 그룹화
    glst = group()
    # print(glst)
    
    # 3. 영역 쪼개지면 없애기, 영역 큰 순, 먼저 투입된 순 정렬, 0,0 상대 좌표로 변환
    glst = del_sort(glst)
    
    # 4. 새 용기에 옮기기
    arr = move(glst)
    # for row in (reversed(arr)):
    #    print(*row)
    
    # 5. 점수 계산
    ans = score(arr)
    
    print(ans)
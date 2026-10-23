from collections import deque

def bfs(v,si,sj):
    q = deque()
    q.append([si,sj])
    v[si][sj] = 1
    rlst = []
    rlst.append(food[si][sj].copy())
    rlst.append([si,sj,power[si][sj]])
    while q:
        ci, cj = q.popleft()
        # 네방향, 범위내, 미방문, 같은 음식: 같은 그룹
        for di, dj in ((-1,0), (1,0), (0,-1),(0,1)):
            ni,nj = ci+di, cj+dj
            if 1<= ni <=N and 1<=nj<=N and v[ni][nj] ==0 and food[si][sj] == food[ni][nj]:
                q.append([ni,nj])
                v[ni][nj] = 1
                rlst.append([ni,nj,power[ni][nj]])
    return rlst


def group():
    glst = []
    v = [[0] * (N+1) for _ in range(N+1)]
    for si in range(1, N+1):
        for sj in range(1, N+1):
            # 미방문이면
            if v[si][sj] == 0:
                rlst = bfs(v,si,sj)
                glst.append(rlst)

    return glst

def move(lst, v):
    # 전파자 위치, 신앙심, 음식
    si, sj, p = lst[1]
    ni, nj = si, sj
    menu = lst[0]

    # 간절함 계산
    if v[si][sj] == 1:         ### 방어 상태가 되어 전파를 안 하면 신앙심 바뀌면 안 됨
        return

    # 전파자는 신앙심을 1로 남김
    lst[1][2] = 1
    power[lst[1][0]][lst[1][1]] = 1
    x = p - 1

    # 전파 방향
    dir = ((-1,0),(1,0),(0,-1),(0,1))
    di, dj = dir[p % 4]

    while True:
        ni, nj = ni+di, nj+dj

        # 격자 밖이거나 간절함 0이거나 전파 받은 대표자이면 전파 종료
        if ni > N or ni < 1 or nj > N or nj < 1 or x <= 0: break

        # 음식이 같다면 전파 안 하고 다음 칸으로 진행
        if food[si][sj] == food[ni][nj]: continue

        # 다른 경우에 전파 진행
        else:
            v[ni][nj] = 1

            y = power[ni][nj]

            # 강한 전파
            if x > y:
                food[ni][nj] = food[si][sj].copy()  ### .copy() 를 안 하면 set 을 공유하게 됨
                x -= y+1
                power[ni][nj] +=1

            # 약한 전파
            else:
                food[ni][nj].update(menu)        ### set에 set 추가시 add가 아닌 update 또는 |= 합집합 할당
                power[ni][nj] += x
                x = 0

#####################

N, T = map(int, input().split())


tfood = []

for i in range(N):
    tfood.append(input().split())

food = [[0]*(N+1) for _ in range(N+1)]


for i in range(N):
    for j in range(N):
        menu = tfood[i][0][j]
        food[i+1][j+1] = set(menu)

power = [[0] * (N+1)]
for i in range(N):
    power.append([0] + list(map(int,input().split())))



for t in range(T):
    ans = [0] * 7  ### 매일 답을 초기화 해야함 밖에 있으면 누적 됐음
    
    # 1. 아침시간
    # 1.1. 모든 신앙심 +=1
    for i in range(1,N+1):
        for j in range(1,N+1):
            power[i][j] = power[i][j] + 1

    # 2. 점심 시간
    # 2.1. 인접한 신봉자끼리 그룹 형성
    # glst = [[{menu}, [i,j,p],...]]
    glst = group()
    # print(glst)

    # 2.2. 그룹내 power, i, j 순으로 큰 사람 대표로 sort
    for lst in glst:
        lst[1:] = sorted(lst[1:], key=lambda x: (-x[2], x[0], x[1])) ### sort 는 return 안 함. sorted로 해야함
        
        # 2.3. 대표자 power += 그룹원 -1, 그룹원 -= 1
        lst[1][2] += len(lst[2:])
        power[lst[1][0]][lst[1][1]] += len(lst[2:])

        for member in lst[2:]:
            power[member[0]][member[1]] -= 1
            member[2] -= 1
    # print(power)

    # 3. 저녁 시간

    # 3.1. 단일, 이중, 삼중 조합 순 정렬
    # comlst[조합개수][glst][lst][음식,[i,j,power]]
    comlst = [[],[],[],[]]

    for lst in glst:
        comlst[len(lst[0])].append(lst)
    # print(comlst)

    # 3.2. 각 조합 내 대표자 power 큰 순, i, j 작은 순 정렬
    for glst in comlst[1:]:
        if glst:
            glst.sort(key = lambda x: (-x[1][2], x[1][0],x[1][1]))
    # print(power)

    # 3.3. 모든 그룹의 전파 시작
    v = [[0]*(N+1) for _ in range(N+1)]
    for glst in comlst[1:]:
        if glst:
            for lst in glst:
                # print(power)
                move(lst, v)

    # print(food)
    # print(power)


    # 4. 각 음식 순서대로 신앙심 총합 출력
    for i in range(1,N+1):
        for j in range(1,N+1):
            if food[i][j] == {'T', 'C', 'M'}:
                ans[0] += power[i][j]
            elif food[i][j] == {'T', 'C'}:
                ans[1] += power[i][j]
            elif food[i][j] == {'T', 'M'}:
                ans[2] += power[i][j]
            elif food[i][j] == {'M', 'C'}:
                ans[3] += power[i][j]
            elif food[i][j] == {'M'}:
                ans[4] += power[i][j]
            elif food[i][j] == {'C'}:
                ans[5] += power[i][j]
            elif food[i][j] == {'T'}:
                ans[6] += power[i][j]
    print(*ans)


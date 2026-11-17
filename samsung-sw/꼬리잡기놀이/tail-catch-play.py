from collections import deque

def myprint(arr):
    for lst in arr:
        print(*lst,sep=' ')
    print('#'*30)

def move():
    # 꼬리 찾기
    tail = []
    for i in range(N):
        for j in range(N):
            if arr[i][j] == 3:
                tail.append((i,j))

    # 각 팀에 대해서
    while tail:
        si,sj = tail.pop()

        # 이전 위치 기록
        v = [[0]*N for _ in range(N)]
        v[si][sj] = (si,sj)

        q = deque()
        q.append((si,sj))

        # 이동 경로
        route = []

        while q:
            ci,cj = q.popleft()

            # 상하좌우
            for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                ni,nj = ci+di,cj+dj

                # 격자내, 미방문, 2라면 가기
                if 0<=ni<=N-1 and 0<=nj<=N-1 and v[ni][nj] == 0 and arr[ni][nj] ==2:
                    v[ni][nj] = (ci,cj)
                    q.append((ni,nj))

        while True:
            if arr[ci][cj] == 3: break
            route.append((ci,cj))
            ci,cj = v[ci][cj]
        
        # 처음이 꼬리 마지막이 머리
        route = route[::-1]

        # 마지막 2에서 1 찾기
        ci,cj = route[-1]
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di,cj+dj

            # 격자내, 1이라면
            if 0<=ni<=N-1 and 0<=nj<=N-1 and arr[ni][nj] ==1:
                route.append((ni,nj))
        
        # 마지막 1에서 4 또는 3 찾기
        ci,cj = route[-1]
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di,cj+dj

            # 격자내, 4 또는 3이라면
            if 0<=ni<=N-1 and 0<=nj<=N-1 and 3 <= arr[ni][nj] <= 4:
                route.append((ni,nj))

        arr[si][sj] = 4

        # 옮기기
        hi,hj = route.pop()
        ti,tj = route.pop(0)
        arr[hi][hj] = 1
        arr[ti][tj] = 3
        # print('머리', hi,hj)
        for mi,mj in route:
            arr[mi][mj] = 2


def ball(k):

    # 우상좌하
    dirc = ((k-1) // N) % 4
    dlst = ((0,1),(-1,0),(0,-1),(1,0))

    # 행렬 날리는 위치
    idx = (k-1) % N

    # 시작 위치 찾기
    if dirc == 0:
        ci,cj = idx,0
    elif dirc == 1:
        ci,cj = N-1,idx
    elif dirc == 2:
        ci,cj = N-1 - idx,N-1
    elif dirc == 3:
        ci,cj = 0,N-1 - idx

    while True:
        # 격자 밖이면 멈추기
        if not 0<=ci<=N-1 or not 0<=cj<=N-1:
            return (-1,-1)

        # 123 이라면 return
        if 1<= arr[ci][cj] <= 3:
            return (ci,cj)

        # 아니라면 다음칸 이동
        di,dj = dlst[dirc]
        ci,cj = ci+di,cj+dj

def cal_score(si,sj):

    # 이동한 길이를 저장
    v = [[0]*N for _ in range(N)]
    v[si][sj] = 1

    q = deque()
    q.append((si,sj))

    while q:

        ci,cj = q.popleft()

        # 1을 만나면 길이 가져오기
        if arr[ci][cj] == 1:
            order = v[ci][cj]
            return order ** 2

        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di,cj+dj

            # 격자내, 미방문, 다음칸이 2이거나 내가 2이면서 다음이 1이면 가기
            if 0<=ni<=N-1 and 0<=nj<=N-1 and v[ni][nj] == 0 and (arr[ni][nj] == 2 or (arr[ci][cj] == 2 and arr[ni][nj] == 1)):
                v[ni][nj] = v[ci][cj] + 1
                q.append((ni,nj))



def change(si,sj):
    # 방문 표시
    v = [[0]*N for _ in range(N)]
    v[si][sj] = 1

    q = deque()
    q.append((si,sj))

    while q:

        ci,cj = q.popleft()

        # 머리와 꼬리 위치 저장
        if arr[ci][cj] == 1:
            hi,hj = (ci,cj)
        elif arr[ci][cj] == 3:
            ti,tj = (ci,cj)

        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di,cj+dj

            # 격자내, 미방문, 123이라면 가기
            if 0<=ni<=N-1 and 0<=nj<=N-1 and v[ni][nj] == 0 and 1<= arr[ni][nj] <=3:
                v[ni][nj] = v[ci][cj] + 1
                q.append((ni,nj))
    
    # 바꾸기
    arr[hi][hj] = 3
    arr[ti][tj] = 1


    
#############

N,M,K = map(int,input().split())

arr = [list(map(int,input().split())) for _ in range(N)]

ans = 0

# K 라운드에 대해
for k in range(1,K+1):

    # 팀별로 머리사람 따라 한 칸 이동
    move()

    # 공 던져서 맞은 사람 찾기
    si,sj = ball(k)

    # 공을 맞았다면 점수 추가
    if (si,sj) != (-1,-1):
        score = cal_score(si,sj)
        ans += score

        # 공 맞은 팀은 순서 바꾸기
        # print('맞음',si,sj)
        change(si,sj)

    # myprint(arr)
print(ans)  

from collections import deque

def myprint(arr):
    print("#"*30)
    for lst in arr:
        print(*lst, sep='\t')

def bfs(arr,earr,si,sj,k):

    v = [[0]*(C+1) for _ in range(R+3)]
    v[si][sj] = 1

    rset = set()

    q = deque()
    q.append((si,sj))

    while q:
        ci, cj = q.popleft()

        for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):

            ni,nj = ci+di, cj+dj

            # 격자내, 미방문,                                     같은 골렘 내이거나                  현재가 출구이면서 다음이 골렘이면
            if (3<=ni<=R+2 and 1<=nj<=C and v[ni][nj] == 0) and (arr[ni][nj] == arr[ci][cj] or (earr[ci][cj]>0 and arr[ni][nj] > 0)):
                v[ni][nj] = 1
                q.append((ni,nj))
                rset.add(ni)
    # if k == 5:
    #     myprint(arr)
    #     myprint(earr)
    #     myprint(v)


    # 방문한 가장 아래 행 return
    return max(rset) -2


#############

R, C, K = map(int,input().split())
glst = [list(map(int,input().split())) for _ in range(K)]

# -1 빈공간, k 골렘
arr = [[-1]*(C+1) for _ in range(R+3)]
earr = [[-1]*(C+1) for _ in range(R+3)]

dwest = {0:3,1:0,2:1,3:2}
deast = {0:1,1:2,2:3,3:0}
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

ans = 0

# K마리의 골렘에 대해서
for k in range(K):

    # 초기 골렘 중앙 위치
    # cd: 0123 북 동 남 서
    ci, cj, cd = 1, glst[k][0], glst[k][1]

    while True:
        # 아래칸이 바닥이면 멈추기
        if ci+1 >= R+2: break

        # 1. 남쪽으로 한 칸 내려가기
        # 아래가 바닥이 아니면서 아래 빈 공간이면 한 칸 아래로 이동
        elif arr[ci+2][cj] == -1 and arr[ci+1][cj-1] == -1 and arr[ci+1][cj+1] == -1:
            ci +=1
        
        # 2. 남쪽으로 못가면 서쪽 회전 후 내려가기 (출구 반시계)
        # 서쪽이 비어 있으면 회전에서 아래로 이동
        elif cj -1 >= 2 and arr[ci][cj-2] == -1 and arr[ci+1][cj-1] == -1 and arr[ci-1][cj-1] == -1 and arr[ci+2][cj-1] == -1 and arr[ci+1][cj-2] == -1:
                ci +=1
                cj -=1
                cd = dwest[cd]

        # 3. 남쪽 x, 서쪽 x이면 동쪽 회전 후 내려가기 (출구 시계)
        elif cj +1 <= C-1 and arr[ci][cj+2] == -1 and arr[ci+1][cj+1] == -1 and arr[ci-1][cj+1] == -1 and arr[ci+2][cj+1] == -1 and arr[ci+1][cj+2] == -1:
                ci +=1
                cj +=1
                cd = deast[cd]
        
        # 못 내려가면 탍출
        else: break


    # 4. 더 이상 아래로 못 내려갈 때

    # 4.1. 골렘 일부가 숲 밖이면 숲 초기화 후 다음 골렘부터
    if ci <= 3:
        arr = [[-1]*(C+1) for _ in range(R+3)]
        earr = [[-1]*(C+1) for _ in range(R+3)]
        continue

    # 4.2. 골렘 위치 기록
    arr[ci][cj], arr[ci+1][cj], arr[ci-1][cj], arr[ci][cj+1], arr[ci][cj-1] = k+1,k+1,k+1,k+1,k+1
    earr[ci + di[cd]][cj + dj[cd]] = k+1

    # myprint(arr)

    # 4.3. 골렘 내에서 상하좌우 이동
        # 출구가 다른 골렘 인접 시 다른 골렘으로 이동 가능

    rmax = bfs(arr,earr,ci,cj,k)

    # 5. 가장 남쪽 행을 정답에 추가
    # print(rmax)
    ans+=rmax

print(ans)
from collections import deque

def myprint(arr):
    print("#"*30)
    for lst in arr:
        print(*lst,sep='\t')

# 중심 기준 90도 회전
def rotate(r,arr,i,j):
    tarr = [lst[:] for lst in arr]

    di = [-1,-1,-1,0,1,1,1,0]
    dj = [-1,0,1,1,1,0,-1,-1]

    for idx in range(8):
        tarr[i+di[idx]][j+dj[idx]] = arr[i+di[idx-2]][j+dj[idx-2]]
    
    return tarr

# 유물인 좌표들 리스트로 반환
def mark(arr):
    vset = set()
    mlst = []

    # 모든 칸에 대해서 출발지로 설정
    for si in range(5):
        for sj in range(5):
            # 공유 방문 set에 포함시 건너뛰기
            if (si,sj) in vset: continue

            vset.add((si,sj))
            q = deque()
            q.append((si,sj))

            tlst = [(si,sj)]

            while q:
                ci,cj = q.popleft()

                # 네방향, 격자내, 미방문, 같은 번호이면 이동.
                for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                    ni,nj = ci+di, cj+dj

                    if 0<=ni<=4 and 0<=nj<=4 and (ni,nj) not in vset and arr[ni][nj] == arr[ci][cj]:
                        vset.add((ni,nj))

                        # 이동시 방문 리스트에 좌표 추가
                        tlst.append((ni,nj))
                        q.append((ni,nj))


            # bfs 끝났는데 방문 리스트 수가 3개 이상이면 전체 리스트에 추가
            if len(tlst) >=3:
                mlst += tlst
        
    return mlst

# mlst 위치에 wlst 순서대로 갱신
def fill(arr,mlst,wlst):
    # 작은 열 -> 큰 행
    mlst.sort(key=lambda x: (x[1], -x[0]))

    for i,j in mlst:
        arr[i][j] = wlst.pop()

    return arr


#######################

K, M = map(int,input().split())

arr = [list(map(int,input().split())) for _ in range(5)]

wlst = list(map(int,input().split()))
# 뒤에서부터 꺼내기
wlst = wlst[::-1]

ans = []

# K번의 턴 동안 반복
for k in range(K):

    # 1. 탐사 진행
    # 1.1. 회전 중앙 좌표 선정

    # maxcnt = 0
    # maxarr = arr
    # maxmlst = []

    lst = []

    # 1.2. 90도, 180도, 270도 회전
    for r in range(3):
        for j in range(1,4):
            for i in range(1,4):
            
                # 해당 중심에서 90도 만큼 회전한 arr 반환
                tarr = [lst[:] for lst in arr]
                for _ in range(r+1):
                    tarr = rotate(r,tarr,i,j)

                # 유물인 좌표들 리스트 반환
                mlst = mark(tarr)

                cnt = len(mlst)

                # 1.3. 유물 1차 획득 가치 최대화 -> 회전 각도 최소 -> 중심 열 작게 -> 중심 행 작게
                # if maxcnt < cnt:
                #     maxcnt = cnt
                #     maxarr = tarr
                #     maxmlst = mlst
                lst.append((cnt,r,j,i,tarr,mlst))

    lst.sort(key=lambda x: (-x[0],x[1],x[2],x[3]))
    maxcnt = lst[0][0]
    maxarr = lst[0][4]
    maxmlst = lst[0][5]

    # myprint(maxarr)
    # print(maxmlst)
    # print
    
    # 유물 획득 불가시 출력 추가 없이 종료
    if maxcnt == 0: break

    # 2. 유물 획득
    turn_cnt = maxcnt

    # 2.1. 인접 같은 숫자 3개 이상 연결시 그 개수가 유물 가치

    # 2.2. 유물 사라지고 해당 위치에 wlst 순서대로 추가
    

    # maxmlst 위치에 wlst 순서대로 갱신
    arr = fill(maxarr,maxmlst,wlst)

    # 2.3. 유물 연쇄 획득: 더 이상 유물 없을 때까지 반복
    while True:
        mlst = mark(arr)

        if len(mlst) == 0: break
        turn_cnt += len(mlst)

        arr = fill(arr, mlst, wlst)
    
    ans.append(turn_cnt)


# 각 턴 마다 유물 가치 총합 출력
print(*ans, sep=" ")
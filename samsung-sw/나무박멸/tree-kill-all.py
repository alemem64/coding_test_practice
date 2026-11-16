def myprint(arr):
    for lst in arr:
        print(*lst,sep=' ')
    print('#'*30)

def grow():
    for ci in range(N):
        for cj in range(N):
            # 나무에 대해서
            if arr[ci][cj] >= 1:
                cnt = 0
                for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                    ni,nj = ci+di,cj+dj
                    # 격자내, 나무이면 cnt 추가
                    if 0<=ni<=N-1 and 0<=nj<=N-1 and arr[ni][nj] >= 1:
                        cnt += 1
                arr[ci][cj] += cnt

def propagate():
    tarr = [lst[:] for lst in arr]

    for ci in range(N):
        for cj in range(N):
            # 나무에 대해서
            if arr[ci][cj] >= 1:
                # 인접 4개 칸에 대해 번식 가능한 칸을 세기
                can_propagate = 0
                for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                    ni,nj = ci+di,cj+dj
                    # 빈칸이면서 제초제 영향 없는 칸이면 번식 가능
                    if 0<=ni<=N-1 and 0<=nj<=N-1 and arr[ni][nj] == 0 and barr[ni][nj] < m:
                        can_propagate += 1

                # 번식하는 수
                if can_propagate:
                    n_children = arr[ci][cj] // can_propagate

                    for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                        ni,nj = ci+di,cj+dj
                        # 빈칸이면서 제초제 영향 없는 칸이면 번식 가능
                        if 0<=ni<=N-1 and 0<=nj<=N-1 and arr[ni][nj] == 0 and barr[ni][nj] < m:
                            tarr[ni][nj] += n_children
    
    return tarr

def kill(ans):
    # 죽이는 나무수, i,j
    cand = []

    for si in range(N):
        for sj in range(N):
            # 나무에 대해서
            if arr[si][sj] >=1:
                # 자기 자신이 죽음
                n_kill = arr[si][sj]

                # 대각선 방향에 대해서 세기
                for di,dj in ((-1,-1),(-1,1),(1,-1),(1,1)):
                    ci,cj = si+di,sj+dj
                    for k in range(K):
                        
                        # 격자내이고 나무이면 전파
                        if 0<=ci<=N-1 and 0<=cj<=N-1 and arr[ci][cj] >= 1:
                            n_kill += arr[ci][cj]

                            ci,cj = ci+di,cj+dj

                        # 나무가 아니면 전파 종료
                        else: break
                cand.append((n_kill,si,sj))
    
    cand.sort(key=lambda x: (-x[0],x[1],x[2]))

    if cand:
        # 제초제 뿌릴 곳
        si,sj = cand[0][1], cand[0][2]


        # 나무 죽이고 제초제 뿌리기
        ans += arr[si][sj]
        arr[si][sj] = 0
        barr[si][sj] = m + C

        # 대각선 방향 제초제 뿌리기
        for di,dj in ((-1,-1),(-1,1),(1,-1),(1,1)):
            ci,cj = si+di,sj+dj
            for k in range(K):
                
                # 격자내이고 나무이면 전파
                if 0<=ci<=N-1 and 0<=cj<=N-1 and arr[ci][cj] >= 1:
                    ans += arr[ci][cj]
                    arr[ci][cj] = 0
                    barr[ci][cj] = m + C

                    ci,cj = ci+di,cj+dj

                # 나무가 아니면 제초제 뿌리고 전파 종료
                elif 0<=ci<=N-1 and 0<=cj<=N-1 and arr[ci][cj] <= 0:
                    barr[ci][cj] = m + C
                    break

                # 격자 밖이면 종료
                else: break

    return ans




###################

N,M,K,C = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(N)]

# 제초제가 영향 있는 년까지를 기록
barr = [[0]*N for _ in range(N)]

ans = 0

# M년 동안
for m in range(1,M+1):

    # 1. 인접 4개 칸의 나무 수만큼 나무 성장
    grow()

    # 2. 번식
    arr = propagate()

    # 3. 제초제
    ans = kill(ans)


    # myprint(arr)
print(ans)
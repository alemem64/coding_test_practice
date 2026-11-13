def myprint(arr):
    tarr = [lst[:] for lst in arr]
    for i in range(M):
        if elst[i] == 1: continue
        pi,pj = plst[i]
        d = dlst[i]
        tarr[pi][pj] = f'({d})'
    print('#'*30)
    for lst in tarr:
        print(*lst,sep='\t')
    print('#'*30)

def cald(si,sj,ei,ej):
    return abs(si-ei) + abs(sj-ej)





#################3

N,M,K = map(int,input().split())

# 출구, 벽 위치
arr = [list(map(int,input().split())) for _ in range(N)]

# 참가자별 좌표
plst = [list(map(lambda x: int(x) - 1,input().split())) for _ in range(M)]

# 참가자별 이동거리 합
dlst = [0]*M

# 참가자별 탈출했으면 1 아니면 0
elst = [0]*M

# 출구 좌표
ei,ej = map(lambda x: int(x) - 1,input().split())

# 출구는 -1
arr[ei][ej] = -1

# print('초기')
# myprint(arr)


# K초 동안 반복
for _ in range(K):

    # 1. 모든 참가자 동시 이동
    for i in range(M):
        # 탈출한 참가자는 이동 안 함
        if elst[i] == 1: continue

        # 참가자 현재 위치
        ci,cj = plst[i]

        cd = cald(ci,cj,ei,ej)

        # 상하좌우에 대해서
        for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni,nj = ci+di,cj+dj
            nd = cald(ni,nj,ei,ej)

            # 격자내, 벽이 아님, 현재칸보다 거리가 가까우면 이동
            if 0<=ni<=N-1 and 0<=nj<=N-1 and arr[ni][nj] <= 0 and nd < cd:

                # print(f'{i}번째 사람 {ci,cj}에서 {ni,nj}로 이동')

                # 다음칸으로 이동
                plst[i] = [ni,nj]
                dlst[i] += 1

                # 이동했는데 탈출구라면 탈출
                if (ni,nj) == (ei,ej):
                    elst[i] = 1

                # 이동했으면 넘어가기
                break
    # print('사람 이동')
    # myprint(arr)

    # 2. 미로 회전
    aside = 0
    ai = 0
    aj = 0
    found = False

    # 참가자와 출구를 포함하는 가장 작은 정사각형 찾기
    for side in range(2,N+1): # 한 변이 2부터 N까지 늘려보기
        if found: break

        # 정사각형 왼쪽 위가 왼쪽 위부터 오른쪽 아래까지
        for si in range(N+1-side):
            if found: break
            for sj in range(N+1-side):

                # 해당 정사각형에 대해서
                have_e = False
                have_p = False

                for di in range(side):
                    for dj in range(side):
                        ni,nj = si+di,sj+dj
                        # 출구 포함
                        if arr[ni][nj] == -1:
                            have_e = True
                            # print('출구 찾음',side,si,sj)

                        # 사람 포함
                        for idx in range(M):
                            # 탈출한 사람은 건너뛰기
                            if elst[idx] == 1: continue
                            pi,pj = plst[idx]
                            if (pi,pj) == (ni,nj):
                                have_p = True
                                # print('사람 찾음',side,si,sj)

                # 둘 다 있으면
                if have_e and have_p:
                    aside = side
                    ai = si
                    aj = sj
                    found = True
                    break

    
    # 해당 정사각형에 대해 시계방향 90도 회전
    tarr = [lst[:] for lst in arr]
    tplst = plst[:]

    # 바깥변부터 안쪽까지
    oi,oj = ai,aj
    for cside in range(aside,0,-2):
        # 상하좌우 방향에 대해
        ci,cj = 0,0
        for di,dj in ((0,1),(1,0),(0,-1),(-1,0)):
            # 더해주는 횟수
            for d in range(cside-1):

                if (di,dj) == (0,1):
                    ni,nj = cj,cside-1-cj

                elif (di,dj) == (1,0):
                    ni,nj = cside-1-ci,-ci
                elif (di,dj) == (0,-1):
                    ni,nj = -(cside-1-cj),-cj
                else:
                    ni,nj = -ci,cside-1-ci

                # 사람 옮기기
                for idx in range(M):
                    pi,pj = plst[idx]
                    if (oi,oj) == (pi,pj):
                        tplst[idx] = [oi+ni,oj+nj]

                # 회전하고 벽 내구도 깎기
                if arr[oi][oj] == -1:
                    tarr[oi+ni][oj+nj] = -1
                    ei,ej = oi+ni,oj+nj
                else: tarr[oi+ni][oj+nj] = max(0,arr[oi][oj] -1)

                
                ci += di
                cj += dj
                oi += di
                oj += dj
        if cside == 1:
            ni,nj = 0,0

            # 출구이면 출구 업데이트
            if arr[oi][oj] == -1:
                    tarr[oi+ni][oj+nj] = -1
                    ei,ej = oi+ni,oj+nj
            # 아니면 벽 깎기
            else: tarr[oi+ni][oj+nj] = max(0,arr[oi][oj] -1)

            # 사람 회전하기
            for idx in range(M):
                    pi,pj = plst[idx]
                    if (oi,oj) == (pi,pj):
                        tplst[idx] = [oi+ni,oj+nj]
        ci+=1
        cj+=1
        oi+=1
        oj+=1
    
    # 90도 회전
    arr = tarr
    plst = tplst
    
    # print('회전',ai,aj,aside)
    # print(plst)
    # print(dlst)
    # print("출구:",ei,ej)
    # myprint(arr)



    # 모든 참가자 탈출했으면 게임 종료
    if elst.count(1) == M:
        break


# 모든 참가자들의 이동 거리 합
print(sum(dlst))

# 출구 좌표
print(ei+1,ej+1)

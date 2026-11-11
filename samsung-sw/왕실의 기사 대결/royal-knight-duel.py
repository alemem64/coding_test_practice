from collections import deque

def myprint(arr):
    print("#"*30)
    for lst in arr:
        print(*lst,sep=' ')
    print("#"*30)

###############
L,N,Q = map(int,input().split())

# 0 빈칸, 1 함정 2 벽
carr = [list(map(int,input().split())) for _ in range(L)]

# 0 빈칸, k 기사 번호
karr = [[0]*L for _ in range(L)]

# r,c,h,w
klst = [[] for _ in range(N+1)]

# 기사별 체력
hlst = [0] * (N+1)

# 입은 데미지 리스트
dlst = [0] * (N+1)

for n in range(1,N+1):
    r,c,h,w,k = map(int,input().split())
    klst[n] = [r-1,c-1,h,w]
    hlst[n] = k
    for hi in range(h):
        for wi in range(w):
            karr[r-1+hi][c-1+wi] = n

# 명령 리스트
clst = [list(map(int,input().split())) for _ in range(Q)]

# 상우하좌
di = [-1,0,1,0]
dj = [0,1,0,-1]

# myprint(karr)

# Q번의 명령에 대해서
for k,d in clst:
    
    # 체력이 1이상인 기사이면서 명령 받은 기사를 q에 넣기
    if hlst[k] <=0: continue # 죽은 기사는 건너뛰기
    
    q1 = deque()
    q1.append(k)

    q2 = deque()
    q2.append(k)
   
    v = set()

    # q에서 꺼낸 기사가 다음칸이 격자내이고 벽이 아니라면 미는 q에 추가
    while q1:
        cur = q1.popleft()
        ci,cj,ch,cw = klst[cur]
        ni,nj = ci+di[d],cj+dj[d]
        
        canmove = []
        for hi in range(ch):
            for wi in range(cw):
                # 벽이 아니고 격자 안이라면
                if 0<=ni+hi<=L-1 and 0<=nj+wi<=L-1 and carr[ni+hi][nj+wi] != 2 :
                    canmove.append(0)
                else: canmove.append(1)
        
        # 벽이 아니고 격자 안이라면
        if not sum(canmove):

            
            # 밀렸는데 해당 칸에 체력 1 이상인 다른 기사가 있다면 한 번만 q에 넣기
            for hi in range(ch):
                for wi in range(cw):
                    nxt = karr[ni+hi][nj+wi]
                    # 다음칸이 기사이고 내가 아니고 체력이 1이상이고 추가한 적 없으면
                    if nxt!=cur and nxt>= 1 and hlst[nxt] >=1 and nxt not in v:
                        v.add(nxt)
                        q1.append(nxt)
                        q2.append(nxt)
            
                        

        # q에서 꺼냈는데 격자밖이거나 벽이라면 밀림 종료
        else:
            # print('q초기화')
            q2 = deque()
            break
    
    # q에 든 순서대로 밀고 함정 데미지 추가
    while q2: 
        cur = q2.popleft()
        ci,cj,ch,cw = klst[cur]
        ni,nj = ci+di[d],cj+dj[d]

        # 죽었으면 건너뛰기
        if hlst[cur] <= 0: continue

        # q에서 꺼낸 기사 1칸 밀기
        klst[cur][0] += di[d]
        klst[cur][1] += dj[d]

        # 확인 완료 후 현재 기사 1칸 미는 좌표 갱신
        for hi in range(ch):
                for wi in range(cw):
                    karr[ci+hi][cj+wi] = 0
                    karr[ni+hi][nj+wi] = cur

        # 첫 번째 기사가 아니라면 밀리고 난 위치의 함정 수만큼 체력 깎고 데미지 추가
        cnt = 0
        if cur != k:
            for hi in range(ch):
                for wi in range(cw):
                    if carr[ni+hi][nj+wi] == 1:
                        cnt +=1
        hlst[cur] -= cnt
        dlst[cur] += cnt

    # 완료 후 좌표 갱신
    for idx in range(1,N+1):
        r,c,h,w = klst[idx]
        
        for hi in range(h):
            for wi in range(w):
                if hlst[idx] <= 0:
                    karr[r+hi][c+wi] = 0
                else:
                    karr[r+hi][c+wi] = idx
    # print(hlst)
    # print(klst)
    # myprint(karr)

# hlst에서 체력이 1이상인 기사들에 대해서 받은 dlst 총합 출력
ans = 0
for idx in range(1,N+1):
    if hlst[idx] >=1:
        ans += dlst[idx]
    
print(ans)
    
    


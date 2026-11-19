def myprint(arr):
    tarr = [lst[:] for lst in arr]
    for idx in range(1,M+1):
        pi,pj = plst[idx]
        tarr[pi][pj] = idx
    for ti,tj in tlst:
        tarr[ti][tj] = f'({tarr[ti][tj]})'
    tarr[fi][fj] = -2
    for lst in tarr:
        print(*lst,sep=' ')

    print('#'*30)

def myprint2(arr):
    for lst in arr:
        print(*lst,sep=' ')
    print('#'*30)


def move_hider():
    # 살아 있고 술래와의 거리가 3 이하인 도망자들 이동
    for idx in range(1,M+1):
        pi,pj = plst[idx]
        if dead[idx] == 0 and (abs(fi-pi) + abs(fj-pj)) <= 3:
            di,dj = dirc[dlst[idx]]
            ni,nj = pi+di,pj+dj
            # 격자 내이면서 술래 없으면 이동
            if 0<=ni<=N-1 and 0<=nj<=N-1 and (fi,fj) != (ni,nj):
                plst[idx] = [ni,nj]
            # 격자 밖일 때 반대로, 술래 없으면 이동
            elif not 0<=ni<=N-1 or not 0<=nj<=N-1:
                dlst[idx] = (dlst[idx] + 2) % 4 # 방향 반대로
                di,dj = dirc[dlst[idx]]
                ni,nj = pi+di,pj+dj
                if (fi,fj) != (ni,nj):
                    plst[idx] = [ni,nj]

def make_snail():
    srp = [[0,0]]
    srd = [2]
    ci,cj = 0,0
    cd = 2
    ei = ej = (N-1) // 2

    v = [[0]*N for _ in range(N)]
    v[ci][cj] = 1

    while True:
        # print(ci,cj,cd)
        if (ci,cj) == (ei,ej):
            srd[-1] = 2
            break
        di,dj = dirc[cd]
        ni,nj = ci+di,cj+dj
        nni,nnj = ni+di,nj+dj
        # 격자 내, 미방문이면 이동
        if 0<=nni<=N-1 and 0<=nnj<=N-1 and v[nni][nnj] == 0:
            ci,cj = ni,nj
            v[ni][nj] = 1
            srp.append([ni,nj])
            srd.append(cd)
        else:
            ci,cj = ni,nj
            v[ni][nj] = 1
            cd = (cd-1) % 4
            srp.append([ni,nj])
            srd.append(cd)
    sd = [0]

    for d in srd:
        sd.append((d+2)%4)

    sd.pop()
    sp = srp[::-1]

    return srp,sp,sd,srd[::-1]

def move_finder(fi,fj,curp,curd):
    ni,nj = curp.pop()
    nd = curd.pop()
    M = (N-1) // 2

    if (ni,nj) == (0,0):
        curp = orirp[:]
        curd = orird[:]
        curp.pop()
        nd = curd.pop()
    elif (ni,nj) == (M,M):
        curp = orip[:]
        curd = orid[:]
        curp.pop()
        nd = curd.pop()
    return ni,nj,nd,curp,curd

def catch(fi,fj,fd):
    caught = 0
    for offset in range(3):
        di,dj = dirc[fd]
        ci,cj = fi+di*offset,fj+dj*offset

        # 범위 밖이면 멈추기
        if not 0<=ci<=N-1 or not 0<=cj<=N-1:
            break

        for idx in range(1,M+1):
            if dead[idx] == 1: continue
            pi,pj = plst[idx]

            if (ci,cj) == (pi,pj) and arr[pi][pj] != -1:
                caught +=1
                dead[idx] = 1

    return caught

##########
N,M,H,K = map(int,input().split())

# 술래 -2, 나무 -1, 0 빈공간, m 도망자
arr = [[0]*N for _ in range(N)]

plst = [[]]
dlst = [[]]
dead = [0]*(M+1) # 죽었으면 1
tlst = []

fi = fj = (N-1) // 2
fd = 0

# 상우하좌
dirc = ((-1,0),(0,1),(1,0),(0,-1))

for idx in range(1,M+1):
    pi,pj,pd = map(int,input().split())
    plst.append([pi-1,pj-1])

    if pd == 1: dlst.append(1)
    elif pd == 2: dlst.append(2)

for _ in range(H):
    hi,hj = map(int,input().split())
    arr[hi-1][hj-1] = -1
    tlst.append([hi-1,hj-1])


orip,orirp,orid,orird = make_snail()
#print(orip)
#print(orid)
#print(orirp)
#print(orird)
curp = orip[:]
curd = orid[:]
curp.pop()
curd.pop()

#test = [[0]*N for _ in range(N)]
#for idx in range(1,48):
#    fi,fj,fd,curp,curd = move_finder(fi,fj,curp,curd)
#    test[fi][fj] = fd
#myprint2(test)

ans = 0

#myprint(arr)

# K턴 동안 반복
for k in range(1,K+1):
    move_hider()

    fi,fj,fd,curp,curd = move_finder(fi,fj,curp,curd)

    n_caught = catch(fi,fj,fd)

    score = k*n_caught

    ans += score
    #print(score)
    #myprint(arr)
    
print(ans)
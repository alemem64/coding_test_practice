n, m = map(int, input().split())
A = list(map(int, input().split()))

answer = 0


def choose(start, count, xor_value):
    global answer

    # M개를 모두 골랐다면 최댓값 갱신
    if count == m:
        answer = max(answer, xor_value)
        return

    # 남은 수를 모두 골라도 M개를 채울 수 없다면 종료
    if n - start < m - count:
        return

    for i in range(start, n):
        choose(i + 1, count + 1, xor_value ^ A[i])


choose(0, 0, 0)
print(answer)
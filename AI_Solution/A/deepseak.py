def solve():
    A1, A2, A3, N = map(int, input().split())
    A4 = A3 - A2 + A1
    period_sum = 2 * (A1 + A3)  # A1 + A2 + A3 + A4
    q, r = divmod(N, 4)
    ans = q * period_sum
    if r >= 1:
        ans += A1
    if r >= 2:
        ans += A2
    if r >= 3:
        ans += A3
    print(ans)

if __name__ == "__main__":
    solve()
    

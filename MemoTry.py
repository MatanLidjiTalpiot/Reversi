memo = {}
def fib(n):
    if n in memo:
        return memo[n]

    if n == 1 or n == 0:
        return n
    else:
        ret= fib(n-1) + fib(n-2)
        memo[n] = ret
        return ret

print(fib(300))
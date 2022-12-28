def create_fibonacci(n):
    """Get n-th fibonacci number"""
    if n <= 1:
        return n
    res = n
    n1 = 0
    n2 = 1
    for _ in range(n-1):
        res = n1 + n2
        n1 = n2
        n2 = res
    return res

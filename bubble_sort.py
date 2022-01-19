def bubble_sort(x, compare_func=None):
    if compare_func is None:
        def compare_func(a, b):
            return a > b
    
    n = len(x)
    for k in range(n-1, 0, -1):
        for i in range(k):
            if compare_func(x[i], x[i+1]):
                x[i], x[i+1] = x[i+1], x[i]
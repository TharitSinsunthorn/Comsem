def bubble_sort(x, key=None, reverse=False):
    if key is None:
        def key(x):
            return x

    if reverse:
        def compare_func(a, b):
            return a < b
    else:
        def compare_func(a, b):
            return a > b
    
    n = len(x)
    for k in range(n-1, 0, -1):
        for i in range(k):
            if compare_func(key(x[i]), key(x[i+1])):
                x[i], x[i+1] = x[i+1], x[i]
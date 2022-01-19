def bubble_sort(x):
    n = len(x)
    for k in range(n-1, 0, -1):
        for i in range(k):
            if x[i].math_mark > x[i+1].math_mark:
                x[i], x[i+1] = x[i+1], x[i]
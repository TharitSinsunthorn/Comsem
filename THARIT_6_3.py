def bubble_sort(x, key=None, reverse=False):
    if key is None:
        def key(x):
            avg = (x[1] + x[2])/2
            return avg
        
        def key2(x):
            return min(x[1], x[2])
        
        def key3(x):
            return x[1]

    if reverse:
        def compare_func(a, b):
            if key(a) != key(b):
                return key(a) < key(b)
            else:
                if key2(a) != key2(b):
                    return key2(a) < key2(b)
                elif key3(a) != key3(b):
                    return key3(a) < key3(b)
                
    else:
        def compare_func(a, b):
            if key(a) != key(b):
                return key(a) > key(b)
            else:
                if key2(a) != key2(b):
                    return key2(a) > key2(b)
                elif key3(a) != key3(b):
                    return key3(a) > key3(b)
    
    n = len(x)
    for k in range(n-1, 0, -1):
        for i in range(k):
            if compare_func(x[i], x[i+1]):
                x[i], x[i+1] = x[i+1], x[i]

X = []
X.append(("Alice", 90, 95))
X.append(("Bob", 80, 75))
X.append(("Charlie", 0, 100))
X.append(("Dave", 75, 80))
X.append(("Ellen", 77, 78))
bubble_sort(X, key=None, reverse=True)
print(X)
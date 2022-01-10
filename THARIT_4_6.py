def set_to_zero_vector(vec, n_elements):
    vec.clear()
    for _ in range(n_elements):
        vec.append(0)

x = []
set_to_zero_vector(x, 3)
assert x == [0, 0, 0] 

y = [10, 20] 
set_to_zero_vector(y, 5) 
assert y == [0, 0, 0, 0, 0]
square_items = []
for num in range(10):
    square_items.append(num**2)
print(square_items)

square_items_lc = [num**2 for num in range(10)]
print(square_items_lc)

combs = []
for x in [1,2,3]:
    for y in [3,2,1]:
        if x != y:
            combs.append((x, y))
print(combs)
combs_lc = [(x,y) for x in [1,2,3] for y in [3,2,1] if x!= y]
print(combs_lc)

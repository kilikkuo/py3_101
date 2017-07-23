seqString = 'abcde'
seqList = [6, 3, 1, 2, 8]
for item in seqString:
    print(item)
print(' for =>>>>> ')
for item in seqList:
    print(item)
print(' while =>>>>> ')
count = 10
while count > 0:
    count = count - 1 
    print(count)
print(' for =>>>>> continue ')
for state in ['飽', '飽', '餓', '飽', '餓']:
    if state == '飽':
        continue
    print('覓食吧...')
print(' nested for =>>>>> continue ')
for index in range(-2, 10):
    for letter in 'python27':
        if letter != 't':
            continue
        print(letter)
    if index % 2 != 0:
        continue
    print(index)
print(' while =>>>>> break ')
value = 0
while value <= 10:
    print(value)
    if value >= 5:
        break
    value += 1
print(' nested loop =>>>>> break ')
value = 0
while value <= 10:
    print('value = {}'.format(value))
    for idx in range(value):
        if idx >= 2:
            # 中斷且跳出最靠近的 loop
            break
        print('idx = {}'.format(idx))
    value += 1
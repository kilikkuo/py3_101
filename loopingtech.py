bags = ['potion', 'super_potion', 'hyper_potion']
# 列舉 sequence 裡的項目, 並且回傳 index 與 item
for index, name in enumerate(bags):
   print('Item index {} is {}'.format(index, name))
# ====================================================
print('====================================================')
questions = ['name', 'age', 'favirot food']
answers = ['McDonald', '100', 'burger']
# 組合兩個 sequence, 並且一個接一個回傳每個組合
for q, a in zip(questions, answers):
    print('What\'s your {} ? It\'s {}'.format(q, a))
# ====================================================
print('====================================================')
# 將 sequence 反轉
for idx in reversed(range(0, 3)):
    print('Idx = {}'.format(idx))
# ====================================================
print('====================================================')
bags = ['potion', 'super_potion', 'hyper_potion']
# 將 sequence 排序
for name in sorted(bags):
    print('Item is {}'.format(name))
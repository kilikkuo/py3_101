pkm_set = set(['pikachu', 'raichu', 'bulbasaur', 'raichu'])
pkm_set2 = {'raichu'}
pkm_set3 = {'charmander'}
pkm_set4 = {'raichu', 'charmander'}

# 交集
print(pkm_set & pkm_set2) # {‘raichu’}
# 差集
print(pkm_set - pkm_set2) # {‘pikachu’, ‘balbasaur’}
# 聯集
print(pkm_set | pkm_set3) # {'pikachu', 'bulbasaur', 'charmander', 'raichu'}
# 互斥
print(pkm_set ^ pkm_set4) # {'pikachu', 'bulbasaur', 'charmander'}

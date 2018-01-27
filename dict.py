import datetime

personal_info = {'name' : 'Kilik', '生日' : datetime.date(1983, 2, 26), 'Age' : 34}
print('個人資料 => {}'.format(personal_info))
print('印出 \'name\' => {}'.format(personal_info['name'])) # 'Kilik'

# 新增 key : value
personal_info['gender'] = 'male'
print('新增 \'gender\' 後 => {}'.format(personal_info))
# {'生日': datetime.date(1983, 2, 26), 'name': 'Kilik', 'Age': 34, 'gender': 'male'}

# 修改
personal_info['Age'] = 50
print('修改 \'Age\' 後 => {}'.format(personal_info))
# {'生日': datetime.date(1983, 2, 26), 'name': 'Kilik', 'Age': 50, 'gender': 'male'}

# 刪除
del personal_info['生日']
print('刪除 \'生日\' => {}'.format(personal_info))
# {'name': 'Kilik', 'Age': 50, 'gender': 'male'}

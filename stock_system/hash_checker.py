import os
import time
import hashlib

t1 = time.time()

# 一次讀入的資料大小
block_size = 2**20

cwd = os.getcwd()
m = hashlib.md5()

csv_dir = os.path.join(cwd, '2018-02-02_all')
for root, dirs, files in os.walk(csv_dir):
    # 針對所有 csv 的檔案, 每一個的資料都讀入並且餵進 md5 去產生 digest.
    if files:
        for f in files:
            fname = os.path.join(csv_dir, f)
            with open(fname, "rb", encoding='utf8') as f:
                while True:
                    buf = f.read(block_size)
                    if not buf:
                        break
                    m.update(buf)

print('MD5 (csv) : {}'.format(m.hexdigest()))
sdbp_fname = os.path.join(cwd, 'sourcedata.p')
# 如果有產生過 sourcedata.p 之後, 也將 sourcedata.p 餵入 md5 產生 digest
if os.path.exists(sdbp_fname):
    with open(sdbp_fname, "rb", encoding='utf8') as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    print('MD5 (csv+sourcedata.p) : {}'.format(m.hexdigest()))
t2 = time.time()
print(' Generating MD5 took {} seconds'.format(t2-t1))
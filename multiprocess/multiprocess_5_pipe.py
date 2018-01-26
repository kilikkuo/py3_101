from multiprocessing import Process, Pipe

def handle(conn):
    # 接收來自 conn_p 送的資料
    print('[Child] recv : {} '.format(conn.recv()))
    # 送出資料給 conn_p
    conn.send([10, 'hi', None])
    # 從 child 端關閉 child process 的 conn 端口，這不影響 parenet process 的接收端口
    conn.close()
    print('[Child] conn close : {}'.format(conn.closed))
    print('[Child] Exit')

if __name__ == '__main__':
    # 建立一對 connection pair, 兩端可以互相溝通.
    # Parent 使用 parent 的 connection 進行 send/recv
    # Child 使用 child 的 connection 進行 send/recv
    conn_p, conn_c = Pipe()
    # 建立 & 啟動 child process
    proc_c = Process(target=handle, args=(conn_c,))
    proc_c.start()
    # Parent 透過 conn_p 送出資料給 child 的 conn (也就是 conn_c)
    conn_p.send('Greetings from Parent')
    # Parent 從 conn_p 接收來自 child 透過 conn_c 送出的資料
    print('[Parent] recv : {}'.format(conn_p.recv()))
    # 等待直到 child process 完成
    proc_c.join()
    # 在 child process 關閉，並不影響 parent process 對於 Child 的端口
    print('[Parent] conn_c close : {}'.format(conn_c.closed))
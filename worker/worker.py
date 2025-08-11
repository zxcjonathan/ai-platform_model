# worker/worker.py

import time
from redis import Redis
from redis.exceptions import ConnectionError
from rq import Worker, Queue

# 連接到 Redis
redis_conn = None
# 設定連線重試次數和間隔
max_retries = 10
retry_delay = 5  # 秒

for i in range(max_retries):
    try:
        print(f"嘗試連線到 Redis... (第 {i+1} 次)")
        redis_conn = Redis(host='redis', port=6379)
        # 嘗試ping Redis以確認連線成功
        redis_conn.ping()
        print("Redis 連線成功！")
        break
    except ConnectionError as e:
        print(f"Redis 連線失敗: {e}")
        if i < max_retries - 1:
            print(f"等待 {retry_delay} 秒後重試...")
            time.sleep(retry_delay)
        else:
            print("達到最大重試次數，無法連線到 Redis。")
            exit(1)

listen = ['default']

if __name__ == '__main__':
    queues = [Queue(name, connection=redis_conn) for name in listen]
    
    print("工作者啟動，等待任務中...")
    worker = Worker(queues, connection=redis_conn)
    worker.work()
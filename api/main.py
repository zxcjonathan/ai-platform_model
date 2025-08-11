# api/main.py

from fastapi import FastAPI, HTTPException
from redis import Redis
from rq import Queue
from rq.job import Job
from tasks.train import train_model # 匯入你的 AI 訓練任務函數

app = FastAPI()

# 連接到 Redis 佇列，使用 docker-compose 的服務名稱
redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)

@app.get("/")
def read_root():
    """
    提供一個根路徑，用於檢查 API 服務是否正常運行。
    """
    return {"message": "歡迎來到 AI Platform API！服務正常運行。"}

@app.post("/tasks/train")
def submit_training_job():
    """
    提交一個新的訓練任務到佇列。
    """
    # 這裡我們將 task_train_model 設為一個回傳模型儲存路徑的函式
    job = q.enqueue(train_model)
    return {"message": "訓練任務已提交", "job_id": job.id}

@app.get("/tasks/{job_id}/status")
def get_job_status(job_id: str):
    """
    根據 job_id 查詢任務狀態和結果。
    """
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        status = job.get_status()
        result = job.result if status == 'finished' else None
        
        return {"job_id": job.id, "status": status, "result": result}
    except Exception as e:
        return {"error": str(e), "message": "Job not found"}
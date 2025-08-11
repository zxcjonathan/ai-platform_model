# 使用官方 Python 3.11 映像檔作為基礎
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 將 requirements.txt 複製到容器中
COPY requirements.txt .

# 安裝所有必要的 Python 套件
# 使用 --extra-index-url 確保能正確安裝 PyTorch CPU 版本
RUN pip install --no-cache-dir -r requirements.txt

# 將專案程式碼複製到容器中
COPY . .

# 定義一個環境變數，讓 Python 的輸出立即顯示
ENV PYTHONUNBUFFERED=1

# 設置啟動指令（這是最佳實踐，雖然在 docker-compose 中會被覆寫）
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制代码及模板静态文件
COPY . .

# 运行服务，绑定 0.0.0.0 端口8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

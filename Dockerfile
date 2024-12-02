FROM python:3.8.20-slim

# 设置工作目录
WORKDIR /app

# 复制项目代码到容器
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 暴露 FastAPI 服务端口
EXPOSE 8000

# 容器启动命令




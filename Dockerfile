FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8081
CMD ["uvicorn", "mcp.server:app", "--host", "0.0.0.0", "--port", "8081"]

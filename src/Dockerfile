FROM python:3.10-slim
LABEL description="fastapi"
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "main.py"]
FROM python:3.7

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -U wheel cmake
RUN pip3 install -r requirements.txt --no-cache-dir
RUN export PYTHONPATH='${PYTHONPATH}:/app'

COPY . .

EXPOSE 5000
CMD ["python3", "./app.py"]

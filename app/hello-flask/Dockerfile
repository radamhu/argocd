FROM python:3.6.12-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
# CMD ["python", "app.py"]
ENTRYPOINT ["./gunicorn.sh"]

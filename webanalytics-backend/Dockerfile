FROM python:3.10

WORKDIR /app

COPY backend-requirements.txt .

RUN pip install --no-cache-dir "setuptools<58.0.0"
RUN pip install --no-cache-dir -r backend-requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["ls"]
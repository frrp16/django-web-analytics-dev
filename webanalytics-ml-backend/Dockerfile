FROM python:3.10

WORKDIR /app

COPY ml-backend-requirements.txt .

RUN pip install --no-cache-dir "setuptools<58.0.0"
RUN pip install --no-cache-dir -r ml-backend-requirements.txt

COPY . .

EXPOSE 8001

COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]

# CMD ["ls"]
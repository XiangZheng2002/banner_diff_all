FROM python:3.10.14-slim-bookworm

WORKDIR /usr/src/app

COPY ./backend/requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

# CMD [ "sqlite3", "./backend/instance/db.sqlite3"]

EXPOSE 5000

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


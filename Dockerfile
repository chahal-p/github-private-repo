FROM python:3.9.0b5-alpine3.12
COPY . /app
WORKDIR /app

RUN apk update
RUN apk add g++
RUN apk add libffi-dev
RUN apk add libressl-dev

RUN python -m pip install --upgrade pip
RUN pip install -r python-dependencies.txt

EXPOSE 5000/tcp
RUN export FLASK_APP=session.app.py
RUN export FLASK_ENV=production
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
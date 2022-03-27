# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
EXPOSE 5000
WORKDIR /app

# no default value
ENV api_key _

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
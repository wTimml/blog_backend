FROM python:3.9-slim

WORKDIR /usr/src/blog_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/blog_backend/entrypoint.sh
RUN chmod +x /usr/src/blog_backend/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/blog_backend/entrypoint.sh"]
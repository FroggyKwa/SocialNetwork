FROM python:3.10

ARG NAME
ARG PORT

RUN mkdir -p "/usr/src/${NAME}_backend"

WORKDIR "/usr/src/${NAME}"

COPY ./requirements.txt "/usr/src/${NAME}"
RUN pip install --no-cache-dir -r requirements.txt
COPY . "/usr/src/${NAME}"
EXPOSE ${PORT}

CMD gunicorn SocialNetwork.asgi:application -w 4 -b 0.0.0.0:${PORT} -k uvicorn.workers.UvicornWorker 

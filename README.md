# SocialNetwork
<b>to run:</b>
<br>
``docker-compose up --build``
<br>
<br>
<br>
<b>or to run database and asgi server independently:</b>
<br>
``./start_db.sh``
<br>
``gunicorn SocialNetwork.asgi:application --reload -w 4 -b 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker
``
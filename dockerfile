FROM python:3.8.0
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=1 --bind 0.0.0.0:$PORT app:app



## 1312

## Heroku dynamically assigns your app a port, so you can't set the port to a fixed number. Heroku adds the port to the env, so you can pull it from there. Switch your listen to this:

## .listen(process.env.PORT || 5000)
## That way it'll still listen to port 5000 when you test locally, but it will also work on Heroku.

## You can check out the Heroku docs on Node.js

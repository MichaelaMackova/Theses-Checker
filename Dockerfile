FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OPERATING_SYSTEM=Linux
ENV RELATIVE_STATIC_ROOT=staticfiles

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements_web.txt /app/

RUN pip install -r requirements_web.txt
RUN pip install uwsgi

COPY . .

WORKDIR /app/src/web

RUN --mount=type=secret,id=SECRET_KEY,env=SECRET_KEY python manage.py collectstatic --noinput

RUN rm -rf static && ln -s staticfiles static

EXPOSE 8000

CMD ["uwsgi", "--http", "0.0.0.0:8000", "--module", "web.wsgi:application", "--master", "--processes", "4", "--static-map", "/static=staticfiles"]

FROM python:3.11-alpine

ENV PYTHONBUFFERED 1

COPY ./requirements.txt tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --upgrade --no-cache postgresql-client jpeg-dev && \
    apk add --upgrade --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r tmp/requirements.txt && \
    if [ $DEV = 'true']; \
        then /py/bin/pip install -r /tmp/requirments.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disable-password \
        --no-create-password \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chown -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD["run.sh"]

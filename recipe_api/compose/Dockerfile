FROM python:3.11.9-alpine

ENV PYTHONUNBUFFERED 1

ADD ./requirements/ requirements/
RUN pip install -r requirements/local.txt

COPY ./compose/entrypoint.sh ./entrypoint
RUN chmod +x /entrypoint

WORKDIR /app
ADD ./ ./

ENTRYPOINT [ "/entrypoint" ]

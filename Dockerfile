FROM python:3.8

ENV PORT 5000
ENV HOST 0.0.0.0

EXPOSE 5000

RUN apt-get update -y && \
    apt-get install -y python3-pip

COPY ./requirement.txt /app/requirement.txt

WORKDIR /app

RUN pip install -r requirement.txt

COPY . /app


ENTRYPOINT ["python"]

CMD [ "app.py" ]
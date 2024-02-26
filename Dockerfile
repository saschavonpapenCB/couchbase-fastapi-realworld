FROM python:3.9-slim-bullseye

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/api

ENV DB_CONN_STR=couchbases://cb.zlaigahlligbqidy.cloud.couchbase.com
ENV DB_PASSWORD=RealWorld123456!
ENV DB_USERNAME=Administrator
ENV DB_BUCKET_NAME=travel-sample
ENV DB_SCOPE_NAME=inventory

CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "8000"]

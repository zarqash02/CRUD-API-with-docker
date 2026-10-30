FROM python:3.15-slim

WORKDIR /crud-api

COPY ./requirements.txt /crud-api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /crud-api/requirements.txt

COPY . /crud-api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
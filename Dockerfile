FROM python:3.13-slim 

WORKDIR /main 
ENV PYTHONPATH=/main

COPY requirements.txt . 

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY alembic.ini .
COPY alembic ./alembic
COPY pytest.ini .
COPY .env .
COPY app ./app 
COPY tests ./tests 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

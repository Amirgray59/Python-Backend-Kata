FROM python:3.13-slim 

WORKDIR /main 

COPY requirements.txt . 

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY app ./app 
COPY tests ./tests 

RUN pip install "fastapi[standard]"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

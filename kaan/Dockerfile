FROM python:3.11.8

WORKDIR /src

ADD ./ /src 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main.classify:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.10

WORKDIR /app
ADD ./ /app
RUN mkdir -p /app/data
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000 
CMD ["uvicorn","main:mou","--host","0.0.0.0","--port","8000","--reload"]
FROM python:3.8

RUN useradd -ms /bin/bash user  
USER user

RUN poetry export -f requirements.txt --output requirements.txt
COPY requirements.txt .

EXPOSE 10000

ENTRYPOINT ["python", "main.py"]

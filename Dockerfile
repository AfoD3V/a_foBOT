FROM python:3.10

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user

RUN poetry export -f requirements.txt --output requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY . .

EXPOSE 10000

ENTRYPOINT ["python", "main.py"]

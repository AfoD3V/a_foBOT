FROM python:3.10

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user

COPY src .

RUN pip install poetry
RUN poetry install

EXPOSE 10000

ENTRYPOINT ["python", "main.py"]
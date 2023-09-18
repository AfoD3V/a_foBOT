FROM python:3.10

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user

COPY src .

FROM python:3.10

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user

COPY src .

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl


EXPOSE 10000

ENTRYPOINT ["python", "main.py"]
EXPOSE 10000

ENTRYPOINT ["python", "main.py"]

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user

COPY src .

RUN apt-get update && apt-get install -y gcc libffi-dev musl-dev postgresql-dev
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl


EXPOSE 10000

ENTRYPOINT ["python", "main.py"]


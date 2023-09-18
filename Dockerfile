
I see that you're using a Dockerfile to set up a Python environment with Poetry and some specific dependencies. Based on the Dockerfile you provided, I'll create a new one below, making sure it's structured correctly:

Dockerfile
Copy code
# Use a base Python image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Create a user and switch to that user
RUN useradd -ms /bin/bash user
USER user

# Copy project files into the working directory
COPY src .

# Install necessary system dependencies
RUN apt-get update && apt-get install -y gcc libffi-dev musl-dev postgresql-dev

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Create a virtual environment
RUN python -m venv /venv

# Copy project configuration files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

# Copy the rest of the project files
COPY . .

# Build the project
RUN poetry build && /venv/bin/pip install dist/*.whl

# Expose the port your application will run on
EXPOSE 10000

# Define the default command to run when the container starts
ENTRYPOINT ["python", "main.py"]

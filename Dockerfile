FROM python:3.11-buster

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root && rm -rf $POETRY_CACHE_DIR

EXPOSE 8000

# Copy the project files
COPY atom ./atom

ENTRYPOINT ["poetry", "run", "python", "-m", "atom.main"]

#CMD ["uvicorn", "atom:main:app", "--host", "0.0.0.0", "--port", "8000"]

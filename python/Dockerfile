# syntax=docker/dockerfile:1

# Base setup
FROM python:3.11.9 AS base
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app


# Standalone testing 
FROM base AS test

RUN pip install coverage pytest pytest-asyncio

COPY ./app_driver.py /code
COPY ./tests /code/tests
RUN chmod +x /code/tests/entrypoint.sh

CMD ["/code/tests/entrypoint.sh", "/code/tests"]

# Standalone app 
FROM base AS app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port", "8000"]

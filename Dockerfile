FROM python:3.14.5
WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install --no-root

COPY src .
CMD ["poetry", "run", "python", "-m", "elkollege_guidance_bot"]

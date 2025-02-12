FROM python:3.12-slim

WORKDIR /app

# Install poetry and wait-for-it
RUN pip install poetry && \
    apt-get update && \
    apt-get install -y wget && \
    wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy application
COPY . .

# Install the application
RUN poetry install --no-interaction --no-ansi

# Create entrypoint script
RUN echo '#!/bin/sh\n\
wait-for-it.sh db:5432 -t 60 -- echo "Database is up"\n\
poetry run alembic upgrade head\n\
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000\n'\
> /app/entrypoint.sh \
&& chmod +x /app/entrypoint.sh

# Run the application with migrations
CMD ["/app/entrypoint.sh"]

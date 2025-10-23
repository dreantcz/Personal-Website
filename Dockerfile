FROM python:3.11-slim

# Install build dependencies then clean up to keep image small
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port (app uses 3000 in project)
EXPOSE 3000

# Set Flask environment for development and run on all interfaces
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3000

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
# syntax=docker/dockerfile:1

FROM node:lts-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
EXPOSE 3000
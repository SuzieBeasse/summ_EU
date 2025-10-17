FROM python:3.12.9-slim

COPY backend_summeu/requirements.txt /requirements.txt
COPY backend_summeu /backend_summeu

# Install Python dependencies
RUN pip install --upgrade pip
RUN apt-get -y update
RUN apt-get -y upgrade
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e backend_summeu

# Run the application when the container launches
CMD uvicorn backend_summeu.api.fast:app --host 0.0.0.0 --port $PORT

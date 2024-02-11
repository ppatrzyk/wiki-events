FROM python:3.12.1-slim

COPY ./ ./dash/
WORKDIR /dash
RUN pip3 install -r requirements.txt

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app:server" ]
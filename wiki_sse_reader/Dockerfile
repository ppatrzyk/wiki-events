FROM python:3.12.1-slim

COPY ./ ./wiki_sse_reader/
WORKDIR /wiki_sse_reader
RUN pip3 install -r requirements.txt

CMD [ "python3", "run.py" ]
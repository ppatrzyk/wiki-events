FROM python:3.12.1-slim

RUN apt-get update \
    && apt-get install -y \
    cron \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./ ./wiki_dbt/
WORKDIR /wiki_dbt
RUN pip3 install -r requirements.txt

RUN cp crontab /etc/cron.d/crontab \
    && chmod 0644 /etc/cron.d/crontab \
    && /usr/bin/crontab /etc/cron.d/crontab

CMD ["/usr/sbin/cron", "-f"]

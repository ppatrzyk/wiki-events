-- Queue read definition
-- https://clickhouse.com/docs/en/engines/table-engines/integrations/rabbitmq

-- TODO parse data according to schema, change in run.py as well
-- https://clickhouse.com/docs/en/sql-reference/data-types/json

-- TODO decide multiple streams into multiple tables? wikissereader multiple containers each routing to own queue vs stuff dumped into one table

USE wiki;

CREATE TABLE wiki_stream (
    time DateTime64(4, 'Etc/UTC'),
    data String
) ENGINE = RabbitMQ SETTINGS 
    rabbitmq_address = 'amqp://user_666:password_666@rabbit:5672',
    rabbitmq_queue_consume = true,
    rabbitmq_queue_base = 'wikiqueue',
    rabbitmq_format = 'JSONEachRow',
    rabbitmq_num_consumers = 1,
    date_time_input_format = 'best_effort';

CREATE TABLE wiki (
    id UUID DEFAULT generateUUIDv4(),
    time DateTime64(4, 'Etc/UTC'),
    data String
)
ENGINE = MergeTree()
ORDER BY time;

CREATE MATERIALIZED VIEW wiki_stream_mv TO wiki
AS SELECT generateUUIDv4(), time, data FROM wiki_stream;

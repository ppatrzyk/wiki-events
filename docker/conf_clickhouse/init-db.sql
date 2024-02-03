
USE wiki;

CREATE TABLE wiki_stream (
    created_at DateTime64(4, 'Etc/UTC'),
    data_raw_json String
) ENGINE = RabbitMQ SETTINGS 
    rabbitmq_address = 'amqp://user_666:password_666@rabbit:5672',
    rabbitmq_queue_consume = true,
    rabbitmq_queue_base = 'wikiqueue',
    rabbitmq_format = 'JSONEachRow',
    rabbitmq_num_consumers = 1,
    date_time_input_format = 'best_effort';

CREATE TABLE wiki_raw (
    id UUID DEFAULT generateUUIDv4(),
    created_at DateTime64(4, 'Etc/UTC'),
    data_raw_json String
)
ENGINE = MergeTree()
ORDER BY created_at;

CREATE MATERIALIZED VIEW wiki_stream_mv TO wiki_raw
AS SELECT generateUUIDv4(), created_at, data_raw_json FROM wiki_stream;

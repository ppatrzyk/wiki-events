
USE wiki;

CREATE TABLE wiki_stream (
    created_at DateTime64(4, 'Etc/UTC'),
    data_raw_json String
) ENGINE = RabbitMQ SETTINGS 
    rabbitmq_address = 'amqp://rabbitro:rabbitro_pass@rabbit:5672',
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

create user clickhousero identified with sha256_password by 'clickhousero_pass' settings profile 'readonly';
grant select on wiki.* to clickhousero;

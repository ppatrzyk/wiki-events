from diagrams import Cluster, Diagram, Edge

from diagrams.generic.storage import Storage

from diagrams.onprem.analytics import Dbt
from diagrams.onprem.client import Users
from diagrams.onprem.database import Clickhouse
from diagrams.onprem.network import Traefik
from diagrams.onprem.queue import Rabbitmq

from diagrams.programming.language import Python

with Diagram("Wiki Events", show=False):
    user = Users("User")
    wiki = Storage("Wiki EventStreams")
    with Cluster("Docker Swarm"):
        db = Clickhouse("Clickhouse")
        proxy = Traefik("Traefik")
        dash = Python("wiki_dash [BI dashboard]")

        rabbit = Rabbitmq("RabbitMQ")
        ssereader = Python("wiki_sse_reader")
        dbt = Dbt("wiki_dbt")

    wiki >> Edge(label="read SSE") >> ssereader >> Edge(label="send to queue") >> rabbit >> Edge(label="ingest into") >> db
    dbt >> Edge(label="transform data")>> db
    db << Edge(label="access data") >> dash
    user << Edge(label="via http") >> proxy << Edge(label="route") >> dash

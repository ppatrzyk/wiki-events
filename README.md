# wiki-events

Project for https://github.com/DataTalksClub/data-engineering-zoomcamp

TODO write readme with proj description, some chart etc

## Architecture

TODO schema img + description

## Deployment

Common actions to be taken bot for cloud and local. Adjust paths for your system.

1. Clone this repo

```
todo
```

2. Install Docker

[Instructions for Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

3. Build docker images

```
cd wiki-events/wiki_sse_reader/
sudo docker build -t wikissereader:latest .

cd wiki-events/wiki_dbt/
sudo docker build . -t wikidbt:latest
```

4. Download clickhouse driver 

```
curl -L https://github.com/ClickHouse/metabase-clickhouse-driver/releases/download/1.3.3/clickhouse.metabase-driver.jar > docker/conf_metabase/clickhouse.metabase-driver.jar
```

### Cloud

#### Terraform

Create file `terraform/terraform.tfvars` with the following contents:

```
hcloud_token = "<HETZNER_API>"
```

TODO terraform instructions

#### Docker Swarm

set up swarm and deploy

```
mkdir /var/lib/swarm
mkdir /var/lib/swarm/{data_clickhouse,data_rabbit}

docker swarm init
docker network create --scope=swarm --attachable -d overlay internal
docker stack deploy -c docker/stack-data.yml data
docker stack deploy -c docker/stack-pipelines.yml pipelines
docker stack deploy -c docker/stack-bi.yml bi

```

traefik pass
https://doc.traefik.io/traefik/middlewares/http/basicauth/#configuration-options

metabase
```
admin@admin.admin
metabase_pass1
http://localhost:3000/public/dashboard/6d2cbb29-e310-4c80-ac3d-b8903d92efaf
```

TODO fix routers, now auth required on all requests

### Local

todo docker compose desc

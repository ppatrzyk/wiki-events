# Deployment

Common actions to be taken both for cloud and local. Adjust paths for your system.

1. Clone this repo

```
git clone https://github.com/ppatrzyk/wiki-events.git
```

2. [Install Docker]((https://docs.docker.com/engine/install/))

3. Build docker images

```
cd wiki-events/wiki_sse_reader/
docker build -t wikissereader:latest .

cd wiki-events/wiki_dbt/
docker build . -t wikidbt:latest

cd wiki-events/wiki_dash/
docker build . -t wikidash:latest
```

## Cloud

### Terraform

Create file `terraform/terraform.tfvars` with the following contents:

```
hcloud_token = "<HETZNER_API>"
```

Instructions on obtaining api key from your [Hetzner](https://www.hetzner.com/) account [here](https://community.hetzner.com/tutorials/howto-hcloud-terraform).

Creating server:

```
terraform init
terraform apply
```

Server data for logging in is sent via email. When doing basic setup of the server, you need to ensure that firewall allows access to port `80`.

### Docker Swarm

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

Dashboard is available at server's IP address: `http://<_SERVER_IP>/` behind basic http auth:

```
user: dezoomcamp
password: dezoomcamp
```

## Local

Code can also be run locally using docker compose.

```
cd docker
docker-compose up -d
```

Dashboard is exposed at http://localhost:8000/

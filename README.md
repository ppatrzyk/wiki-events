# wiki-events

Project for https://github.com/DataTalksClub/data-engineering-zoomcamp

TODO:
- bi app for dashboard
- write readme with proj description, some chart etc

## Architecture

TODO schema img + description

## Deployment

### Cloud

#### Terraform

Create file `terraform/terraform.tfvars` with the following contents:

```
hcloud_token = "<HETZNER_API>"
```

TODO terraform instructions

#### Server setup

[install docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

#### Docker Swarm

set up swarm and deploy

```
TODO swarm commands

wget https://github.com/ClickHouse/metabase-clickhouse-driver/releases/download/1.3.3/clickhouse.metabase-driver.jar
```

metabase
```
admin@admin.admin
metabase_pass1
http://localhost:3000/public/dashboard/6d2cbb29-e310-4c80-ac3d-b8903d92efaf
```

### Local

todo docker compose desc

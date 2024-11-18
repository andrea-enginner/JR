#!/usr/bin/bash

sudo docker compose up -d --scale pgadmin=0 --scale web=0 --scale projetosd_db=1

sudo docker exec -it postgres psql -U postgres -c  "DROP DATABASE projetosd"
sudo docker exec -it postgres psql -U postgres -c  "DROP USER projetosd"
sudo docker exec -it postgres psql -U postgres -c  "CREATE DATABASE projetosd"
sudo docker exec -it postgres psql -U postgres -c  "CREATE USER projetosd WITH PASSWORD 'antonio'" # verificar passord em /infra/secrets/pgapp_pass
sudo docker exec -it postgres psql -U postgres -c  "GRANT ALL PRIVILEGES ON DATABASE projetosd to projetosd"
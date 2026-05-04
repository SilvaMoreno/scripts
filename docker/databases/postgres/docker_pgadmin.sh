sudo docker run --name my-pgadmin --network=postgres-network -p 8888:80 -e "PGADMIN_DEFAULT_EMAIL=pgadmin@pgadmin.com" -e "PGADMIN_DEFAULT_PASSWORD=pgadmin" -d dpage/pgadmin4


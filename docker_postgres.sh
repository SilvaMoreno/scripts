sudo docker run --name my-postgres --network=postgres-network -e "POSTGRES_PASSWORD=postgres" -p 5432:5432 -v /home/silva/Documents/dbs/postgres:/var/lib/postgresql/data -d postgres


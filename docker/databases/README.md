# Database Containers

Docker configurations for database services.

## Available Databases

### PostgreSQL
**Location**: `postgres/`

Sets up PostgreSQL with optional pgAdmin interface.

**Quick Start**:
```bash
cd postgres
./docker_pgadmin.sh  # Starts pgAdmin on port 8888
```

**Default Credentials**:
- pgAdmin: pgadmin@pgadmin.com / pgadmin
- PostgreSQL: postgres / postgres

**Volumes**: Data stored in `/home/silva/Documents/dbs/postgres`

### MySQL
**Location**: Root directory (`../docker_containers.sh`)

```bash
cd ..
./docker_containers.sh  # Starts both Postgres and MySQL
```

**Default Credentials**:
- Root password: root
- Port: 3306

### Redis
**Setup**: Create network first, then run container

```bash
docker network create --driver bridge redis-network

docker run --name my-redis \
  --network=redis-network \
  -p 6379:6379 \
  -d redis
```

**Port**: 6379

## Common Operations

```bash
# Access PostgreSQL shell
docker exec -it my-postgres psql -U postgres

# Access MySQL shell
docker exec -it my-mysql mysql -u root -p

# Redis CLI
docker exec -it my-redis redis-cli

# View logs
docker logs my-postgres
docker logs my-mysql
docker logs my-redis
```

## Network

All databases use dedicated Docker networks for isolation:
- `postgres-network` for PostgreSQL and pgAdmin
- `redis-network` for Redis

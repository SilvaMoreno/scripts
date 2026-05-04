# MySQL Database Container

MySQL database setup using Docker.

## Quick Start

The MySQL container is included in the main database script at `../docker_containers.sh`.

### Run MySQL

```bash
cd ..
./docker_containers.sh
```

This will start both PostgreSQL and MySQL containers.

### Manual Start

```bash
docker run --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -p 3306:3306 \
  -d mysql
```

## Configuration

- **Image**: `mysql:latest`
- **Port**: 3306 (host) → 3306 (container)
- **Root Password**: `root` (change in script)
- **Container Name**: `my-mysql`

## Usage

### Access MySQL Shell

```bash
docker exec -it my-mysql mysql -u root -p
# Enter password: root
```

### Create Database

```bash
docker exec -it my-mysql mysql -u root -p -e "CREATE DATABASE mydb;"
```

### Backup Database

```bash
docker exec my-mysql mysqldump -u root -p mydb > backup.sql
```

### Restore Database

```bash
docker exec -i my-mysql mysql -u root -p mydb < backup.sql
```

## Environment Variables

Customize by editing the run command:

```bash
docker run --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=secure_password \
  -e MYSQL_DATABASE=mydb \
  -e MYSQL_USER=myuser \
  -e MYSQL_PASSWORD=mypassword \
  -p 3306:3306 \
  -v /path/to/mysql/data:/var/lib/mysql \
  -d mysql
```

## Notes

- No docker-compose.yml (uses simple docker run)
- Consider adding one for persistent configurations
- Data is lost when container is removed (unless using volumes)

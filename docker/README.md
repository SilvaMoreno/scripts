# Docker Configurations

Docker Compose files and container setup scripts for various services.

## Directory Structure

- **databases/** - Database containers (PostgreSQL, MySQL, Redis)
- **dns/** - DNS services (Pi-hole)
- **vpn/** - VPN configurations (WireGuard)
- **web/** - Web servers (Apache)

## Common Commands

```bash
# Start a service
cd <service-directory>
docker-compose up -d

# Stop a service
docker-compose down

# View logs
docker-compose logs -f

# Validate compose file
docker-compose config
```

## Network Setup

Some services require custom Docker networks:

```bash
# Create postgres network
docker network create --driver bridge postgres-network

# Create redis network
docker network create --driver bridge redis-network
```

## Notes

- Replace `PUBLIC_IP` and password placeholders before deploying
- Use relative paths for volumes (`./config`) for portability
- Services use `restart: unless-stopped` for persistence

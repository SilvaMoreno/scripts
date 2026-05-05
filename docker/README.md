# Docker Configurations

Docker Compose files and container setup scripts for various services.

## Directory Structure

- **reverse-proxy/** - Reverse proxy with SSL/TLS (Traefik 2.11)
  - **traefik/** - Standalone Traefik for automatic Let's Encrypt certificates
- **nextcloud/** - Nextcloud stack (Production ready)
  - Nextcloud + PostgreSQL + Redis with Traefik integration
- **databases/** - Database containers (PostgreSQL, MySQL, Redis)
- **dns/** - DNS services (Pi-hole)
- **vpn/** - VPN configurations (WireGuard)
- **web/** - Web servers (Apache)

## Production Stack (Recommended Order)

### 1. Deploy Traefik Reverse Proxy First

```bash
cd reverse-proxy/traefik
cp .env.example .env
# Edit .env with your email and dashboard password
docker network create proxy
touch acme.json && chmod 600 acme.json
docker-compose up -d
```

### 2. Deploy Nextcloud Stack

```bash
cd nextcloud
cp .env.example .env
# Edit .env with secure passwords
docker-compose up -d
# Access https://cloud.example.com
```

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

# Restart a service
docker-compose restart <service-name>
```

## Network Setup

Some services require custom Docker networks:

```bash
# Create proxy network (for Traefik)
docker network create proxy

# Create postgres network
docker network create --driver bridge postgres-network

# Create redis network
docker network create --driver bridge redis-network
```

## Notes

- Replace `PUBLIC_IP`, domain names, and password placeholders before deploying
- Use relative paths for volumes (`./config`) for portability
- Services use `restart: unless-stopped` for persistence
- Sensitive files (`.env`, `acme.json`) are gitignored
- Traefik automatically manages SSL certificates via Let's Encrypt


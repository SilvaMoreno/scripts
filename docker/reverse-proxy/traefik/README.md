# Traefik 2.11 Reverse Proxy

Standalone Traefik reverse proxy for production VPS deployments. Manages SSL/TLS certificates automatically via Let's Encrypt and routes traffic to Docker services.

## Overview

- **Image**: `traefik:v2.11`
- **Purpose**: Global reverse proxy for all Docker services
- **Features**: Automatic SSL, HTTP→HTTPS redirect, Docker service discovery
- **Dashboard**: Available at `traefik.example.com` (protected with basic auth)
- **Configuration**: Using command-line arguments (no traefik.yml needed)

## Prerequisites

- Docker and Docker Compose installed
- Domain pointing to your VPS (e.g., `traefik.example.com`, `cloud.example.com`)
- Ports 80 and 443 available

## Quick Start

### 1. Create External Network

```bash
docker network create proxy
```

### 2. Configure Environment

```bash
cd docker/reverse-proxy/traefik
cp .env.example .env
```

Edit `.env` and set:
- `TRAEFIK_EMAIL` - Your email for Let's Encrypt
- `TRAEFIK_DASHBOARD_PASSWORD` - Generate with:

  ```bash
  # Generate bcrypt password hash
  htpasswd -nb admin yourpassword
  # Output: admin:$apr1$abc123$hash
  
  # Escape $ as $$ for .env file
  # In .env, write: admin:$$apr1$$abc123$$hash
  ```

  **Important**: Docker Compose interprets `$` as variable reference. You must escape each `$` as `$$` in the `.env` file.

### 3. Initialize ACME File

```bash
touch acme.json
chmod 600 acme.json
```

### 4. Deploy Traefik

```bash
docker-compose up -d
```

### 5. Verify

- Dashboard: https://traefik.example.com
- Logs: `docker logs traefik`

## How It Works

1. **Entry Points**: 
   - `web` (port 80) redirects all HTTP to HTTPS
   - `websecure` (port 443) handles HTTPS with automatic TLS

2. **Service Discovery**: Traefik watches Docker socket and automatically configures routes based on container labels

3. **Certificate Management**: Let's Encrypt HTTP challenge automatically provisions SSL certs

## Adding Services

To expose a service through Traefik, add these labels to the service's docker-compose.yml:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.servicename.rule=Host(`service.example.com`)"
  - "traefik.http.routers.servicename.entrypoints=websecure"
  - "traefik.http.routers.servicename.tls.certresolver=letsencrypt"
  - "traefik.http.services.servicename.loadbalancer.server.port=8080"  # Internal port
```

And ensure the service is on the `proxy` network:

```yaml
networks:
  - proxy
```

## Useful Commands

```bash
# View logs
docker logs -f traefik

# Check certificate status
docker exec traefik cat acme.json

# Reload configuration (if using file providers)
docker kill -s USR1 traefik

# Stop Traefik
docker-compose down
```

## Security Notes

- `acme.json` must have `600` permissions (created automatically by setup)
- `.env` file is gitignored - never commit secrets
- Dashboard is protected with basic auth
- `no-new-privileges` security opt is set
- Only services with `traefik.enable=true` are exposed (not all containers)

## Troubleshooting

### Certificate Issues
```bash
# Check Traefik logs for ACME errors
docker logs traefik | grep acme

# Verify domain DNS points to your VPS
dig +short yourdomain.com
```

### Dashboard Not Accessible
- Verify `traefik.example.com` DNS
- Check basic auth password format in `.env`
- Ensure ports 80/443 are open in firewall

### Service Not Routed
- Confirm service has `traefik.enable=true` label
- Verify service is on `proxy` network
- Check `traefik.http.services.*.loadbalancer.server.port` matches container port

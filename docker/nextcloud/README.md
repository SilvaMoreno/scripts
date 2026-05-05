# Nextcloud with PostgreSQL and Redis

Production-ready Nextcloud deployment with Traefik 2.11 reverse proxy, PostgreSQL database, and Redis caching.

## Overview

- **Nextcloud**: `nextcloud:28-apache` - Main application
- **PostgreSQL**: `postgres:16-alpine` - Database (more robust than MySQL for Nextcloud)
- **Redis**: `redis:7-alpine` - Cache backend + file locking
- **Traefik**: Handles SSL/TLS via Let's Encrypt automatically

## Prerequisites

- Traefik deployed and running (see `../reverse-proxy/traefik/`)
- Domain `cloud.example.com` pointing to your VPS
- External Docker network `proxy` created
- Secure passwords ready

## Quick Start

### 1. Configure Environment

```bash
cd docker/nextcloud
cp .env.example .env
```

Edit `.env` and set:
- `POSTGRES_PASSWORD` - Secure database password
- `REDIS_PASSWORD` - Secure Redis password
- `NEXTCLOUD_ADMIN_PASSWORD` - Admin account password
- `NEXTCLOUD_TRUSTED_DOMAINS` - Your domain (e.g., `cloud.example.com`)

### 2. Deploy Stack

```bash
docker-compose up -d
```

### 3. Complete Installation

Wait 30-60 seconds for containers to start, then access:
```
https://cloud.example.com
```

If you set `NEXTCLOUD_ADMIN_USER` and `NEXTCLOUD_ADMIN_PASSWORD` in `.env`, the installation completes automatically. Otherwise, use the web interface.

### 4. Configure Redis (Post-Install)

Edit `config/config.php` inside the Nextcloud container or mount a custom config:

```bash
docker exec -it nextcloud bash
cd /var/www/html
sudo -u www-data php occ config:system:set memcache.local --value='\OC\Memcache\APCu'
sudo -u www-data php occ config:system:set memcache.distributed --value='\OC\Memcache\Redis'
sudo -u www-data php occ config:system:set memcache.locking --value='\OC\Memcache\Redis'
```

Or use the provided `config/config.sample.php` template.

### 5. Traefik Middlewares (Already Configured)

The docker-compose.yml includes necessary Traefik middlewares:

- **nextcloud-dedupe**: Removes trailing slashes from URLs
- **nextcloud-caldav**: Redirects `.well-known/carddav` and `.well-known/caldav` to Nextcloud's DAV endpoint (fixes CalDAV/CardDAV errors)

If you see "middleware does not exist" errors in Traefik, ensure these labels are present in the docker-compose.yml under the `nextcloud` service.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Traefik   │────▶│ Nextcloud   │────▶│ PostgreSQL  │
│   :80/443   │     │   :80       │     │   :5432     │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           └────────────▶│   Redis     │
                                        │   :6379     │
                                        └─────────────┘

Networks:
- proxy (external): Traefik ↔ Nextcloud
- internal (internal): Nextcloud ↔ PostgreSQL, Redis
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | nextcloud | Database user |
| `POSTGRES_PASSWORD` | - | **Required** - Database password |
| `REDIS_PASSWORD` | - | **Required** - Redis password |
| `NEXTCLOUD_ADMIN_USER` | admin | Admin username |
| `NEXTCLOUD_ADMIN_PASSWORD` | - | **Required** - Admin password |
| `NEXTCLOUD_TRUSTED_DOMAINS` | cloud.example.com | Trusted domain(s) |

## Useful Commands

```bash
# View logs
docker logs -f nextcloud
docker logs -f nextcloud-db
docker logs -f nextcloud-redis

# Nextcloud occ commands (maintenance)
docker exec -u www-data nextcloud php occ maintenance:mode --on
docker exec -u www-data nextcloud php occ maintenance:mode --off

# Backup database
docker exec nextcloud-db pg_dump -U nextcloud nextcloud > backup_$(date +%Y%m%d).sql

# Restart stack
docker-compose restart

# Update Nextcloud
docker-compose pull
docker-compose up -d
```

## Performance Optimization

### APCu and Redis
Already configured via environment + config.php:
- **APCu**: Local cache (in-memory)
- **Redis**: Distributed cache + file locking

### PHP Configuration
For better performance, adjust PHP settings:
```bash
docker exec -it nextcloud bash
echo "memory_limit=512M" >> /usr/local/etc/php/conf.d/nextcloud.ini
echo "upload_max_filesize=10G" >> /usr/local/etc/php/conf.d/nextcloud.ini
echo "post_max_size=10G" >> /usr/local/etc/php/conf.d/nextcloud.ini
```

## Security Notes

- Database and Redis are on an `internal` network (not exposed to host)
- Only Nextcloud is exposed via Traefik on the `proxy` network
- All passwords stored in `.env` (gitignored)
- Automatic SSL/TLS via Let's Encrypt
- HTTP automatically redirects to HTTPS

## Troubleshooting

### Installation Fails
```bash
# Check container health
docker ps
docker logs nextcloud

# Verify database connection
docker exec nextcloud-db pg_isready -U nextcloud
```

### 502 Bad Gateway
- Wait longer (first start takes 30-60s)
- Check Traefik logs: `docker logs traefik`
- Verify Nextcloud is on `proxy` network

### Redis Connection Error
- Check Redis password in `config.php` matches `.env`
- Verify Redis health: `docker exec nextcloud-redis redis-cli -a password ping`

### "Trusted Domain" Error
Add your domain to `.env`:
```
NEXTCLOUD_TRUSTED_DOMAINS=cloud.example.com
```
Then restart: `docker-compose restart nextcloud`

## Maintenance

### Backup
```bash
# Stop containers
docker-compose stop

# Backup volumes
tar -czf nextcloud-backup-$(date +%Y%m%d).tar.gz data/ config/

# Backup database
docker exec nextcloud-db pg_dump -U nextcloud nextcloud > db-backup-$(date +%Y%m%d).sql

# Restart
docker-compose start
```

### Update
```bash
docker-compose pull
docker-compose up -d
docker exec -u www-data nextcloud php occ upgrade
```

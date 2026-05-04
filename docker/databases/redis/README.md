# Redis Container

Redis in-memory data structure store setup using Docker.

## Quick Start

### Create Network (First Time)

```bash
docker network create --driver bridge redis-network
```

### Run Redis

```bash
docker run --name my-redis \
  --network=redis-network \
  -p 6379:6379 \
  -d redis
```

## Configuration

- **Image**: `redis:latest`
- **Port**: 6379 (host) → 6379 (container)
- **Container Name**: `my-redis`
- **Network**: `redis-network`

## Usage

### Redis CLI

```bash
docker exec -it my-redis redis-cli
```

### Test Connection

```bash
docker exec my-redis redis-cli ping
# Output: PONG
```

### Set/Get Key

```bash
docker exec my-redis redis-cli SET mykey "Hello Redis"
docker exec my-redis redis-cli GET mykey
```

### Monitor Commands

```bash
docker exec -it my-redis redis-cli MONITOR
```

## Persistence

To persist data, add a volume:

```bash
docker run --name my-redis \
  --network=redis-network \
  -p 6379:6379 \
  -v /path/to/redis/data:/data \
  -d redis redis-server --appendonly yes
```

## Custom Configuration

Create a custom `redis.conf` and mount it:

```bash
docker run --name my-redis \
  -p 6379:6379 \
  -v ./redis.conf:/usr/local/etc/redis/redis.conf \
  -d redis redis-server /usr/local/etc/redis/redis.conf
```

## Notes

- No docker-compose.yml (uses simple docker run)
- Default configuration is suitable for development
- For production, configure persistence and security

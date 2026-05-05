# AGENTS.md - Developer Scripts Repository

This repository contains a collection of developer scripts for Linux environments, including Docker configurations, VPN management tools, and utility scripts.

## Project Structure

```
.
├── docker/                    # Docker configurations
│   ├── databases/            # Database containers
│   │   ├── postgres/        # PostgreSQL + pgAdmin
│   │   ├── mysql/           # MySQL setup
│   │   └── redis/           # Redis setup
│   ├── dns/                 # DNS services
│   │   └── pihole/         # Pi-hole ad blocker
│   ├── vpn/                 # VPN configurations
│   │   └── wireguard/      # WireGuard VPN server
│   └── web/                 # Web servers
│       └── apache/          # Apache + PHP
├── scripts/                  # Utility shell scripts
│   └── setup/              # Environment setup scripts
├── tools/                    # Standalone tools
│   └── vpn-tray/           # VPN system tray app
├── docs/                     # Documentation
└── AGENTS.md                # This file
```

### Key Files
- `docker/reverse-proxy/traefik/docker-compose.yml` - Traefik 2.11 reverse proxy
- `docker/nextcloud/docker-compose.yml` - Nextcloud + PostgreSQL + Redis stack
- `docker/databases/docker_containers.sh` - Main database container setup
- `docker/vpn/wireguard/docker-compose.yml` - WireGuard VPN server
- `tools/vpn-tray/vpn_tray.py` - VPN tray application
- `docker/dns/pihole/docker-compose.yml` - Pi-hole DNS blocker

## Build/Lint/Test Commands

This repository contains scripts and configuration files rather than a traditional software project. There are no build, lint, or test commands configured.

### Running Scripts
```bash
# Make shell scripts executable if needed
chmod +x docker_containers.sh docker_pgadmin.sh

# Run Docker setup scripts
./docker_containers.sh
./docker_pgadmin.sh

# Run Python VPN tray application
cd WireGuard && python3 vpn_tray.py
```

### Docker Compose
```bash
# Start services
cd WireGuard && docker-compose up -d
cd Pihole && docker-compose up -d

# Stop services
docker-compose down
```

### Manual Testing
Since there are no automated tests, verify scripts manually:
- Check shell scripts for syntax: `bash -n script.sh`
- Validate Docker Compose files: `docker-compose config`
- Test Python syntax: `python3 -m py_compile WireGuard/vpn_tray.py`

## Code Style Guidelines

### Shell Scripts

- **Shebang**: Start with `#!/bin/bash` (currently missing from existing scripts)
- **Comments**: Use `#` for comments, not `//` (see `docker_containers.sh`)
- **Variables**: Use uppercase for environment variables, lowercase for local variables
- **Quoting**: Quote variable expansions: `"$variable"` not `$variable`
- **Sudo**: Use `sudo` only when necessary; document why it's needed
- **Line length**: Keep lines under 120 characters when possible

Example:
```bash
#!/bin/bash
# Postgres container setup
POSTGRES_PASSWORD="postgres"
POSTGRES_DATA_DIR="/home/silva/Documents/dbs/postgres"

docker run --name my-postgres \
  --network=postgres-network \
  -e "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" \
  -p 5432:5432 \
  -v "${POSTGRES_DATA_DIR}:/var/lib/postgresql/data" \
  -d postgres
```

### Python (WireGuard/vpn_tray.py)

- **Python version**: Use Python 3 syntax
- **Imports**: Group imports in order: standard library, third-party, local
  ```python
  import os
  import sys
  from pystray import Icon, Menu, MenuItem
  from PIL import Image, ImageDraw
  import subprocess
  ```
- **Naming conventions**:
  - Functions/variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Classes: `PascalCase`
- **Docstrings**: Use triple quotes for function documentation
- **Error handling**: Use try/except blocks with specific exceptions
- **Line length**: Maximum 88-100 characters (PEP 8 style)
- **String formatting**: Use f-strings for modern Python

### Docker Compose Files

- **Version**: Specify version at top (`version: '3.8'` or `version: "3"`)
- **Indentation**: Use 2 spaces (consistent across files)
- **Environment variables**: Use uppercase with clear comments
- **Volume paths**: Use relative paths (`./config`) for portability
- **Networks**: Define custom networks when services need to communicate
- **Restart policy**: Use `restart: unless-stopped` for persistent services

Example:
```yaml
version: '3.8'
services:
  service_name:
    image: repository/image:tag
    container_name: service_name
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
    volumes:
      - ./config:/config
    ports:
      - 51820:51820/udp
    restart: unless-stopped
```

### Documentation (Markdown)

- **README**: Keep README.md updated with new scripts and configurations
- **Headers**: Use ATX-style headers (`## Header`)
- **Code blocks**: Specify language for syntax highlighting (`bash`, `yaml`, `python`)
- **Links**: Use relative links for internal docs, absolute for external

## Error Handling Patterns

### Shell Scripts
```bash
if ! docker run ...; then
    echo "Failed to start container" >&2
    exit 1
fi
```

### Python
```python
try:
    output = subprocess.check_output(["nmcli", "connection", "show"], text=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed: {e}")
    return False
```

## Security Considerations

- **Secrets**: Never commit passwords; use environment variables or `.env` files (add to `.gitignore`)
- **Privileges**: Minimize use of `sudo` and `cap_add` in Docker; document why needed
- **Public IPs**: Replace `PUBLIC_IP` placeholders before committing
- **Permissions**: Ensure scripts are executable (`chmod +x`)

## Git Workflow

- **Branch**: Work on feature branches, merge to master
- **Commit messages**: Use imperative mood ("Add WireGuard tray app" not "Added...")
- **Pre-commit**: No hooks configured; verify changes manually before committing

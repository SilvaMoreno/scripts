# Dev Scripts Repository

Collection of utility scripts for developers using Linux environments.

## Structure

```
.
├── docker/                    # Docker configurations
│   ├── reverse-proxy/        # Reverse proxy (Traefik 2.11)
│   │   └── traefik/        # Traefik for SSL/TLS termination
│   ├── nextcloud/           # Nextcloud stack (Prod ready)
│   │   ├── config/         # Custom Nextcloud config
│   │   └── data/           # Nextcloud data volume
│   ├── databases/           # Database containers
│   │   ├── postgres/       # PostgreSQL + pgAdmin
│   │   ├── mysql/          # MySQL setup
│   │   └── redis/          # Redis setup
│   ├── dns/                 # DNS-related containers
│   │   └── pihole/        # Pi-hole ad blocker
│   ├── vpn/                 # VPN configurations
│   │   └── wireguard/     # WireGuard VPN server
│   └── web/                 # Web server containers
│       └── apache/         # Apache web server
├── scripts/                  # Utility shell scripts
│   └── setup/              # Environment setup scripts
├── tools/                    # Standalone tools
│   └── vpn-tray/           # VPN system tray application
├── docs/                     # Documentation
│   ├── git.md              # Git-related notes
│   ├── linux.md            # Linux tips
│   └── xdebug_lampp_vscode.md  # Xdebug + VSCode + LAMPP
└── AGENTS.md                # Guidelines for AI agents
```

## Quick Start

### Prerequisites
- Linux environment (VPS for production services)
- Docker and Docker Compose installed
- Python 3.x (for tools)
- Domain pointing to your VPS (for Traefik/Nextcloud)

### Deploy Traefik Reverse Proxy (First)

```bash
cd docker/reverse-proxy/traefik
cp .env.example .env
# Edit .env with your email and dashboard password
docker network create proxy
touch acme.json && chmod 600 acme.json
docker-compose up -d
```

### Deploy Nextcloud Stack

```bash
cd docker/nextcloud
cp .env.example .env
# Edit .env with secure passwords
docker-compose up -d
# Access https://cloud.example.com to complete setup
```

### Other Docker Containers

```bash
# Make scripts executable
chmod +x docker/databases/docker_containers.sh
chmod +x docker/databases/postgres/docker_pgadmin.sh

# Run database containers
cd docker/databases
./docker_containers.sh

# Run pgAdmin
cd postgres && ./docker_pgadmin.sh
```

### VPN Tray Tool

```bash
cd tools/vpn-tray
pip install pystray pillow
python3 vpn_tray.py
```

## Documentation

Each directory contains its own README.md with specific instructions:

- [Docker Overview](docker/README.md)
- [Database Containers](docker/databases/README.md)
- [WireGuard VPN](docker/vpn/wireguard/README.md)
- [Pi-hole DNS](docker/dns/pihole/README.md)
- [VPN Tray Tool](tools/vpn-tray/README.md)

## Contributing

1. Create feature branch
2. Add scripts with proper documentation
3. Update relevant README files
4. Follow code style guidelines in [AGENTS.md](AGENTS.md)

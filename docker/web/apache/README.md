# Apache Web Server

Apache HTTP Server with PHP support via Docker.

## Overview

Quick setup for Apache web server with PHP, useful for local development and testing.

## Quick Start

```bash
docker run -d -p 80:80 --name my-apache -v "$PWD":/var/www/html php:7.2-apache
```

## Configuration

- **Image**: `php:7.2-apache`
- **Port**: 80 (host) → 80 (container)
- **Volume**: Current directory mounted to `/var/www/html`
- **Container Name**: `my-apache`

## Usage

1. Place your PHP files in the current directory
2. Access via http://localhost
3. All files are synced live through the volume mount

## PHP Version Options

### PHP 7.2 (Default)
```bash
docker run -d -p 80:80 --name my-apache -v "$PWD":/var/www/html php:7.2-apache
```

### PHP 8.0
```bash
docker run -d -p 80:80 --name my-apache -v "$PWD":/var/www/html php:8.0-apache
```

### PHP 8.2
```bash
docker run -d -p 80:80 --name my-apache -v "$PWD":/var/www/html php:8.2-apache
```

## Custom Configuration

### Different Document Root

```bash
docker run -d -p 80:80 --name my-apache \
  -v /path/to/your/app:/var/www/html \
  php:7.2-apache
```

### Custom php.ini

```bash
docker run -d -p 80:80 --name my-apache \
  -v "$PWD":/var/www/html \
  -v ./php.ini:/usr/local/etc/php/php.ini \
  php:7.2-apache
```

## Useful Commands

```bash
# Access container shell
docker exec -it my-apache bash

# View logs
docker logs my-apache

# Restart Apache
docker exec my-apache apachectl restart

# Check PHP version
docker exec my-apache php -v

# Install PHP extensions
docker exec my-apache docker-php-ext-install pdo pdo_mysql
```

## Notes

- No docker-compose.yml provided (single command setup)
- For production, use official Apache image with proper configuration
- Consider creating a docker-compose.yml for complex setups
- Data persists only through volume mounts

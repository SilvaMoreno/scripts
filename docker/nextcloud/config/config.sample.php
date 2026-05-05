<?php
$CONFIG = array (
  // Redis configuration for caching and file locking
  'memcache.local' => '\\OC\\Memcache\\APCu',
  'memcache.distributed' => '\\OC\\Memcache\\Redis',
  'memcache.locking' => '\\OC\\Memcache\\Redis',
  'redis' => array (
    'host' => 'redis',
    'port' => 6379,
    'password' => getenv('REDIS_HOST_PASSWORD') ?: 'your_redis_password',
    'dbindex' => 0,
    'timeout' => 1.5,
  ),

  // Trusted proxies (Traefik)
  'trusted_proxies' => ['172.16.0.0/12', '10.0.0.0/8'],

  // Overwrite settings for Traefik
  'overwritehost' => 'cloud.example.com',
  'overwriteprotocol' => 'https',
  'overwritewebroot' => '',

  // File handling
  'filesystem_check_changes' => 0,

  // Logging
  'loglevel' => 2,
  'log_type' => 'file',
);

# Setup Scripts

Utility shell scripts for environment setup and configuration.

## Purpose

This directory contains scripts that help set up development environments, configure tools, or automate initial system configuration.

## Adding New Scripts

When adding a setup script:

1. Use `#!/bin/bash` shebang
2. Add descriptive comments explaining what the script does
3. Quote all variable expansions
4. Add error handling where appropriate
5. Document usage in this README

## Current Scripts

_No scripts yet. Add your setup scripts here._

## Template

```bash
#!/bin/bash
# Script: example_setup.sh
# Description: Brief description of what this script does
# Usage: ./example_setup.sh [arguments]

set -e  # Exit on error

# Your script here

echo "Setup completed successfully!"
```

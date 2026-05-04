# VPN Tray Application

Python system tray application for managing WireGuard VPN connections.

## Description

A lightweight system tray tool that provides:
- Visual indication of VPN connection status (icon changes)
- One-click VPN toggle (connect/disconnect)
- Automatic status detection using NetworkManager

## Requirements

```bash
pip install pystray pillow
```

System dependencies:
- Python 3.x
- NetworkManager (`nmcli`)
- System tray support (GTK/X11/Wayland)

## Installation

```bash
cd tools/vpn-tray
pip install -r requirements.txt  # If available
```

Or install manually:
```bash
pip install pystray pillow
```

## Usage

```bash
python3 vpn_tray.py
```

The tray icon will appear showing current VPN status:
- **Connected**: Green/active icon (`connected.png`)
- **Disconnected**: Gray/inactive icon (`disconnected.png`)

Right-click the tray icon for options:
- **Toggle VPN**: Connect or disconnect
- **Quit**: Exit the application

## Configuration

Edit `vpn_tray.py` to change:
```python
VPN_CONNECTION_NAME = "wg0"  # Change if your connection has different name
```

## How It Works

1. **Status Check**: Runs `nmcli connection show --active` to detect VPN
2. **Toggle Action**: Uses `nmcli connection up/down <name>` to control VPN
3. **Icon Update**: Loads appropriate PNG based on connection state
4. **Event Loop**: Runs continuously in system tray

## Files

- `vpn_tray.py` - Main application script
- `connected.png` - Icon for active VPN connection
- `disconnected.png` - Icon for inactive VPN connection

## Troubleshooting

### VPN connection not detected
- Verify connection name: `nmcli connection show`
- Update `VPN_CONNECTION_NAME` in script

### Icon not showing
- Ensure system tray is available
- Check if pystray is installed correctly

### Permission denied
- May need to run with appropriate user permissions
- VPN control typically doesn't require sudo

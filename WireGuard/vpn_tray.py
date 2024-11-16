import os
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import subprocess

VPN_CONNECTION_NAME = "wg0"  # WireGuard connection name in Network Manager

def load_image(filename):
    """Load an image file and return an icon-compatible image."""
    width = 64
    height = 64
    image = Image.open(filename)
    return image.resize((width, height), Image.ANTIALIAS)

def is_vpn_connected():
    """Checks if the VPN is connected."""
    try:
        output = subprocess.check_output(
            ["nmcli", "connection", "show", "--active"], text=True
        )
        return VPN_CONNECTION_NAME in output
    except subprocess.CalledProcessError:
        return False

def toggle_vpn(icon):
    """Enable or disable the VPN."""
    if is_vpn_connected():
        os.system(f"nmcli connection down {VPN_CONNECTION_NAME}")
    else:
        os.system(f"nmcli connection up {VPN_CONNECTION_NAME}")
    update_icon(icon)

def update_icon(icon):
    """Update the tray icon based on VPN status."""
    icon.icon = load_image("connected.png" if is_vpn_connected() else "disconnected.png")

def quit_app(icon, item):
    """Quit the application."""
    icon.stop()

# Define the menu for the tray application
menu = Menu(
    MenuItem("Toggle VPN", toggle_vpn),
    MenuItem("Quit", quit_app)
)

# Initialize and run the tray icon
icon = Icon("VPN Tray",  load_image("disconnected.png"), menu=menu)

# Update the icon to reflect the current VPN status
update_icon(icon)

# Run the application
icon.run()


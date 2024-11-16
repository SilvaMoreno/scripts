# **WireGuard VPN Server with Docker**

This guide provides a complete walkthrough to set up a **WireGuard VPN Server** on a VPS using Docker, add new clients, configure the VPN on Android and Linux, and create a tray application for Linux to manage the VPN connection.

---

## **1. Setting Up the WireGuard Server**

### **1.1 Prerequisites**

-   A VPS with a public IP.
-   Docker and Docker Compose installed on your VPS.

Install Docker and Docker Compose:

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
```

### **1.2 Docker Compose File**

Create a `docker-compose.yml` file with the following content:

```yaml
version: "3.8"
services:
    wireguard:
        image: lscr.io/linuxserver/wireguard:latest
        container_name: wireguard
        cap_add:
            - NET_ADMIN
            - SYS_MODULE
        environment:
            - PUID=1000 # User ID
            - PGID=1000 # Group ID
            - TZ=Europe/London # Replace with your timezone
            - SERVERURL=your-public-ip-or-domain # Public IP or domain
            - SERVERPORT=51820 # VPN Port
            - PEERS=2 # Number of client devices to configure
            - PEERDNS=auto # Use internal or custom DNS (e.g., 1.1.1.1)
            - INTERNAL_SUBNET=10.13.13.0 # VPN Subnet
        volumes:
            - ./config:/config # Path for server and client configuration files
            - /lib/modules:/lib/modules
        ports:
            - 51820:51820/udp # Port for WireGuard
        sysctls:
            - net.ipv4.conf.all.src_valid_mark=1
        restart: unless-stopped
```

### **1.3 Start the WireGuard Server**

1. Run the following commands:
    ```bash
    mkdir wireguard && cd wireguard
    nano docker-compose.yml  # Paste the file contents above
    ```
2. Start the server:
    ```bash
    docker-compose up -d
    ```
3. Check the status:
    ```bash
    docker logs wireguard
    ```

---

## **2. Adding New Clients**

1. Stop the container:
    ```bash
    docker-compose down
    ```
2. Increase the `PEERS` value in the `docker-compose.yml` file.
3. Restart the container to regenerate client configurations:
    ```bash
    docker-compose up -d
    ```
4. Client configuration files (`peer1.conf`, `peer2.conf`, etc.) will be available in the `config/peer_configs` directory.

---

## **3. Configuring WireGuard Clients**

### **3.1 Android**

1. Download the WireGuard app from the [Play Store](https://play.google.com/store/apps/details?id=com.wireguard.android).
2. Access the `peerX.conf` file for the client you wish to connect.
3. Generate a QR Code on your VPS:
    ```bash
    sudo apt install qrencode
    qrencode -t ansiutf8 < ./config/peer2/peer2.conf
    ```
4. Scan the QR Code with the WireGuard app to import the configuration.
5. Connect to the VPN.

---

### **3.2 Linux**

#### **3.2.1 Install WireGuard Tools**

```bash
sudo apt update
sudo apt install wireguard wireguard-tools
```

#### **3.2.2 Configure the Client**

1. Copy the `peerX.conf` file to your Linux machine:
    ```bash
    scp user@your-vps:/path-to-wireguard/config/peer1/peer1.conf .
    ```
2. Rename the configuration file (if needed):
   If the client configuration file is not named `wg0.conf`, rename it:
   ```bash
   mv peer1.conf wg0.conf
   ```
3. Move the configuration file to the directory:
   ```bash
   sudo mv wg0.conf /etc/wireguard
   ```
4. Activate the WireGuard connection:
   ```bash
   sudo wg-quick up wg0
   ```

5. Deactivate the WireGuard connection:
   ```bash
   sudo wg-quick down wg0
   ```

7. Import the configuration to Network Manager:
    ```bash
    sudo nmcli connection import type wireguard file /etc/wireguard/wg0.conf
    ```

#### **3.2.3 Connect to the VPN**

-   Activate the VPN:
    ```bash
    nmcli connection up wg0
    ```
-   Disconnect the VPN:
    ```bash
    nmcli connection down wg0
    ```

---

## **4. Creating a Tray Application on Linux**

### **4.1 Install Dependencies**

```bash
sudo apt install python3 python3-pip
pip install pystray nmcli pillow
```

### **4.2 Create the Tray Application**

Save the following script as `vpn_tray.py`:

```python
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
```

### **4.3 Run the Tray Application**

1. Make the script executable:
    ```bash
    chmod +x vpn_tray.py
    ```
2. Run the script:
    ```bash
    python3 vpn_tray.py
    ```

### **4.4 Optional: Start Tray Application on Boot**

Create a `.desktop` file in `~/.config/autostart/`:

```ini
[Desktop Entry]
Type=Application
Exec=python3 /path/to/vpn_tray.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=VPN Tray
Comment=Manage WireGuard VPN
```

---

## **5. Troubleshooting**

-   **VPN not working:** Check your VPS firewall and ensure port 51820/UDP is open.
-   **DNS issues:** Use a custom DNS like `1.1.1.1` in the `docker-compose.yml`.
-   **Android connection fails:** Ensure the QR Code matches the correct client configuration.

---

With this guide, you now have a fully functional WireGuard VPN server with client configurations and a Linux tray application for convenience! 🎉

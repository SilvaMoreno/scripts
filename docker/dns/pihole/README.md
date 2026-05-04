# **Pi-hole Setup and Configuration Guide**

Pi-hole is a network-wide ad blocker that acts as a DNS sinkhole. It blocks unwanted content like ads and trackers for all devices connected to your network.

This guide will help you set up Pi-hole on a Docker container and configure it for use with WireGuard VPN.

---

## **Prerequisites**
- A **VPS** or local server running Linux (Ubuntu/Debian).
- **Docker** and **Docker Compose** installed.
- **Pi-hole Docker image** to run Pi-hole in a container.

---

## **Step 1: Set Up Pi-hole Using Docker Compose**

1. **Create a directory for Pi-hole:**
   ```bash
   mkdir ~/pihole
   cd ~/pihole
   ```

2. **Create a `docker-compose.yml` file in the `~/pihole` directory:**

   Add the following content to the file:
   ```yaml
   version: '3'

   services:
     pihole:
       image: pihole/pihole:latest
       container_name: pihole
       environment:
         - TZ=Europe/London  # Set your timezone
         - WEBPASSWORD=admin_password  # Set the web UI password
         - DNS1=8.8.8.8  # Optional: Set primary DNS server
         - DNS2=8.8.4.4  # Optional: Set secondary DNS server
         - PIHOLE_INTERFACE=eth0  # Interface for Pi-hole to listen on
         - IPv6=FALSE  # Disable IPv6 if not needed
       volumes:
         - ./etc-pihole:/etc/pihole
         - ./etc-dnsmasq.d:/etc/dnsmasq.d
       ports:
         - "80:80"  # Web UI
         - "443:443"  # HTTPS (optional)
         - "53:53/udp"  # DNS queries
         - "53:53/tcp"  # DNS queries
       restart: unless-stopped
       networks:
         - pihole_net

   networks:
     pihole_net:
       driver: bridge
   ```

3. **Start Pi-hole with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

4. **Access Pi-hole Web Interface:**
   Open your browser and navigate to:
   ```
   http://<your-server-ip>/admin
   ```
   Use the password set in the `WEBPASSWORD` environment variable to log in.

---

## **Step 2: Configuring Pi-hole for WireGuard VPN**

To use Pi-hole as your DNS for WireGuard clients, follow these steps:

1. **Update the WireGuard configuration to use Pi-hole as DNS:**
   Edit the `wg0.conf` or other WireGuard client configuration files and set Pi-hole's IP address as the DNS server.

   Example:
   ```ini
   [Interface]
   Address = 10.13.13.2/24
   PrivateKey = <private-key>
   ListenPort = 51820
   DNS = <Pi-hole-server-ip>
   
   [Peer]
   PublicKey = <public-key>
   PresharedKey = <preshared-key
   Endpoint = <server-ip>:51820
   AllowedIPs = 0.0.0.0/0, ::/0
   ```

   Replace `<Pi-hole-server-ip>` with the container name / IP address of the server running Pi-hole (e.g., `pihole`, `192.168.1.2`).

2. **Verify Pi-hole DNS resolution:**
   Once WireGuard clients connect to the VPN, they will route DNS requests through Pi-hole. Check the Pi-hole web interface to confirm that DNS queries from your devices are being logged.

---

## **Step 3: Configuring Pi-hole Settings (Optional)**

You can modify Pi-hole settings from the web interface to enhance your ad-blocking experience:

- **Block Lists:** Add additional block lists in "Adlists" section.
- **Whitelisting/Blacklisting Domains:** You can whitelist or blacklist specific domains to allow or block access to certain websites.
- **Query Logging:** View detailed logs of DNS queries under the "Query Log" section.

---

## **Step 5: Troubleshooting**

1. **Check Docker container status:**
   Ensure the Pi-hole container is running correctly:
   ```bash
   docker ps
   ```

2. **Verify Pi-hole DNS resolution:**
   Test DNS resolution by pinging a domain from a client machine connected to your VPN:
   ```bash
   nslookup example.com <Pi-hole-server-ip>
   ```

3. **Check Pi-hole logs:**
   Check Pi-hole logs for any issues:
   ```bash
   docker logs pihole
   ```

---

## **Additional Notes**

- You can customize Pi-hole’s behavior by modifying the `pihole` container’s environment variables in the `docker-compose.yml` file.
- Make sure your Pi-hole container has access to the internet for downloading block lists and resolving DNS queries.
- To update Pi-hole, simply pull the latest image and restart the container:
   ```bash
   docker-compose pull pihole
   docker-compose restart pihole
   ```

---

This guide should help you set up Pi-hole in Docker and integrate it with your WireGuard VPN for DNS resolution.
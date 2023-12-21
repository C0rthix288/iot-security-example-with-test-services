#!/bin/bash

prompt_for_ports() {
    echo "Enter the port number for the Weather Data Service (leave empty if default):"
    read WEATHER_SERVICE_PORT
    echo "Enter the port number for the Provisioning Service (leave empty if default):"
    read PROVISIONING_SERVICE_PORT
}

create_directories() {
    sudo mkdir -p /opt/gProVision/secrets
}

# Function to generate device ID
generate_device_id() {
    local serial_number=$(cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2)
    local hostname=$(hostname)
    DEVICE_ID="rpi-${serial_number}-${hostname}"
}

# Function to generate salt and salted token
generate_salted_token() {
    local salt=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
    SPECIAL_DEVICE_TOKEN=$(echo -n "${AUTH_TOKEN}${salt}" | sha256sum | cut -d ' ' -f 1)
}

store_device_credentials() {
    echo "DEVICE_ID=${DEVICE_ID}" > /opt/gProVision/secrets/device_credentials
    echo "SPECIAL_DEVICE_TOKEN=${SPECIAL_DEVICE_TOKEN}" >> /opt/gProVision/secrets/device_credentials
}

save_server_url() {
    echo "${CONTROL_PLANE_URL}" > /opt/gProVision/secrets/server_url
}

construct_service_urls() {
    if [ -n "$WEATHER_SERVICE_PORT" ]; then
        WEATHER_SERVICE_URL="${CONTROL_PLANE_URL}:${WEATHER_SERVICE_PORT}"
    else
        WEATHER_SERVICE_URL="${CONTROL_PLANE_URL}"
    fi

    if [ -n "$PROVISIONING_SERVICE_PORT" ]; then
        PROVISIONING_SERVICE_URL="${CONTROL_PLANE_URL}:${PROVISIONING_SERVICE_PORT}"
    else
        PROVISIONING_SERVICE_URL="${CONTROL_PLANE_URL}"
    fi
}

# Function to generate hash of the special device token and register it
register_device_token() {
    local hashed_token=$(echo -n "${SPECIAL_DEVICE_TOKEN}" | sha256sum | cut -d ' ' -f 1)
    local ip_address=$(hostname -I | awk '{print $1}')
    local status="online"

    # POST request to the weather-data-service to register the device token
    curl -s -X POST "${WEATHER_SERVICE_URL}/register_device_token/" \
        -H "Content-Type: application/json" \
        -d "{\"device_id\": \"$DEVICE_ID\", \"ip_address\": \"$ip_address\", \"status\": \"$status\", \"special_device_token_hash\": \"$hashed_token\"}"
}


install_wireguard() {
    echo "Installing WireGuard..."
    sudo apt update
    sudo apt install -y wireguard
    echo "WireGuard installed successfully."
}

install_jq_if_not_present() {
    if ! command -v jq &> /dev/null; then
        echo "jq not found. Installing jq..."
        sudo apt install -y jq
        echo "jq installed successfully."
    fi
}


# Function to generate and register WireGuard keys
register_wireguard_keys() {
    echo "Generating WireGuard keys and registering with Control Plane..."

    # Generate private and public keys
    sudo wg genkey | sudo tee privatekey >/dev/null
    sudo cat privatekey | sudo wg pubkey | sudo tee publickey >/dev/null
    private_key=$(sudo cat privatekey)
    public_key=$(sudo cat publickey)

    # POST request to the provisioning-service to register the WireGuard keys
    response=$(curl -s -X POST "$PROVISIONING_SERVICE_URL/register_device/" \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer $AUTH_TOKEN" \
                -d "{\"device_id\": \"$DEVICE_ID\", \"public_key\": \"$public_key\"}")

    
    server_public_key=$(echo $response | jq -r '.server_public_key')
    server_ip=10.2.10.148
    internal_ip=$(echo $response | jq -r '.internal_ip')

    
    if [ -z "$server_public_key" ] || [ "$server_public_key" = "null" ] || 
       [ -z "$server_ip" ] || [ "$server_ip" = "null" ] ||
       [ -z "$internal_ip" ] || [ "$internal_ip" = "null" ]; then
        echo "Failed to get necessary data from server."
        exit 1
    fi

    
    echo "Creating WireGuard configuration..."
    sudo bash -c "cat > /etc/wireguard/wg0.conf <<EOF
[Interface]
Address = $internal_ip/24
PrivateKey = $private_key
ListenPort = 51820

[Peer]
PublicKey = $server_public_key
AllowedIPs = 0.0.0.0/0
Endpoint = $server_ip:51820
EOF"
}

configure_wg_tunnel() {
    echo "Configuring WireGuard tunnel..."
    sudo wg-quick up wg0
    echo "WireGuard tunnel configured."
}

configure_firewall() {
    echo "Configuring firewall..."
    sudo ufw default deny incoming
    sudo ufw default deny outgoing
    sudo ufw allow 51820/udp comment 'WireGuard port'
    sudo ufw enable
    echo "Firewall configured."
}

BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}  .~~.   .~~.${NC}"
echo -e "${GREEN} '. \ ' ' / .'${NC}"
echo -e "${RED}  .~ .~~~..~.${NC}"
echo -e "${RED} : .~.'~'.~. :${NC}"
echo -e "${RED} ~ (   ) (   ) ~${NC}"
echo -e "${RED}( : '~'.~.'~' : )${NC}"
echo -e "${RED} ~ .~ (   ) ~. ~${NC}"
echo -e "${RED}  (  : '~' :  )${NC}"
echo -e "${RED}   '~ .~~~. ~'${NC}"
echo -e "${RED}       '~'${NC}"


# Main execution
create_directories
echo -e "Starting ${RED}Raspberry${NC} ${GREEN}Pi${NC} setup..."
echo "=============================="
if [ -z "$CONTROL_PLANE_URL" ]; then
    echo -e "${RED}ERROR${NC}: CONTROL_PLANE_URL environment variable not set."
    echo "Please enter the Control Plane URL:"
    read CONTROL_PLANE_URL
fi
save_server_url
echo "=============================="
if [ -z "$AUTH_TOKEN" ]; then
    echo -e "${RED}ERROR${NC}: AUTH_TOKEN environment variable not set."
    echo "Please enter the Auth Token:"
    read AUTH_TOKEN
fi
echo "=============================="
echo -e "Control Plane URL: ${BLUE}$CONTROL_PLANE_URL${NC}"
echo "=============================="
prompt_for_ports
construct_service_urls
echo "Generating special device token..."
generate_salted_token
echo "Generating device ID..."
generate_device_id
echo -e "${GREEN}OK${NC}, device ID generated: ${BLUE}$DEVICE_ID${NC}"
echo "Saving credentials..."
store_device_credentials
echo -e "${GREEN}OK${NC}."
echo "Installing WireGuard..."
install_wireguard
echo -e "${GREEN}OK${NC}, WireGuard installed."
echo "Installing jq..."
install_jq_if_not_present
echo -e "${GREEN}OK${NC}, jq installed."
echo "Registering WireGuard keys..."
register_wireguard_keys
echo -e "${GREEN}OK${NC}, WireGuard keys registered."
echo "Configuring WireGuard tunnel..."
configure_wg_tunnel
echo -e "${GREEN}OK${NC}, WireGuard tunnel configured."
echo "Configuring firewall..."
configure_firewall
echo -e "${GREEN}OK${NC}, firewall configured."
echo "=============================="
echo "Registering device token..."
register_device_token
echo -e "${GREEN}OK${NC}, device token registered."
echo "=============================="
echo -e "${RED}Raspberry${NC} ${GREEN}Pi${NC} setup complete."
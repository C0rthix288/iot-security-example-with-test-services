#!/bin/bash

install_wireguard() {
    echo "Installing WireGuard..."
    sudo apt-get update
    sudo apt-get install -y wireguard wireguard-tools
    echo "WireGuard installed."
}


setup_wireguard_interface() {
    echo "Setting up WireGuard interface wg0..."

    WG_CONF="/etc/wireguard/wg0.conf"


    WG_KEY="/etc/wireguard/privatekey"
    if [[ ! -f "$WG_KEY" ]]; then
        echo "Generating WireGuard private key..."
        sudo wg genkey | sudo tee $WG_KEY >/dev/null
    fi
    WG_PRIVATE_KEY=$(sudo cat $WG_KEY)

    if [[ ! -f "$WG_CONF" ]]; then
        echo "Creating WireGuard configuration file..."
        sudo bash -c "cat > $WG_CONF <<EOF
[Interface]
Address = 10.0.0.1/24
PrivateKey = $WG_PRIVATE_KEY
ListenPort = 51820
EOF"
    else
        echo "WireGuard configuration already exists."
    fi

    sudo wg-quick up wg0
    sudo systemctl enable wg-quick@wg0
    echo "WireGuard interface wg0 is set up and running."
}


generate_public_key() {
    echo "Generating and storing WireGuard public key..."

    WG_PUB_KEY="/etc/wireguard/publickey"
    if [[ ! -f "$WG_PUB_KEY" ]]; then
        sudo cat $WG_KEY | sudo wg pubkey | sudo tee $WG_PUB_KEY >/dev/null
        echo "WireGuard public key generated and stored at $WG_PUB_KEY."
    else
        echo "WireGuard public key already exists at $WG_PUB_KEY."
    fi
}


install_wireguard
setup_wireguard_interface
generate_public_key

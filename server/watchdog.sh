#!/bin/bash

WG_CONF="/etc/wireguard/wg0.conf"
LAST_MD5SUM=""

while true; do
    CURRENT_MD5SUM=$(md5sum $WG_CONF | awk '{print $1}')

    if [ "$LAST_MD5SUM" != "$CURRENT_MD5SUM" ]; then
        echo "Configuration changed. Reloading WireGuard interface..."
        sudo wg-quick down wg0 && sudo wg-quick up wg0
        LAST_MD5SUM=$CURRENT_MD5SUM
    fi

    sleep 60
done

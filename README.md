# iot-security-example-with-test-services

This piece of software is under the WTFPL license.

Project was developed for scholar purposes.
The whole idea was to suggest a solution for securing the IoT systems.

In the project was utilized:
- containerization
- sending traffic over WG tunnel,
- exchanging and hashing tokens

It simulates collecting the weather data on the edge device (Raspberry Pi 4), then sends the data to the weather-data-service which saves it in the database and allows user to view them.

There is a provisioning service which creates a secure connection between edge device and the server.

Overall the wireguard provisioning service and weather data service should be behind reverse-proxy, however it was made purely for lab purposes (doesn't mean it do not work in real-world scenario; it just needs some modifications).

Feel free to do whatever You want with this code.

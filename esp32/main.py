import wifimgr
import socket
import ure
import time
import testuart

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D

import network
import socket
import time


from machine import UART
import time

uart = UART(1, baudrate=115200)

def send_command(cmd, timeout=1000):
    if isinstance(cmd, str):
        cmd = cmd.encode()

    uart.write(cmd)

    start = time.ticks_ms()
    response = b""

    while True:
        try:
            n = uart.any()
            if n:
                data = uart.read(n)
                if data:
                    response += data
        except OSError as e:
            # Ignore timeout errors
            if e.args[0] == 116:  # ETIMEDOUT
                break
            else:
                raise

        if time.ticks_diff(time.ticks_ms(), start) > timeout:
            break

        time.sleep_ms(10)

    return response

# ====== START SERVER ======
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)

print("Server listening...")

testuart.playSound()
while True:
    client, addr = server.accept()
    print("Client connected from", addr)

    request = client.recv(1024)  # We don't even parse it

    response = "Hello from MicroPython!\n"

    client.send("HTTP/1.1 200 OK\r\n")
    client.send("Content-Type: text/plain\r\n")
    client.send("Connection: close\r\n\r\n")
    client.send(response)
    client.send("<pre>")
    client.send(testuart.getVersion());
    client.send("</pre>")
    client.close()


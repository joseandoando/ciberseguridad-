import os

for i in range(1, 255):
    ip = f"192.168.1.{i}"
    response = os.system(f"ping -c 1 -w 1 {ip} > /dev/null")
    if response == 0:
        print(f"{ip} está activo")

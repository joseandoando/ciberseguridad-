#!/bin/bash
echo "[+] Escaneando red interna..."
nmap -sS -T4 192.168.1.0/24 -oN scan_result.txt
echo "[+] Resultados guardados en scan_result.txt"

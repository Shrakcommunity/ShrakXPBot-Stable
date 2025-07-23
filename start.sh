#!/bin/bash

# Démarre le serveur Flask en arrière-plan
python3 keep_alive.py &

# Lance le bot
python3 main.py

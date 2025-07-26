#!/bin/bash

# Active le mode "fail on error"
set -e

# Démarre le serveur Flask en arrière-plan
python3 keep_alive.py &

# Attendre 1-2 secondes pour s'assurer que Flask est bien démarré
sleep 2

# Démarre le bot et affiche un message s’il crash
echo "▶️ Lancement du bot..."
python3 main.py || echo "❌ Bot terminé avec une erreur."

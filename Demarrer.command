#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
echo "Coopérative IA — démonstration hors ligne"
echo "Ce programme n’installe rien et ne crée aucun réseau."
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.11+ est nécessaire : https://www.python.org/downloads/"
  exit 1
fi
if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
  echo "La version de Python est trop ancienne. Installer Python 3.11 ou plus récent."
  exit 1
fi
echo "Exemple : plafond de 20 % sur une machine de 36 Go avec 12 Go disponibles."
python3 -m coopai quota --installed-gb 36 --available-gb 12 --reserve-gb 2 --percent 20
echo "Exemple : placement fictif dans un cercle de quatre machines."
python3 -m coopai plan examples/mac_circle.json
echo "Vérification du socle :"
python3 -m unittest discover -s tests -v
echo "Terminé. Lire docs/GETTING_STARTED.md pour la suite."
if [[ -t 0 ]]; then read -r -p "Appuyer sur Entrée pour fermer." reply; fi

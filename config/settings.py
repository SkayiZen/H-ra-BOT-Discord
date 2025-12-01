import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s : %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("Bot")

CONFIG_FILE = BASE_DIR / "config" / "config.json"
_config_data = {}

if CONFIG_FILE.exists():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        _config_data = json.load(file)
else:
    logger.warning("Fichier config.json introuvable.")

CSV_PATH = _config_data.get("csv_path", str(BASE_DIR / "config" / "vehicules_cIara_2025.csv"))
HISTORY_PATH = _config_data.get("history_path", str(BASE_DIR / "config" / "backup_data.json"))
COMMANDS_DIR = BASE_DIR / "commandes"

SCENARIO_PATH = BASE_DIR / "config" / "scenario.json"
SCENARIO = {}

if SCENARIO_PATH.exists():
    try:
        with open(SCENARIO_PATH, "r", encoding="utf-8") as file:
            SCENARIO = json.load(file)
        logger.info("Scénario chargé depuis JSON.")
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de syntaxe dans scenario.json : {e}")
else:
    logger.warning("Fichier scenario.json introuvable. L'arbre sera vide.")
import csv
import json
import logging
from pathlib import Path
from core.structures import HistoryLinkedList

logger = logging.getLogger("Bot")

def load_csv_data(filepath):
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            data = list(csv.DictReader(file))
        logger.info(f"CSV chargé : {len(data)} lignes.")
        return data
    except Exception as e:
        logger.error(f"Erreur chargement CSV : {e}")
        return []

def save_history_json(filepath, user_histories):
    try:
        data = {str(userid): history_linked_list.get_all() for userid, history_linked_list in user_histories.items()}
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Erreur sauvegarde JSON : {e}")

def load_history_json(filepath):
    user_histories = {}
    path = Path(filepath)

    if not path.exists():
        return {}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        for uid, cmds in raw_data.items():
            history_list = HistoryLinkedList()
            for commands in cmds:
                history_list.add(commands['cmd'], commands['time'])
            user_histories[int(uid)] = history_list

        logger.info("Historique chargé.")
        return user_histories

    except Exception as e:
        logger.error(f"Erreur lecture JSON : {e}")
        return {}
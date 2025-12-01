import discord
from discord.ext import commands
from config.settings import logger, CSV_PATH, HISTORY_PATH, COMMANDS_DIR, SCENARIO
from core import data_manager
from core.structures import DialogueTree

class BotManager(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="!", intents=intents)

        self.vehicules_data = []
        self.user_histories = {}
        self.dialogue_system = DialogueTree(SCENARIO)

    async def _load_extensions(self):
        if not COMMANDS_DIR.exists():
            logger.error(f"Le dossier {COMMANDS_DIR} n'existe pas !")
            return

        for category in [folder for folder in COMMANDS_DIR.iterdir() if folder.is_dir() and not folder.name.startswith("__")]:
            for file in category.glob("*.py"):
                if not file.name.startswith("__"):
                    ext_name = f"commandes.{category.name}.{file.stem}"
                    try:
                        await self.load_extension(ext_name)
                        logger.info(f"[EXTENSION] Chargee : {ext_name}")
                    except Exception as e:
                        logger.error(f"[ERREUR] Sur {ext_name} : {e}")

    async def setup_hook(self):
        logger.info("--- INITIALISATION ---")

        self.vehicules_data = data_manager.load_csv_data(CSV_PATH)
        logger.info(f"[DATA] CSV : {len(self.vehicules_data)} vehicules charges.")

        self.user_histories = data_manager.load_history_json(HISTORY_PATH)
        logger.info("[DATA] Historique utilisateurs charge.")

        await self._load_extensions()

        logger.info("[SYNC] Synchronisation des commandes Slash...")
        try:
            synced = await self.tree.sync()
            logger.info(f"[SYNC] REUSSIE : {len(synced)} commandes actives.")
        except Exception as e:
            logger.error(f"[ERREUR] Synchro : {e}")

    async def on_ready(self):
        logger.info(f"[ON] CONNECTE : {self.user} (ID: {self.user.id})")

    async def on_disconnect(self):
        logger.info("[SAVE] Sauvegarde automatique en cours...")
        data_manager.save_history_json(HISTORY_PATH, self.user_histories)
        logger.info("[SAVE] Sauvegarde terminee.")
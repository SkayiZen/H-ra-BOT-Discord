import discord
from config.settings import TOKEN, logger
from core.bot import BotManager

if __name__ == "__main__":
    if not TOKEN:
        logger.critical("ERREUR : Aucun token trouvé ! Vérifiez votre fichier .env")
    else:
        try:
            bot = BotManager()
            bot.run(TOKEN)
        except discord.LoginFailure:
            logger.critical("Token invalide.")
        except Exception as e:
            logger.critical(f"Erreur fatale : {e}")
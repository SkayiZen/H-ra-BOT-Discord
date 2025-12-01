import discord
from discord import app_commands
from discord.ext import commands
from core import data_manager
from config.settings import HISTORY_PATH

class ClearCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear_history", description="Vide l'historique.")
    async def clear_history(self, interaction: discord.Interaction):
        userid = interaction.user.id

        if userid in self.bot.user_histories:
            self.bot.user_histories[userid].clear()
            
            data_manager.save_history_json(HISTORY_PATH, self.bot.user_histories)
            
            await interaction.response.send_message("Historique effacé.")
        else:
            await interaction.response.send_message("Rien à effacer.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ClearCmd(bot))
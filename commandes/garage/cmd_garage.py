import discord
from discord import app_commands
from discord.ext import commands
from core.views import GaragePaginationView
from core.structures import HistoryLinkedList
from core import data_manager
from config.settings import HISTORY_PATH

class GarageCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="garage", description="Liste des véhicules.")
    async def garage(self, interaction: discord.Interaction):
        userid = interaction.user.id

        if userid not in self.bot.user_histories:
            self.bot.user_histories[userid] = HistoryLinkedList()
        
        self.bot.user_histories[userid].add("/garage")

        data_manager.save_history_json(HISTORY_PATH, self.bot.user_histories)

        view = GaragePaginationView(self.bot.vehicules_data)
        await interaction.response.send_message(embed=view.get_current_embed(), view=view)

async def setup(bot):
    await bot.add_cog(GarageCmd(bot))
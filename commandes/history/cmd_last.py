import discord
from discord import app_commands
from discord.ext import commands
from core.structures import HistoryLinkedList
from core import data_manager
from config.settings import HISTORY_PATH

class LastCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="last", description="Affiche la commande précédente.")
    async def last(self, interaction: discord.Interaction):
        userid = interaction.user.id

        if userid not in self.bot.user_histories:
            self.bot.user_histories[userid] = HistoryLinkedList()
        
        self.bot.user_histories[userid].add("/last")

        data_manager.save_history_json(HISTORY_PATH, self.bot.user_histories)

        user_history_list = self.bot.user_histories.get(userid)
        previous_command = user_history_list.get_penultimate() if user_history_list else None

        if previous_command:
            embed = discord.Embed(
                title="Commande précédente",
                description=f"**{previous_command['cmd']}**\nDate : {previous_command['time']}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Pas d'historique avant cette commande.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LastCmd(bot))
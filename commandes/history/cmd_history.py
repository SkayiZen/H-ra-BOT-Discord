import discord
from discord import app_commands
from discord.ext import commands
from core.structures import HistoryLinkedList
from core import data_manager
from config.settings import HISTORY_PATH

class HistoryCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="history", description="Affiche tout l'historique.")
    async def history(self, interaction: discord.Interaction):
        userid = interaction.user.id

        if userid not in self.bot.user_histories:
            self.bot.user_histories[userid] = HistoryLinkedList()
        
        self.bot.user_histories[userid].add("/history")

        data_manager.save_history_json(HISTORY_PATH, self.bot.user_histories)

        user_history_list = self.bot.user_histories.get(userid)
        
        if user_history_list and user_history_list.head:
            all_commands = user_history_list.get_all()
            
            history_text = "\n".join([
                f"🔹 `{command_item['time']}` : **{command_item['cmd']}**" 
                for command_item in all_commands
            ])

            if len(history_text) > 4000:
                history_text = history_text[:4000] + "\n... (historique tronqué)"

            embed = discord.Embed(
                title="Historique complet", 
                description=history_text, 
                color=discord.Color.gold()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Historique vide.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HistoryCmd(bot))
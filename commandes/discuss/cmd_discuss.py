import discord
from discord import app_commands
from discord.ext import commands
from core.views import DiscussionView
from core.structures import HistoryLinkedList
from core import data_manager
from config.settings import HISTORY_PATH

class DiscussCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="discuss", description="Lance le questionnaire interactif.")
    async def discuss(self, interaction: discord.Interaction):
        userid = interaction.user.id

        if userid not in self.bot.user_histories:
            self.bot.user_histories[userid] = HistoryLinkedList()
        
        self.bot.user_histories[userid].add("/discuss")

        data_manager.save_history_json(HISTORY_PATH, self.bot.user_histories)

        self.bot.dialogue_system.reset(userid)
        current_node = self.bot.dialogue_system.get_node(userid)
        
        discussion_view = DiscussionView(userid, self.bot.dialogue_system, current_node)
        
        embed = discord.Embed(
            title="Questionnaire", 
            description=current_node.text, 
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=discussion_view)

async def setup(bot):
    await bot.add_cog(DiscussCmd(bot))
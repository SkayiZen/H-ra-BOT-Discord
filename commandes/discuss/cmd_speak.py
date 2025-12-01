import discord
from discord import app_commands
from discord.ext import commands
from core.structures import HistoryLinkedList
from core import data_manager
from config.settings import HISTORY_PATH

class SpeakCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="speak_about", description="Cherche un sujet.")
    async def speak_about(self, interaction: discord.Interaction, topic: str):
        userid = interaction.user.id

        if userid not in self.bot.user_histories:
            self.bot.user_histories[userid] = HistoryLinkedList()
        
        self.bot.user_histories[userid].add(f"/speak_about {topic}")

        data_manager.save_history_json(HISTORY_PATH, self.bot.user_histories)

        topic_exists = self.bot.dialogue_system.search_topic(self.bot.dialogue_system.root, topic)
        
        if topic_exists:
            await interaction.response.send_message(f"Oui, je peux parler de **{topic}**.")
        else:
            await interaction.response.send_message(f"Non, sujet **{topic}** inconnu.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SpeakCmd(bot))
import discord
from discord import app_commands
from discord.ext import commands
from core.structures import HistoryLinkedList
from core import data_manager
from config.settings import HISTORY_PATH

class CheckCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="check", description="Vérifier une plaque.")
    async def check(self, interaction: discord.Interaction, plaque: str):
        userid = interaction.user.id

        if userid not in self.bot.user_histories:
            self.bot.user_histories[userid] = HistoryLinkedList()
        
        self.bot.user_histories[userid].add(f"/check {plaque}")

        data_manager.save_history_json(HISTORY_PATH, self.bot.user_histories)

        formatted_plate = plaque.upper().strip()
        
        found_vehicle = next(
            (vehicle for vehicle in self.bot.vehicules_data 
             if vehicle.get('immatriculation') == formatted_plate), 
            None
        )

        if found_vehicle:
            state = found_vehicle.get('etat', '')
            color = discord.Color.green() if "Disponible" in state else discord.Color.red()
            
            embed = discord.Embed(
                title=f"{found_vehicle.get('marque')} {found_vehicle.get('modele')}", 
                color=color
            )
            embed.add_field(name="Plaque", value=found_vehicle.get('immatriculation'))
            embed.add_field(name="Etat", value=state)
            embed.add_field(name="Localisation", value=found_vehicle.get('localisation'))
            
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Plaque introuvable.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CheckCmd(bot))
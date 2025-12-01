import discord
from discord import app_commands
from discord.ext import commands
from core.structures import HistoryLinkedList
from core import data_manager
from config.settings import HISTORY_PATH

class ModelSelect(discord.ui.Select):
    def __init__(self, vehicles):
        self.vehicles = vehicles

        unique_models = sorted(list(set(vehicule['modele'] for vehicule in vehicles)))
        
        options = []
        for model in unique_models[:25]:
            count = sum(1 for vehicule in vehicles if vehicule['modele'] == model)
            options.append(discord.SelectOption(
                label=model, 
                description=f"{count} véhicules trouvés",
                emoji="🚘"
            ))

        super().__init__(placeholder="Choisis un modèle pour voir les détails...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_model = self.values[0]
        
        filtered_vehicles = [vehicule for vehicule in self.vehicles if vehicule['modele'] == selected_model]
        
        lines = []
        for vehicle in filtered_vehicles:
            state = vehicle.get('etat', 'Inconnu')
            plate = vehicle.get('immatriculation', 'Sans plaque')
            icon = "🟢" if "Disponible" in state else "🔴" if "Hors" in state else "🔧"
            lines.append(f"{icon} `{plate}` • {state}")

        details_text = "\n".join(lines)
        if len(details_text) > 4000:
            details_text = details_text[:4000] + "\n... (tronqué)"

        embed = discord.Embed(
            title=f"Détails : {selected_model}",
            description=details_text,
            color=discord.Color.blue()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SearchView(discord.ui.View):
    def __init__(self, vehicles):
        super().__init__()
        self.add_item(ModelSelect(vehicles))

class SearchCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="search", description="Chercher par marque.")
    async def search(self, interaction: discord.Interaction, marque: str):
        userid = interaction.user.id

        if userid not in self.bot.user_histories:
            self.bot.user_histories[userid] = HistoryLinkedList()
        
        self.bot.user_histories[userid].add(f"/search {marque}")
        data_manager.save_history_json(HISTORY_PATH, self.bot.user_histories)

        search_term = marque.lower()
        
        brand_vehicles = [
            vehicule for vehicule in self.bot.vehicules_data 
            if vehicule['marque'].lower() == search_term
        ]

        if brand_vehicles:
            model_counts = {}
            for vehicule in brand_vehicles:
                model = vehicule['modele']
                model_counts[model] = model_counts.get(model, 0) + 1

            summary_lines = [f"• **{model}** : {count} véhicule(s)" for model, count in model_counts.items()]
            summary_text = "\n".join(summary_lines)

            embed = discord.Embed(
                title=f"Garage : {marque.title()}",
                description=f"Voici les modèles disponibles :\n\n{summary_text}",
                color=discord.Color.purple()
            )
            embed.set_footer(text="Utilisez le menu ci-dessous pour voir les détails.")

            view = SearchView(brand_vehicles)
            await interaction.response.send_message(embed=embed, view=view)
        
        else:
            await interaction.response.send_message(f"Aucun véhicule trouvé pour la marque **{marque}**.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SearchCmd(bot))
import discord
from core.structures import DialogueTree, TreeNode

class GaragePaginationView(discord.ui.View):
    def __init__(self, all_data):
        super().__init__(timeout=None)
        self.all_data = all_data
        self.filtered_data = all_data 
        self.current_page = 0
        self.items_per_page = 10
        self.category_name = "Tous les véhicules"
        self.color = discord.Color.dark_grey()
        self.update_buttons()

    def get_max_pages(self):
        return (len(self.filtered_data) - 1) // self.items_per_page + 1

    def update_buttons(self):
        max_pages = self.get_max_pages()
        if len(self.children) > 5:
            self.children[4].disabled = (self.current_page == 0)
            self.children[5].disabled = (self.current_page >= max_pages - 1)

    def get_current_embed(self):
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page
        page_items = self.filtered_data[start_index:end_index]
        
        description = ""
        if not page_items:
            description = "Aucun résultat."
        
        for vehicle in page_items:
            state = vehicle.get('etat', '')
            icon = "🟢" if "Disponible" in state else "🔴" if "Hors" in state else "🔧"
            
            description += (
                f"{icon} **{vehicle['marque']} {vehicle['modele']}** "
                f"- {vehicle['immatriculation']}\n"
            )

        embed = discord.Embed(
            title=f"{self.category_name} ({len(self.filtered_data)})", 
            description=description, 
            color=self.color
        )
        embed.set_footer(text=f"Page {self.current_page + 1} sur {self.get_max_pages()}")
        return embed

    async def update_view(self, interaction: discord.Interaction):
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_current_embed(), view=self)

    @discord.ui.button(label="Total", style=discord.ButtonStyle.secondary, row=0)
    async def filter_total(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.filtered_data = self.all_data
        self.current_page = 0
        self.category_name = "Tous les véhicules"
        self.color = discord.Color.dark_grey()
        await self.update_view(interaction)

    @discord.ui.button(label="Dispo", style=discord.ButtonStyle.success, row=0)
    async def filter_dispo(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.filtered_data = [
            vehicle for vehicle in self.all_data 
            if "Disponible" in vehicle.get('etat', '')
        ]
        self.current_page = 0
        self.category_name = "Disponibles"
        self.color = discord.Color.green()
        await self.update_view(interaction)

    @discord.ui.button(label="Maint.", style=discord.ButtonStyle.primary, row=0)
    async def filter_maint(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.filtered_data = [
            vehicle for vehicle in self.all_data 
            if "aintenance" in vehicle.get('etat', '')
        ]
        self.current_page = 0
        self.category_name = "En Maintenance"
        self.color = discord.Color.orange()
        await self.update_view(interaction)

    @discord.ui.button(label="H.S.", style=discord.ButtonStyle.danger, row=0)
    async def filter_hs(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.filtered_data = [
            vehicle for vehicle in self.all_data 
            if "Hors" in vehicle.get('etat', '')
        ]
        self.current_page = 0
        self.category_name = "Hors Service"
        self.color = discord.Color.red()
        await self.update_view(interaction)

    @discord.ui.button(label="Prec.", style=discord.ButtonStyle.gray, row=1)
    async def go_prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_view(interaction)

    @discord.ui.button(label="Suiv.", style=discord.ButtonStyle.gray, row=1)
    async def go_next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.get_max_pages() - 1:
            self.current_page += 1
            await self.update_view(interaction)


class DiscussionSelect(discord.ui.Select):
    def __init__(self, userid, tree_system, current_node):
        self.userid = userid
        self.tree_system = tree_system
        
        options = []
        for choice_text in current_node.children.keys():
            options.append(discord.SelectOption(
                label=choice_text.capitalize(), 
                value=choice_text,
                emoji="💭"
            ))

        super().__init__(
            placeholder="Sélectionnez votre réponse...", 
            min_values=1, 
            max_values=1, 
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.userid:
            await interaction.response.send_message("Ce n'est pas votre discussion !", ephemeral=True)
            return
        
        selected_choice = self.values[0]
        next_node = self.tree_system.set_next_node(self.userid, selected_choice)
        
        embed = discord.Embed(
            title="Questionnaire", 
            description=next_node.text, 
            color=discord.Color.blue()
        )
        
        if next_node.is_leaf:
            embed.color = discord.Color.gold()
            await interaction.response.edit_message(embed=embed, view=None)
            self.tree_system.reset(self.userid)
        else:
            new_view = DiscussionView(self.userid, self.tree_system, next_node)
            await interaction.response.edit_message(embed=embed, view=new_view)

class DiscussionView(discord.ui.View):
    def __init__(self, userid, tree_system, current_node):
        super().__init__()
        self.add_item(DiscussionSelect(userid, tree_system, current_node))
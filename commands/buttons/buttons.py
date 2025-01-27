import disnake

class PlaybackControls(disnake.ui.View):
    def __init__(self, ctx, cog):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.cog = cog
        self.is_paused = False 

    @disnake.ui.button(label="Pause", style=disnake.ButtonStyle.secondary)
    async def pause_resume(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user == self.ctx.author:
            if self.is_paused:
                await self.cog.bot.get_command("resume").callback(self.cog, self.ctx)
                self.is_paused = False
                button.label="Pause"  
                button.style = disnake.ButtonStyle.secondary
            else:
                await self.cog.bot.get_command("pause").callback(self.cog, self.ctx)
                self.is_paused = True
                button.label = "Play" 
                button.style = disnake.ButtonStyle.success
            
            await interaction.response.edit_message(view=self)  
        else:
            await interaction.response.send_message("You are not authorized to control playback.", ephemeral=True)

    @disnake.ui.button(emoji="◼️", style=disnake.ButtonStyle.danger)
    async def stop(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user == self.ctx.author:
            await self.cog.bot.get_command("stop").callback(self.cog, self.ctx)
            await interaction.response.defer()
        else:
            await interaction.response.send_message("You are not authorized to control playback.", ephemeral=True)

    @disnake.ui.button(emoji="⏭️", style=disnake.ButtonStyle.primary)
    async def skip(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user == self.ctx.author:
            await self.cog.bot.get_command("skip").callback(self.cog, self.ctx)
            await interaction.response.defer()
        else:
            await interaction.response.send_message("You are not authorized to control playback.", ephemeral=True)

    @disnake.ui.button(emoji="🔁", style=disnake.ButtonStyle.primary)
    async def loop(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user == self.ctx.author:
            await self.cog.bot.get_command("loop").callback(self.cog, self.ctx)
            await interaction.response.defer()
        else:
            await interaction.response.send_message("You are not authorized to control playback.", ephemeral=True)

    @disnake.ui.button(emoji="🔀", style=disnake.ButtonStyle.primary)
    async def shuffle(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user == self.ctx.author:
            await self.cog.bot.get_command("shuffle").callback(self.cog, self.ctx)
            await interaction.response.defer()
        else:
            await interaction.response.send_message("You are not authorized to control playback.", ephemeral=True)
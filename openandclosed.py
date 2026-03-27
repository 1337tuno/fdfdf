import discord
from discord.ui import Button, View
from discord.ext import commands
import os

# Bot setup
TOKEN = 'YOUR_BOT_TOKEN_HERE'
OPEN_IMAGE = 'open_sign.png'
CLOSED_GIF = 'closed_sign.gif'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='*', intents=intents)

class OrderStatusButtons(View):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.channel = channel
    
    @discord.ui.button(label="Accept Orders", style=discord.ButtonStyle.green, emoji="🟢")
    async def accept_orders(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You need **Manage Channels** permission!", ephemeral=True)
            return
        
        # Change channel name to open
        await self.channel.edit(name='🟢・open')
        
        # Update the embed to show OPEN
        embed = discord.Embed(
            title="🟢 WE ARE OPEN!",
            description="**Orders are being accepted**\n\nPlace your orders now!",
            color=discord.Color.green()
        )
        embed.set_footer(text="Beast Eats - Order Status")
        
        # Try to attach open image
        file = None
        if os.path.exists(OPEN_IMAGE):
            file = discord.File(OPEN_IMAGE, filename=OPEN_IMAGE)
            embed.set_image(url=f"attachment://{OPEN_IMAGE}")
        
        # Edit the original message
        await interaction.message.edit(embed=embed, attachments=[file] if file else [])
        await interaction.response.send_message("✅ Status changed to **OPEN** - Channel name updated!", ephemeral=True)
    
    @discord.ui.button(label="Pause Orders", style=discord.ButtonStyle.red, emoji="🔴")
    async def pause_orders(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You need **Manage Channels** permission!", ephemeral=True)
            return
        
        # Change channel name to closed
        await self.channel.edit(name='🔴・closed')
        
        # Update the embed to show CLOSED
        embed = discord.Embed(
            title="🔴 WE ARE CLOSED",
            description="**Orders are currently paused**\n\nWe'll be back soon!",
            color=discord.Color.red()
        )
        embed.set_footer(text="Beast Eats - Order Status")
        
        # Try to attach closed GIF
        file = None
        if os.path.exists(CLOSED_GIF):
            file = discord.File(CLOSED_GIF, filename=CLOSED_GIF)
            embed.set_image(url=f"attachment://{CLOSED_GIF}")
        
        # Edit the original message
        await interaction.message.edit(embed=embed, attachments=[file] if file else [])
        await interaction.response.send_message("⏸️ Status changed to **CLOSED** - Channel name updated!", ephemeral=True)

@bot.command(name='promo')
async def promo(ctx):
    """Setup the Beast Eats order status display"""
    
    # Change channel name to open initially
    await ctx.channel.edit(name='🟢・open')
    
    # Create initial embed showing OPEN status
    embed = discord.Embed(
        title="🟢 WE ARE OPEN!",
        description="**Orders are being accepted**\n\nPlace your orders now!",
        color=discord.Color.green()
    )
    embed.set_footer(text="Beast Eats - Order Status")
    
    # Try to attach open image
    file = None
    if os.path.exists(OPEN_IMAGE):
        file = discord.File(OPEN_IMAGE, filename=OPEN_IMAGE)
        embed.set_image(url=f"attachment://{OPEN_IMAGE}")
    
    # Create the button view with channel reference
    view = OrderStatusButtons(ctx.channel)
    
    await ctx.send(embed=embed, view=view, file=file)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Beast Eats Bot is ready! 🐺')
    print(f'Command: *promo')

# Run the bot
bot.run(TOKEN)
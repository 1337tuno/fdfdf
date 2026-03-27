import discord
from discord.ui import Button, View
from discord.ext import commands
import os

# Bot setup - Read token from environment variable (Railway)
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print("❌ ERROR: TOKEN not found! Set it in Railway Variables.")
    exit(1)

print("✅ Token loaded successfully")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='*', intents=intents)

# Image files
OPEN_IMAGE = 'open_sign.png'
CLOSED_GIF = 'closed_sign.gif'
LOGO_IMAGE = 'beast_eats.png'

class OrderStatusButtons(View):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.channel = channel
    
    @discord.ui.button(label="Accept Orders", style=discord.ButtonStyle.green, emoji="🟢")
    async def accept_orders(self, interaction: discord.Interaction, button: Button):
        # Check permissions
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
        
        # Edit the original message (doesn't create new message)
        await interaction.message.edit(embed=embed, attachments=[file] if file else [])
        
        # Only the user who clicked sees this confirmation
        await interaction.response.send_message("✅ Status changed to **OPEN** - Channel name updated!", ephemeral=True)
    
    @discord.ui.button(label="Pause Orders", style=discord.ButtonStyle.red, emoji="🔴")
    async def pause_orders(self, interaction: discord.Interaction, button: Button):
        # Check permissions
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
        
        # Edit the original message (doesn't create new message)
        await interaction.message.edit(embed=embed, attachments=[file] if file else [])
        
        # Only the user who clicked sees this confirmation
        await interaction.response.send_message("⏸️ Status changed to **CLOSED** - Channel name updated!", ephemeral=True)

@bot.command(name='promo')
async def promo(ctx):
    """Setup the Beast Eats order status display"""
    
    # Check permissions
    if not ctx.channel.permissions_for(ctx.me).manage_channels:
        await ctx.send("❌ Bot needs **Manage Channels** permission!")
        return
    
    # Change channel name to open initially
    await ctx.channel.edit(name='🟢・open')
    
    # Create initial embed showing OPEN status
    embed = discord.Embed(
        title="🟢 WE ARE OPEN!",
        description="**Orders are being accepted**\n\nPlace your orders now!",
        color=discord.Color.green()
    )
    embed.set_footer(text="Beast Eats - Order Status")
    
    # Try to attach Beast Eats logo
    logo_file = None
    if os.path.exists(LOGO_IMAGE):
        logo_file = discord.File(LOGO_IMAGE, filename=LOGO_IMAGE)
        embed.set_thumbnail(url=f"attachment://{LOGO_IMAGE}")
    
    # Try to attach open image
    open_file = None
    if os.path.exists(OPEN_IMAGE):
        open_file = discord.File(OPEN_IMAGE, filename=OPEN_IMAGE)
        embed.set_image(url=f"attachment://{OPEN_IMAGE}")
    
    # Create the button view with channel reference
    view = OrderStatusButtons(ctx.channel)
    
    # Send the message with embed, buttons, and files
    await ctx.send(embed=embed, view=view, file=open_file)
    
    # Delete the command message
    await ctx.message.delete()

@bot.event
async def on_ready():
    print(f'✅ {bot.user} has connected to Discord!')
    print(f'🐺 Beast Eats Bot is ready!')
    print(f'📝 Command: *promo')
    print(f'🔗 Invite URL: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot')

# Run the bot
try:
    bot.run(TOKEN)
except discord.errors.LoginFailure:
    print("❌ ERROR: Invalid token! Check your Railway Variables.")
except Exception as e:
    print(f"❌ ERROR: {e}")

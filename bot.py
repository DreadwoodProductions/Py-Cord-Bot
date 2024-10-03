import discord
from discord import option
from discord.ext import commands
import json
from enum import Enum

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

connected_channel = None

with open('PetInfo.json', 'r') as f:
    pet_data = json.load(f)

class PetType(Enum):
    NORMAL = "Normal"
    SHINY = "Shiny"
    MYTHIC = "Mythic"
    SHINY_MYTHIC = "Shiny Mythic"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="TRAINING"))

async def get_channels(ctx: discord.AutocompleteContext):
    guild = ctx.interaction.guild
    if ctx.focused.name == "channel":
        return [c.name for c in guild.text_channels]
    elif ctx.focused.name == "voice_channel":
        return [c.name for c in guild.voice_channels]

@bot.slash_command(name="connect_to", description="Connect to a channel or voice channel")
@option("channel", description="Text channel to connect to", autocomplete=get_channels)
@option("voice_channel", description="Voice channel to connect to", autocomplete=get_channels)
async def connect_to(ctx, channel: str = None, voice_channel: str = None):
    global connected_channel
    if channel:
        connected_channel = discord.utils.get(ctx.guild.text_channels, name=channel)
    elif voice_channel:
        connected_channel = discord.utils.get(ctx.guild.voice_channels, name=voice_channel)
    
    if connected_channel:
        await ctx.respond(f"Connected to {connected_channel.name}")
    else:
        await ctx.respond("Failed to connect to the specified channel")

@bot.slash_command(name="send_message", description="Send a message to the connected channel")
@option("message", description="Message to send")
async def send_message(ctx, message: str):
    global connected_channel
    if not connected_channel or not isinstance(connected_channel, discord.TextChannel):
        await ctx.respond("Not connected to a text channel. Use /connect_to first.")
        return
    
    await connected_channel.send(message)
    await ctx.respond(f"Message sent to {connected_channel.name}")

@bot.slash_command(name="disconnect", description="Disconnect from the current channel")
async def disconnect(ctx):
    global connected_channel
    if connected_channel:
        channel_name = connected_channel.name
        connected_channel = None
        await ctx.respond(f"Disconnected from {channel_name}")
    else:
        await ctx.respond("Not currently connected to any channel")

async def get_pet_names(ctx: discord.AutocompleteContext):
    return sorted([
        pet for pet in pet_data.keys()
        if "Mythic" not in pet and ctx.value.lower() in pet.lower()
    ])

async def get_pet_types(ctx: discord.AutocompleteContext):
    pet_name = ctx.options['pet_name']
    if pet_name and pet_name in pet_data:
        if pet_data[pet_name].get("Mythic", False):
            return [t.value for t in PetType]
        else:
            return [PetType.NORMAL.value, PetType.SHINY.value]
    return []

@bot.slash_command(name="search", description="Search for a pet")
@option("pet_name", description="Name of the pet to search", autocomplete=get_pet_names)
@option("pet_type", description="Type of pet to search for", autocomplete=get_pet_types)
async def search_pet(ctx, pet_name: str, pet_type: str):
    if pet_name in pet_data:
        pet_info = pet_data[pet_name]
        
        if pet_type in [PetType.MYTHIC.value, PetType.SHINY_MYTHIC.value] and not pet_info.get("Mythic", False):
            await ctx.respond(f"Pet '{pet_name}' is not a Mythic pet.", ephemeral=True)
            return
        
        embed = discord.Embed(title=f"{pet_type} {pet_name}", color=0x00ff00)
        embed.add_field(name="Rarity", value=pet_info.get("Rarity", "Unknown"), inline=False)
        
        stats = {
            "Bubbles": {"value": pet_info["Buffs"].get("Bubbles", 0), "emoji": "🫧"},
            "Coins": {"value": pet_info["Buffs"].get("Coins", 0), "emoji": "🪙"},
            "Gems": {"value": pet_info["Buffs"].get("Gems", 0), "emoji": "💎"}
        }
        
        if pet_info.get("SixCurrency", False):
            candy_value = pet_info["Buffs"].get("Candy", 0)
            if candy_value != 0:
                stats["Multi"] = {"value": candy_value, "emoji": "🔢"}
        
        multiplier = 1
        if pet_type == PetType.SHINY.value:
            multiplier = 2
        elif pet_type == PetType.MYTHIC.value:
            multiplier = 1.5
        elif pet_type == PetType.SHINY_MYTHIC.value:
            multiplier = 3
        
        for stat, data in stats.items():
            value = data["value"] * multiplier
            formatted_value = f"{value:,}"
            embed.add_field(name=f"{data['emoji']} {stat}", value=formatted_value, inline=True)
        
        if "Limited" in pet_info:
            embed.add_field(name="Limited", value="Yes", inline=False)
        if pet_info.get("Mythic", False):
            embed.add_field(name="Mythic", value="Yes", inline=False)
        
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(f"Pet '{pet_name}' not found.", ephemeral=True)

bot.run('MTI0ODI3NzY3Njk0MzQ3NDcxOQ.GUmDCa.w-CE7whvbpM4FZd4O7VB610sBOAwKuwTzM1Nwk')

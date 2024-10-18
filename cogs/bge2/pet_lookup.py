import json
import discord
from discord.ext import commands
from discord import option

class BGE2PetLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pet_data = self.load_json('cogs/bge2/data/PetData.json')
        self.pet_thumbnails = self.load_json('cogs/bge2/data/PetThumbnails.json')

    def load_json(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    @commands.command()
    async def pet_lookup(self, ctx, name: str):
        """Look up a pet from Bubble Gum Ethereal 2"""
        if self.bot.current_mode != 'bge2':
            await ctx.send("This command is only available in BGE2 mode.")
            return

        pet = next((p for p in self.pet_data if p['Name'].lower() == name.lower()), None)
        if pet:
            embed = discord.Embed(title=pet['Name'], description=f"Rarity: {pet['Data']['Rarity']}")
            # Add more pet details to the embed
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Pet '{name}' not found.")

async def setup(bot):
    await bot.add_cog(BGE2PetLookup(bot))

from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency: {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Bot Help", description="List of available commands:", color=discord.Color.blue())
        for command in self.bot.commands:
            embed.add_field(name=command.name, value=command.help or "No description available", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Core(bot))

from discord.ext import commands

class ModeManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.available_modes = ['bge2', 'other_game']

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_mode(self, ctx, mode: str):
        """Set the current mode for the bot"""
        if mode not in self.available_modes:
            await ctx.send(f"Invalid mode. Available modes: {', '.join(self.available_modes)}")
            return
        self.bot.current_mode = mode
        await ctx.send(f"Mode set to: {mode}")

    @commands.command()
    async def current_mode(self, ctx):
        """Display the current mode"""
        mode = self.bot.current_mode or "No mode set"
        await ctx.send(f"Current mode: {mode}")

async def setup(bot):
    await bot.add_cog(ModeManager(bot))

import discord
from discord.ext import commands
import asyncio
import logging
from config import TOKEN, INITIAL_EXTENSIONS

class ModeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.current_mode = None

    async def setup_hook(self):
        for extension in INITIAL_EXTENSIONS:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = ModeBot()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.")
    else:
        print(f'Unhandled error: {error}')
        await ctx.send("An unexpected error occurred. Please try again later.")

if __name__ == '__main__':
    asyncio.run(bot.start(TOKEN))

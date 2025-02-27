import os
import asyncio

import discord
from discord.ext import commands

import data
from cogs import *

class TTSBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents=discord.Intents.default())
        self.data = data.Data()
        self.set_env_vars()

    def set_env_vars(self):
        self.TOKEN, self.GUILD_NAME = self.data.get_env_vars()
        if self.TOKEN == None or self.GUILD_NAME == None:
            print("ERROR in .env file, double check format in top-level README.md")
            exit()

    async def setup_hook(self):
        #Load cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                await self.load_extension("cogs." + filename[:-3])
        print("Extensions loaded")

    #Sync tree
    async def sync_tree(self, guild):
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print("Tree synced")

    async def on_ready(self):
        #Display the name of the connected server
        for guild in self.guilds:
            if guild.name == self.GUILD_NAME:
                print(
                    f'{self.user} is connected to the following guild:'
                    f'{guild.name}(id: {guild.id})\n'
                )

                #Sync tree (for app commands)
                self.GUILD_OBJ = guild
                await self.sync_tree(guild)
                return
            
        #If not connected    
        print("Something went wrong on startup...")
        exit()

async def main():
    bot = TTSBot()
    async with bot:
        await bot.start(bot.TOKEN)

if __name__ == '__main__':
    asyncio.run(main())

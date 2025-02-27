from discord.ext import commands

import data

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data = data.Data()

    #Dms are assumed to be elevenlabs keys
    @commands.Cog.listener("on_message")
    async def register_dm(self, message):
        if message.author == self.bot.user:
            return
        if not message.guild:
            self.data.save_eleven_labs_key(message.author.id, message.content)
            await message.channel.send("Hello " + message.author.name + ", your elevenlabs id has been added")

async def setup(bot: commands.Bot):
    await bot.add_cog(Util(bot))
    
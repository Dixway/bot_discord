import discord
from discord.ext import commands
import datetime
from datetime import datetime 

anti_add = 'off'

class message(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.sniped_message = {}

#Log Message
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.sniped_message[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

        embed = discord.Embed(description=f'**Message supprimé dans {message.channel.mention}** \n {message.content}', color=discord.Color.red(), timestamp=datetime.utcnow())
        embed.set_author(name= f'{message.author.name}', icon_url=message.author.avatar_url)
        channel = self.client.get_channel(916997074040553474)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        embed = discord.Embed(description = f'**Message édité dans {message_before.channel.mention}**', color=discord.Color.red())
        embed.set_author(name= f'{message_before.author.name}', icon_url=message_before.author.avatar_url)
        embed.add_field(name="Avant", value = f'{message_before.content}', inline=False)
        embed.add_field(name="Après", value = f'{message_after.content}', inline=False)
        channel = self.client.get_channel(916997074040553474)
        await channel.send(embed=embed)
        
    
    @commands.Cog.listener()
    async def on_message(self, message):
        global anti_add
        if "discord.gg" in message.content.lower():
            if anti_add == 'on':
                await message.delete()
                await self.client.process_commands(message)   
#Antilink
    @commands.command()
    async def antilink(self, ctx, *, message):
        global anti_add
        if message == 'off' or message == 'on':
            if message == 'off' and anti_add == 'off' :
                await ctx.send('L\'antilink est déjà désactivé !')
            if message =='on' and anti_add == 'on': 
                await ctx.send('L\'antilink est déjà activé !')
            if message == 'on' and anti_add == 'off': 
                anti_add = message
                await ctx.send('Antilink ON')
                return anti_add
            if message == 'off' and anti_add == 'on':
                anti_add = message
                await ctx.send('Antilink OFF')
                return anti_add          
        else:
            await ctx.send('Erreur de syntaxe !')

#Snipe
    @commands.command()
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time = self.sniped_message[ctx.guild.id]
        except:
            await ctx.channel.send("Aucun message trouvé !")
            return

        embed = discord.Embed(description=contents, color=discord.Color.red(), timestamp=time)
        embed.set_author(name=f"{author.name}", icon_url=author.avatar_url)
        embed.set_footer(text=f"Supprimé dans : #{channel_name}")

        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(message(client))   
    
    

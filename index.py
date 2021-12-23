import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv(".env")

intents = discord.Intents.default()
intents.members = True


#Prefix
client = commands.Bot(command_prefix='&', help_command=None, intents=intents)
client.remove_command("help")
client.warnings = {}
client.serverData = {}

#Cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f'Events.{extension}')
    client.load_extension(f'Commands.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'Events.{extension}')
    client.unload_extension(f'Commands.{extension}')

for filename in os.listdir('./Events'):
    if filename.endswith('.py'):
        client.load_extension(f'Events.{filename[:-3]}')

for filename in os.listdir('./Commands'):
    if filename.endswith('.py'):
        client.load_extension(f'Commands.{filename[:-3]}')

#ERROR
@client.event
async def command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('❌ Cette commande n\'existe pas !')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('❌ Vérifiez les qu\il ne manque aucun argument !')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('❌ Vous ne possédez la permission pour effectuer cette commande !')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send('❌ Oups, vous ne pouvez pas effectuer cette commande !')
    if isinstance(error.original, discord.Forbidden):
        await ctx.send('❌ Vous ne possédez la permission nécessaire pour effectuer cette commande !')

client.run(os.getenv('TOKEN'))

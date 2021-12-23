import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, Interaction
from discord_components.client import DiscordComponents

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        DiscordComponents(self.client)
        self.client.remove_command("help")


    async def create_embed(self):
        embed = discord.Embed(
            title="Modération",
            colour=discord.Colour.red()
        )

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/868297057532797009.png?size=96")
        embed.add_field(name="`&ban <membre> [raison]`", value="Cette commande permet de bannir un membre !", inline=False)
        embed.add_field(name="`&unban <membre>`", value="Cette commande permet de débannir un membre !", inline=False)
        embed.add_field(name="`&banlist`", value="Cette commande permet d'observer la liste des membres bannies !", inline=False)
        embed.add_field(name="`&kick <membre> [raison]`", value="Cette commande permet de d'expulser un membre !", inline=False)
        embed.add_field(name="`&warn <membre> [raison]`", value="Cette commande permet de signaler un membre !", inline=False)
        embed.add_field(name="`&addrole <rôle>`", value="Cette commande d'ajouter un rôle à un membre !", inline=False)
        embed.add_field(name="`&delrole <rôle>`", value="Cette commande permet de retirer un rôle à un membre !", inline=False)
        embed.add_field(name="`&snipe`", value="Cette commande permet de voir le dernier message supprimé !s", inline=False)
        embed.set_footer(text='Page d\'aide')
        return embed

    @commands.command()
    async def help(self, ctx):
        channel = ctx.message.channel
        await channel.send(embed=await self.create_embed(), components = [[Button(label = "⮜", style=ButtonStyle.blue, id= "button1"), Button(label = "⮞", style=ButtonStyle.blue)]])

        res = await self.client.wait_for("button_click")
        if(res.channel == ctx.message.channel):
            await res.respond(
                type=4,
                content=f'{res.component.label} clicked !'
            )



def setup(client):
    client.add_cog(Help(client))


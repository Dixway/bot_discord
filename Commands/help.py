import discord, asyncio
from discord import colour
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionEventType

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        DiscordComponents(self.client)
        self.client.remove_command("help")


    async def create_embed(self, fields):
        embed = discord.Embed(
            title="Modération",
            colour=0
        )

        for f in fields: embed.add_field(name=f["name"], value=f["value"], inline=f["inline"])

        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/868297057532797009.png?size=96")
        embed.set_footer(text='Page d\'aide ')
        return embed

    @commands.command()
    async def help(self, ctx):
        
        embedOne = await self.create_embed([
            {"name":"`&ban <membre> [raison]`", "value":"Cette commande permet de bannir un membre !", "inline":False},
            {"name":"`&unban <membre>`", "value":"Cette commande permet de débannir un membre !", "inline":False},
            {"name":"`&banlist`", "value":"Cette commande permet d'observer la liste des membres bannies !", "inline":False},
            {"name":"`&kick <membre> [raison]`", "value":"Cette commande permet de d'expulser un membre !", "inline":False},
            {"name":"`&warn <membre> [raison]`", "value":"Cette commande permet de signaler un membre !", "inline":False},
            {"name":"`&addrole <rôle>`", "value":"Cette commande d'ajouter un rôle à un membre !", "inline":False},
            {"name":"`&delrole <rôle>`", "value":"Cette commande permet de retirer un rôle à un membre !", "inline":False},
            {"name":"`&snipe`", "value":"Cette commande permet de voir le dernier message supprimé !", "inline":False},
            {"name":"`&sanction`", "value":"Cette commande permet de voir les sanctions d\'un joueur !", "inline":False},
            {"name":"`&clear [nombre de message]`", "value":"Cette commande permet de supprimer les messages!", "inline":False},
            {"name":"`&lock`", "value":"Cette commande permet de lock un salon !", "inline":False},
            {"name":"`&unlock`", "value":"Cette commande permet d\'unlock un salon !", "inline":False},
        ])

        embedTwo = await self.create_embed([
            {"name" : '`&antilink`', "value" : 'Permet d\'éviter les pubs ... ', "inline" : False},
            {"name" : '`&clear_webhooks`', "value" : 'Permet de supprimer les webhooks ', "inline" : False},
            {"name" : '`&antilink`', "value" : 'Permet d\'éviter les pubs ... ', "inline" : False},
            {"name" : '`&antilink`', "value" : 'Permet d\'éviter les pubs ... ', "inline" : False},
            {"name" : '`&antilink`', "value" : 'Permet d\'éviter les pubs ... ', "inline" : False},
        ])

        embedThree = await self.create_embed([
            {"name" : '`&serverinfo`', "value" : 'Information du serveur !', "inline" : False},
        ])

        paginationList = [embedOne, embedTwo, embedThree]

        current = 0

        mainMessage = await ctx.reply(
            embed = paginationList[current],
            components = [
                [
                    Button(
                        label= "◀",
                        id = "back",
                        style = ButtonStyle.gray
                    ),
                    Button(
                        label = "▶",
                        id = "front",
                        style = ButtonStyle.gray
                    )
                ]
            ]
        )

        while True:
            try:
                interaction = await self.client.wait_for(
                    "button_click",
                    check = lambda i: i.component.id in ["back", "front"],
                    timeout = 30.0
                )



                #Getting the right list index
                if interaction.component.id == "back":
                    current -= 1
                elif interaction.component.id == "front":
                    current += 1
                #If its out of index, go back to start / end
                if current == len(paginationList):
                    current = 0
                elif current < 0:
                    current = len(paginationList) - 1

                await interaction.respond(
                    type = 7,
                    embed = paginationList[current],
                    components = [
                        [
                        Button(
                            label= "◀",
                            id = "back",
                            style = ButtonStyle.gray
                        ),
                        Button(
                            label = "▶",
                            id = "front",
                            style = ButtonStyle.gray
                        )
                        ]
                    ]
                )
            except asyncio.TimeoutError:
                await mainMessage.delete()
                break


def setup(client):
    client.add_cog(Help(client))


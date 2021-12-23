import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import *


def circle(pfp,size = (215,215)):

    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

class Profil(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.remove_command("profil")

    @commands.command()
    async def profil(self, ctx, member:discord.Member=None):
        if not member:
            member = ctx.author
            name, nick, Id, status = str(member), member.display_name, str(member.id), str(member.status).upper()
            created_at = member.created_at.strftime("%a %b\n%B %Y")
            joined_at = member.joined_at.strftime("%a %b\n%B %Y")
    
            money, level = "800", "28"

            base = Image.open("profil_card.png").convert("RGBA")
            background = Image.open("back_card.png").convert("RGBA")

            pfp = member.avatar_url_as(size=256)
            data = BytesIO(await pfp.read())
            pfp = Image.open(data).convert("RGBA")

            name = f"{name[:16]}.." if len(name)>16 else name 
            nick = f"AKA - {nick[:17]}.." if len(nick)<17 else f"AKA - {nick}"

            draw = ImageDraw.Draw(base)
            pfp = circle(pfp, (215,215))
            font = ImageFont.truetype("Nunito-Regular.ttf", 38)
            akafont = ImageFont.truetype("Nunito-Regular.ttf", 30)
            subfont = ImageFont.truetype("Nunito-Regular.ttf", 25)

            draw.text((280,240),name,font = font)
            draw.text((270,315),nick,font = akafont)
            draw.text((65,490),Id,font = subfont)
            draw.text((405,490),status,font = subfont)
            draw.text((65,635),money,font = subfont)
            draw.text((405,635),level,font = subfont)
            draw.text((65,770),created_at,font = subfont)
            draw.text((405,770),joined_at,font = subfont)
            base.paste(pfp,(56,158),pfp)

            background.paste(base,(0,0), base)

            with BytesIO() as a :
                background.save(a, "PNG")
                a.seek(0)
                await ctx.send(file = discord.File(a, "profile_card.png"))

def setup(client):
    client.add_cog(Profil(client))


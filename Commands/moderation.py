import discord
from discord.ext import commands
import aiofiles
import json


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.remove_command("ban")
        self.client.remove_command("unban")
        self.client.remove_command("kick")
        self.client.remove_command("addrole")
        self.client.remove_command("delrole")
        self.client.remove_command("warn")
        self.client.remove_command("clear")
        self.client.remove_command("lock")
        self.client.remove_command("unlock")
        

    def get_server_data(self, id):
        return self.client.serverData[id]

    def update_file(self, id):
        a_file = open(f"{id}.json", "w")
        json.dump(self.get_server_data(id), a_file)
        a_file.close()

    def update_warns(self, newWarn, id):
        self.get_server_data(id)["warns"].append(newWarn)
        self.update_file(id)

    def update_color(self, color, id):
        self.get_server_data(id)["color"] = int(color, 16)
        self.update_file(id)

#Ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
            ctx.send('Aucune n\'a été raison fournie !')
        else:
            await ctx.send(f'**{member.mention}** a été ban pour : ' + f'`{reason}`')
            await member.ban(reason=reason)

#Unban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member= None):
        if member == None:
            ctx.send('Erreur de syntaxe')
        else:
            member = await self.client.fetch_user(int(member))
            await ctx.guild.unban(member)
            await ctx.send(f'**{member.name}+** a été unban !')
        
 

#Kick
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None, message: discord.Message):
        if reason == None:
            reason = 'Aucune raison n\'a été fournie !'
        await ctx.send(f'**{member.mention}** a été kick pour : ' + f'`{reason}`')
        await member.kick(reason=reason)

        embed = discord.Embed(description = 'texte', color=discord.Color.red())
        embed.set_author(f'{message.author.name}#{message.authordiscriminator}',message.author.avatar_url)  

        await ctx.send(embed=embed)

#Role error
    async def role_interaction(self, member, role, ctx):
        if member == None:
            await ctx.send('Aucun membre spécifié !')
        if role == None:
            await ctx.send('Aucun role spécifié !')

#Addrole
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member = None, *, role: discord.Role = None):
        self.role_interaction(member, role, ctx)
        await ctx.message.delete()
        await member.add_roles(role)
        await ctx.send(f'{member.mention} a reçus le role "{role}"')

#Delrole
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, ctx, member: discord.Member = None, *, role: discord.Role = None):
        self.role_interaction(member, role, ctx)
        await ctx.message.delete()
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} a perdu le role "{role}"')

#Lock
    @commands.command()
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send(ctx.channel.mention + 'est lock')
                
#Unlock    
    @commands.command()
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.send(ctx.channel.mention + 'est unlock')
#Mute
    @commands.command()
    async def mute(self, ctx, member : discord.Member, *, reason = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if (not ctx.author.guild_permissions.manage_messages):
            await ctx.send('Pas la permission requise pour mute')
            return
        guild = ctx.guild
        muteRole = discord.utils.get(guild.roles, name='Muted')

        if not muteRole:
            await ctx.send('Aucune role mute trouvé, création du rôles en cours ...')
            muteRole = await guild.create_role(name='Muted')
            for channel in guild.channels:               
                await channel.set_permissions(muteRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)        

        if role in member.roles:
            await ctx.send('Cet utilisateur est déjà mute')

        else:
            await member.add_roles(muteRole, reason=reason)
            await ctx.send(f'{member.mention} a été **mute**')
            await member.send(f'Tu as été mute sur **{guild.name}** | Raison : **{reason}**')


#Unmute
    @commands.command()
    async def unmute(self, ctx, member : discord.Member, *, reason = None):
        if (not ctx.author.guild_permissions.manage_messages):
            await ctx.send('Pas la permission requise pour mute')
            return
        guild = ctx.guild
        muteRole = discord.utils.get(guild.roles, name='Muted')

        if not muteRole in member.roles:
            await ctx.send('Cet utilisateur n\'est pas mute')
            return 
        else:
            await member.remove_roles(muteRole, reason=reason)
            await ctx.send(f'{member.mention} a été **unmute**')
            await member.send(f'Votre mute sur **{guild.name}** vient de prendre fin !')
        
#DM
    @commands.command()
    async def dm(self, ctx, user_id = None, *, args = None):
        if user_id != None and args != None:
            try:
                target = await self.client.fetch_user(user_id)
                await target.send(args)
                await ctx.channel.send("'"+ args + "'"'a été envoyé a' + target.name)
            except:
                await ctx.channel.send('Impossible de dm cet utilisateur !')       
        else:
            await ctx.channel.send('Aucun utilisateur ou message n\'a été marqué')

#DM ALL (corrigé erreur)
    @commands.command()
    async def dmall(self, ctx, *, args = None):
        if args != None:
            members = ctx.guild.members
            for member in members:
                try:
                    await member.send(args)
                    await ctx.channel.send("'" + args + "'"'a été envoyé a' + member.name)
                except:
                    await ctx.channel.send('Impossible de dm all !')
        else:
            await ctx.channel.send('Aucun message n\'a été marqué')

#Say
    @commands.command()
    async def say(self, ctx, message=None):
        if not message == None:
            await ctx.send(message)
            await ctx.message.delete()
        else:
            await ctx.send('Erreur de syntaxe !')
            await ctx.message.delete()

#vkick
    @commands.command()
    async def voicekick(self, ctx, member: discord.Member):
        await member.voice_client.disconnect()
#move

#color
    @commands.command()
    async def color(self, ctx, colorint):
        self.update_color(colorint.replace('#', ''), ctx.guild.id)
        await ctx.send(f'{ctx.author.name} a mis a jour la couleur en "{colorint}"')

#pic
    @commands.command()
    async def pic(self, ctx, member: discord.Member = None):
        if(member is None): member = ctx.author
        embed = discord.Embed(title = member.name, color=discord.Color.red())
        embed.set_image(url = member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def banner2(self, ctx, member: discord.Member = None, ):
        if(member is None): member = ctx.author
        banniere = discord.Guild.banner_url
        embed = discord.Embed(title = member.name, color=discord.Color.red())   
        embed.add_field(name = "Bannière", value = banniere, inline = False)
        await ctx.send(embed=embed)

        
#banner
    @commands.command()
    async def banner(self, ctx, user:discord.Member = None):
        if user == None:
            user = ctx.author
        req = await self.client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        # If statement because the user may not have a banner
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
        embed = discord.Embed(title = user.name, color=discord.Color.red())
        embed.set_image(url = banner_url)
        await ctx.send(embed=embed)

    @commands.command()
    
#Warn
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member=None, *, reason=None):
        if member is None:
            return await ctx.send("Veuillez saisir un utilisateur valide !")
            
        if reason is None:
            return await ctx.send("Veuillez saisir une raison !")

        try:
            first_warning = False
            self.client.warnings[ctx.guild.id][member.id][0] += 1
            self.client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

        except KeyError:
            first_warning = True
            self.client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

        count = self.client.warnings[ctx.guild.id][member.id][0]
        self.update_warns({"target": member.id, "author": ctx.author.id, "reason": reason}, ctx.guild.id)

        await ctx.send(f"{member.mention} possède {count} {'warn' if first_warning else 'warns'}.")

#Sanctions
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sanctions(self, ctx, member: discord.Member=None):
        if member is None:
            return await ctx.send("Erreur de syntaxe !")
        
        embed = discord.Embed(description="", colour=discord.Colour.red())
        embed.set_author(name= f'{member.name}', icon_url=member.avatar_url)
        try:
            i = 1
            for admin_id, reason in self.client.warnings[ctx.guild.id][member.id][1]:
                admin = ctx.guild.get_member(admin_id)
                embed.description += f"**{i}** - par: {admin.mention} pour: **{reason}**.\n"
                i += 1

            await ctx.send(embed=embed)

        except KeyError: # no warnings
            await ctx.send("Cet utilisateur ne possède aucun sanction !")
#Webbok
    @commands.command()
    async def clear_webhooks(self, ctx):
        for webhook in await ctx.guild.webhooks(): 
            try:
                await webhook.delete()
                await ctx.send('Tous les webhooks on été supprimé !')
            except Exception as e:
                print(e) 

#Server Info
    @commands.command()
    async def serverinfo(self, ctx):
        color = self.get_server_data(ctx.guild.id)["color"]
        role_count = len(ctx.guild.roles)
        channel_count = len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)
        true_member = len([m for m in ctx.guild.members if not m.bot])
        bot_count = len(([member for member in ctx.guild.members if member.bot]))
        boosters = len(ctx.guild.premium_subscribers)
        emoji_count = len(ctx.message.guild.emojis)
        boost_level = str(ctx.guild.premium_tier)
        voice_numbers = sum(len(c.members) for c in ctx.guild.voice_channels)
        online_member_server = sum(member.status !='offline' and not member.bot for member in ctx.guild.members)

        embed = discord.Embed(title = ctx.guild.name, timestamp= ctx.guild.created_at,color=color, url= ctx.guild.icon_url)
        embed.add_field(name='ID', value= f'{ctx.guild.id}', inline = True)
        embed.add_field(name='Nombre de membres', value= ctx.guild.member_count, inline = True)
        embed.add_field(name='Nombre d\'humains', value= str(true_member), inline = True)
        embed.add_field(name='Nombre de salons', value= str(channel_count) , inline = True)
        embed.add_field(name='Nombre de bots', value= str(bot_count) , inline = True)
        embed.add_field(name='Niveau du serveur', value= str(boost_level), inline = True)
        embed.add_field(name='Nombre de rôles', value= str(role_count), inline = True)
        embed.add_field(name='Nombre de d\'émojies', value= str(emoji_count), inline = True)
        embed.add_field(name='Nombre de boosts', value= f'{str(ctx.guild.premium_subscription_count)}', inline = True)
        embed.add_field(name='Nombre de boosters', value= str(boosters), inline = True)
        embed.add_field(name='Nombres en vocals', value= str(voice_numbers), inline = True)
        embed.add_field(name='Nombres de membres actifs', value= str(online_member_server), inline = True)
        embed.set_footer(text = 'Création du serveur ')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        
        await ctx.send(embed=embed)

#Clear
    @commands.command()
    async def clear(self, ctx, amount: str) -> None:
        try:
            amount = int(amount)
        except ValueError:
            return await ctx.reply("Please input a valid amount (5-100)")
        else:
            if not (5 < amount < 100):
                return await ctx.reply("Please input a valid amount (5-100)")
            try:
                await ctx.channel.purge(limit=amount + 1)
            except Exception as e:
                await ctx.send(f"**ERROR**, `{e}`")



def setup(client):
    client.add_cog(Moderation(client))


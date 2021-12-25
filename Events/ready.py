import discord
from discord.ext import commands, tasks
from itertools import cycle
import json
import os.path 

class status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.status = cycle(['En cours de dev .', 'En cours de dev ..', 'En cours de dev ...'])

    @tasks.loop(seconds=1.0)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        
        for guild in self.client.guilds:
            self.client.warnings[guild.id] = {}
            self.client.serverData[guild.id] = {}
            
            default = {
                "prefix": "&",
                "color": 16777215,
                "warns": []
            }

            if not os.path.exists(f"{guild.id}.json"):
                with open(f"{guild.id}.json", 'w') as srv_file:
                    json.dump(default, srv_file)

            data = json.load(open(f"{guild.id}.json"))
            self.client.serverData[guild.id] = data
            for line in data['warns']:
                target = int(line['target'])
                author = int(line["author"])
                reason = "".join(line["reason"])
                try:
                    self.client.warnings[guild.id][target][0] += 1
                    self.client.warnings[guild.id][target][1].append((author, reason))

                except KeyError:
                    self.client.warnings[guild.id][target] = [1, [(author, reason)]]

    @commands.Cog.listener()                            
    async def on_guild_join(self, guild):
        self.client.warnings[guild.id] = {}
        self.client.serverData[guild.id] = {}

def setup(client):
    client.add_cog(status(client))
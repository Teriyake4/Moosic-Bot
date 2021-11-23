# Discord Bots\Moosic Bot\moosicCmd.py
import moosicCmd
# Discord Bots\Moosic Bot\moosicUtil.py
from moosicUtil import *

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import date
from datetime import datetime

os.system("cls")

# https://discord.com/api/oauth2/authorize?client_id=892635723184881725&permissions=517580545344&scope=bot
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
cogs = [moosicCmd]
client = commands.Bot(command_prefix='-',
intents = discord.Intents.all())
client.remove_command("help")
client.remove_command("l")

# connection
print("Connecting\n")
@client.event
async def on_ready():
    # print bot information
    try:
        os.system("cls")
        dateTime()
        print("Connected")
        print("Client Name: {}".format(client.user.name))
        print("Client id: {}".format(client.user.id))
        print("Discord.py Version: {}".format(discord.__version__))
        print('\nServers connected to:')
        for guild in client.guilds:
            print(guild.name + " id: {}".format(guild.id))
        print("\n")

    except Exception as e:
        print(e)
    # status
    await client.change_presence(activity = discord.Game("-help"))

# commands from moosicCmd.py
def moosic(cogs, client):
    for i in range(len(cogs)):
        cogs[i].setupCmd(client)

moosic(cogs, client)


client.run(TOKEN)

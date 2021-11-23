import time
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, date

# date and time
def dateTime():
    global date
    global time
    date = date.today()
    time = datetime.now()

# message information
async def msgInfo(ctx):
    dateTime()
    print("Date: {}".format(date.strftime("%B %d, %Y")))
    print("Time: {}".format(time.strftime("%H:%M:%S")))
    print("Server: {}".format(ctx.message.guild))
    print("Author: {}".format(ctx.message.author))
    print("Command: {}".format(ctx.message.content))
    print("Action: ", end="")

# url log
async def urlLog(self, ):
    with open("urlLog.txt", "w") as f:
        dateTime()
        f.write("Date: {}".format(date.strftime("%B %d, %Y")))
        f.write("Time: {}".format(time.strftime("%H:%M:%S")))
        f.write("Server: {}".format(ctx.message.guild))
        f.write("Author: {}".format(ctx.message.author))
        f.write("Url: ")

# check if anything is playing
async def ifPlaying(self, ctx):
    try:
        if self.playing == False:
            await ctx.send("Nothing is playing right now")
            print("Nothing was playing\n")

    except:
        pass

async def joinVc(ctx):
    # connection to voice channel
    # if user is not in voice channel
    if ctx.author.voice is None:
        await ctx.send("Please join a voice channel")
        print("Wasn't in voice channel")
    voice_channel = ctx.author.voice.channel
    # if user is in voice channel
    if ctx.voice_client is None:
        await voice_channel.connect()
        print("Connected to voice channel: {}".format(voice_channel))
    else:
        await ctx.voice_client.move_to(voice_channel)
        print("Connected to voice channel: {}".format(voice_channel))

# disconnect if no one in vc
# disconnect after inactivity
async def timeout(self, ctx):
    if self.playing == False:
        print("Timeout started")
        for i in range(60):
            if self.playing == True:
                break
            else:
                await asyncio.sleep(1)
    if self.playing == False:
        await ctx.send("Disconnected due to inactivity")
        print("Disconnected due to inactivity")

def multiPlay():
    pass

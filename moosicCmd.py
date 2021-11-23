from moosicUtil import *
from MoosicPlay import *

import discord
from discord.ext import commands
import youtube_dl
import asyncio


# commands and player
class moosicCmd(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loop = 1
        self.queue = []
        self.playing = False


    # join and add to queue
    @commands.command()
    async def play(self, ctx, *search):
        await msgInfo(ctx)
        # adds the "search"
        for arg in search:
            search1 = " ".join(arg)
        # if there is no argument for search
        if search1 == "":
            await ctx.send("Please enter your search or url")
            print("Didn't enter search or url\n")
        else:
            audioInfo = await ytSearch(ctx, search1)
            self.queue.append(audioInfo)
            await joinVc(ctx)
            if len(self.queue) > 1 or self.playing == True:
                await ctx.send("Number {} in queue".format(len(self.queue)))
            if len(self.queue) == 1 and self.playing == False:
                print("Started player\n")
                await asyncio.create_task(player(self, ctx, audioInfo))
                # if queue is empty and nothing is playing, dc
                if len(self.queue) == 0 and self.playing == False:
                    try:
                        await ctx.voice_client.disconnect()
                        await ctx.send("Disconnected because queue was empty.")
                        dateTime()
                        print("Disconnected because queue was empty.\n")
                    except:
                        pass
            else:
                print("Added to queue")
                print("Queue length: {}\n".format(len(self.queue)))
    @commands.command()
    async def p(self, ctx, *search):
        await self.play(ctx, search)

    # disconnect
    @commands.command()
    async def disconnect(self, ctx):
        await msgInfo(ctx)
        await ctx.voice_client.disconnect()
        self.playing = False
        self.queue.clear()
        await ctx.send("Disconnected")
        print("Disconnected\n")
    @commands.command()
    async def dc(self, ctx):
        await self.disconnect(ctx)

    # pause
    @commands.command()
    async def pause(self, ctx):
        await msgInfo(ctx)
        if self.playing == False:
            await ctx.send("Nothing is playing right now")
            print("Nothing was playing\n")
        else:
            ctx.voice_client.pause()
            await ctx.send("Paused")
            print("Paused\n")
    @commands.command()
    async def pd(self, ctx):
        await self.pause(ctx)

    # resume
    @commands.command()
    async def resume(self, ctx):
        await msgInfo(ctx)
        if self.playing == False:
            await ctx.send("Nothing is playing right now")
            print("Nothing was playing\n")
        else:
            ctx.voice_client.resume()
            await ctx.send("Resumed")
            print("Resumed\n")
    @commands.command()
    async def r(self, ctx):
        await self.resume(ctx)

    # stop
    @commands.command()
    async def stop(self, ctx):
        await msgInfo(ctx)
        if self.playing == False:
            await ctx.send("Nothing is playing right now")
            print("Nothing was playing\n")
        else:
            ctx.voice_client.stop()
            self.queue.clear()
            self.playing = False
            await ctx.send("Stopped queue")
            await ctx.send("Please disconnect the bot if your are done using it")
            print("Stopped queue\n")

    # loop
    @commands.command()
    async def loop(self, ctx, loopNumber = "infinite"):
        await msgInfo(ctx)
        if self.playing == False:
            await ctx.send("Nothing is playing right now")
            print("Nothing was playing\n")
        else:
            try:
                self.loop = loopNumber
                # infinite loop
                if loopNumber == "infinite":
                    await ctx.send("Looping")
                    print("Loop infinitely\n")
                # fixed number loop
                else:
                    int(self.loop)
                    await ctx.send("Looping {}".format(self.loop))
                    print("Looping {}\n".format(self.loop))
            except:
                await ctx.send("Please enter a number")
                print("Didn't enter a number\n")
    @commands.command()
    async def l(self, ctx, loopNumber = "infinite"):
        await self.loop(ctx, loopNumber)

    # skip
    @commands.command()
    async def skip(self, ctx):
        await msgInfo(ctx)
        if self.playing == False:
            await ctx.send("Nothing is playing right now")
            print("Nothing was playing\n")
        else:
            if len(self.queue) == 0:
                await ctx.send("No songs to skip to")
                print("No songs to skip to\n")
            else:
                ctx.voice_client.stop()
                self.playing = False
                await asyncio.sleep(1)
                await ctx.send("Skipped")
                print("Skipped\n")
                await asyncio.create_task(player(self, ctx, self.queue[0]))
    @commands.command()
    async def s(self, ctx):
        await self.skip(ctx)

    # show queue
    @commands.command()
    async def queue(self, ctx):
        await msgInfo(ctx)
        if self.playing == False:
            await ctx.send("Nothing is playing right now")
            print("Nothing was playing\n")
        elif len(self.queue) == 0:
            await ctx.send("Nothing is in the queue")
            print("Nothing was in the queue\n")
        else:
            x = 0
            for i in range(len(self.queue)):
                x += 1
                await ctx.send("{number}. `{queue}`".format(number = x, queue = self.queue[x - 1]["title"]))
            print("Showed queue\n")

    # clear queue
    @commands.command()
    async def clear(self, ctx):
        await msgInfo(ctx)
        if self.playing == False:
            await ctx.send("Nothing is playing right now")
            print("Nothing was playing\n")
        elif len(self.queue) <= 1:
            await ctx.send("Nothing is in the queue")
            print("Nothing was in the queue\n")
        else:
            self.queue.clear()
            await ctx.send("Queue cleared")
            print("Queue cleared\n")
    @commands.command()
    async def cq(self, ctx):
        await self.clear(ctx)

    # help
    @commands.command()
    async def help(self, ctx):
        await msgInfo(ctx)
        await ctx.send("""
My prefix is \"-\"
All Commands List:

play \"search\" --- Plays specified search or url(only Youtube for now... and no playlists or streams)
dc --- Disconnects the bot
stop --- Stops all songs in queue
pause --- Pauses the current song
resume --- Resumes the current song
loop \"number of loops\" --- Loops current song infinitely unless specified with number of times
skip --- Skips the current song
clear --- Clears the queue
queue --- Shows all songs currently in queue(Work in progress)

Contact Teriyake4 for bugs, help, and suggestions
Please be nice to the bot, it is very fragile
                        """)
        print("Gave help\n")


def setupCmd(client):
    client.add_cog(moosicCmd(client))

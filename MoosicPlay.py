from moosicUtil import *

import discord
from discord.ext import commands
import youtube_dl
import asyncio


# player of queue
async def player(self, ctx, audioInfo):
    # prep
    vc = ctx.voice_client
    try:
        while len(self.queue) > 0 and not self.playing:
            self.playing = True
            searchInfo = self.queue[0]
            self.queue.pop(0)
            FFMPEG_OPTIONS = {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                "options": "-vn"
            }
            # audioInfo = await ytSearch(ctx, searchInfo)
            # loop infinte prep
            x = 0
            loopIter = 0
            if self.loop == "infinite":
                loopType = 1
            else:
                loopType = self.loop
            # loop
            while loopType > x:
                loopIter += 1
                if self.loop != "infinite":
                    x += 1
                source = await discord.FFmpegOpusAudio.from_probe(audioInfo["playingUrl"], **FFMPEG_OPTIONS)
                dateTime()
                print("Playing " + audioInfo["url"])
                print("Queue length: {}".format(len(self.queue)))
                print("Loop type: {}".format(self.loop))
                print("Loop iteration: {}\n".format(loopIter))
                if not vc.is_playing():
                    vc.play(source)
                    await ctx.send("Now Playing: `{}`".format(audioInfo["title"]))
                    sleepTime = audioInfo["duration"] + 1
                    int(sleepTime)
                    for i in range(sleepTime):
                        if self.playing == False:
                            break
                        else:
                            await asyncio.sleep(sleepTime)
                else:
                    print("vc was playing")
                if self.loop == "infinite":
                    loopType = 1
                    x=0
    except Exception as e:
        await ctx.send("You found a bug! Try disconnecting and try again or \"-help\" for help.")
        print(e)
        self.queue.clear()

    self.playing = False

# searches youtube
async def ytSearch(ctx, search):
    await ctx.send("Searching: `{}`".format(search))
    print("Searched {}".format(search))
    YDL_OPTIONS = {"format": "bestaudio"}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            # trys link
            video = ydl.extract_info(search, download=False)
        except:
            # searches youtube
            video = ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]
        # once the first search is added
        url = video["formats"][0]["url"]
        audioInfo = {
        "playingUrl" : url,
        "url" : video["webpage_url"],
        "duration" : video["duration"],
        "title" : video["title"],
        }
        return audioInfo

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 11:58:55 2021

@author: dudle
"""

import discord
from discord.ext import commands
import youtube_dl
import os
import nest_asyncio
from requests import get
from dotenv import load_dotenv

load_dotenv()
nest_asyncio.apply()
TOKEN = os.getenv("TOKEN")
print("Loading bot: " + TOKEN)

client = commands.Bot(command_prefix="!")
songList = []

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
YDL_OPTS = {'format': 'bestaudio', 'noplaylist':'True'}

def search(arg):
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)
        else:
            video = ydl.extract_info(arg, download=False)
    return video['webpage_url']

def queue(arg):
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)
        else:
            video = ydl.extract_info(arg, download=False)
    return video['title']

@client.command()
async def play(ctx,*, arg : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        print("error1")
        songList.append(queue(arg))
        print("error2")
        await ctx.send("Added ", str(queue(arg))," to Queue")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Talk - 128kbs')
    try:
        await voiceChannel.connect()
    except:
        print("already in voice channel")
    else:
        print("connected to voice")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search(arg)])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused")
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Resumed")
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    
@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
            await ctx.send('Nothing to skip')
            return
    else:
        voice.stop()
        
        ctx.send('Skipped')


client.run(TOKEN)


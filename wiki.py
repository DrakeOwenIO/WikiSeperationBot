import abc
from cgitb import html
from tracemalloc import start
from turtle import clear
from urllib.request import urlopen
import discord
import asyncio
import urllib3
import string
from datetime import datetime, date, timedelta
from time import timezone
from bs4 import BeautifulSoup
from discord import message
from discord import colour
from discord import channel
from discord.channel import TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.abc import Messageable
from discord.message import Message

# Command prefix
client = commands.Bot(command_prefix = '-', case_insensitive=True, help_command=None)
client.launch_time = datetime.utcnow()

# Set the play status
@client.event
async def on_ready():
    # Setting `Playing ` status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Wikipedia"))
    print('Bot is ready.')

# Uptime command
@client.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time #Calculates Bot Uptime
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send("Seperation Bot has been running for " + f"{days}d {hours}h {minutes}m")

# Delete messages
@client.command(pass_context = True)
async def delete(ctx, number):
    number = int(number) #Converting the amount of messages to delete to an integer
    await ctx.send("Deleting...")
    await ctx.channel.purge(limit = number + 2)

# Say command
@client.command(pass_context = True)
async def say(ctx, *whatYouWantBotToSay):

    await ctx.channel.purge(limit = 1)

    response = ' '.join(whatYouWantBotToSay)

    await ctx.send(response)

# Wiki
@client.command(pass_context = True)

# Note: * is used to make var a tuple so that it reads whitespace
async def wiki(ctx, *startingWikiPage): 

    # Join tuple with underscore
    startingWikiPage = ('_'.join(str(x) for x in startingWikiPage))

    # Create Wiki page
    startingWikiPage = 'https://en.wikipedia.org/wiki/' + str(startingWikiPage)

    page = urlopen(startingWikiPage)

    soup = BeautifulSoup(page, "lxml")

    # mydivs = soup.findAll("div", {"class": "mw-parser-output"})

    # print(mydivs)

    links = []
    # for link in soup.findAll('a'):
    for link in soup.findAll("div", {"class": "mw-parser-output"}):
        for link in soup.findAll('p'):
            links.append(link.get('href'))
            # await ctx.send(link)
            print(link.encode("utf-8"))


    # targetPage = 'https://en.wikipedia.org/wiki/Philosophy'

    # URLLib3 Connection
    # http = urllib3.PoolManager()
    # url = 'https://en.wikipedia.org/wiki/' + startingWikiPage 

    

#Run Token
client.run('')
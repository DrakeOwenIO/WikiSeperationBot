from ast import While
import discord
from datetime import datetime
from bs4 import BeautifulSoup
from discord.ext import commands
from urllib.request import urlopen

# Command prefix
client = commands.Bot(command_prefix = '-', case_insensitive=True, help_command=None)
client.launch_time = datetime.utcnow()

# This function is used in the wiki command
# It finds the first link on a wiki page and confirms that it 
# isn't in ()
def is_first(pLink):
    strBuilder = ""
    strTemp = ""
    counter1 = 0
    counter2 = 0
    for sibling in pLink.previous_siblings:
        thing = type(sibling)
        if str(thing) == "<class 'bs4.element.NavigableString'>":
            strTemp = strBuilder
            strBuilder = sibling + strTemp
    counter1 = strBuilder.count('(')
    counter2 = strBuilder.count(')')
    if counter1 > counter2:
        return False
    else:
        return True 


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

    found_it = False
    firstLink = None

    for childNode in soup.findAll("div", {"class": "mw-parser-output"}):
        for paragraph in soup.findAll('p'):
            for link in paragraph.findAll('a',recursive=False):
                if is_first(link) == True:
                    found_it = True
                    firstLink = link
                    break
            if found_it == True:
                break
        if found_it == True:
            break

    await ctx.send(firstLink['title'])
    firstLinkURL = 'https://en.wikipedia.org/wiki/' + firstLink['title']

    while firstLink['title'] != 'Philosophy':
        page = urlopen(firstLinkURL)

        soup = BeautifulSoup(page, "lxml")

        found_it = False
        firstLink = None

        for childNode in soup.findAll("div", {"class": "mw-parser-output"}):
            for paragraph in soup.findAll('p'):
                for link in paragraph.findAll('a',recursive=False):
                    if is_first(link) == True:
                        found_it = True
                        firstLink = link
                        break
                if found_it == True:
                    break
            if found_it == True:
                break
        
        firstLinkURL = 'https://en.wikipedia.org' + firstLink['href']
        await ctx.send(firstLink['title'])



    # targetPage = 'https://en.wikipedia.org/wiki/Philosophy'



#Run Token
client.run('')
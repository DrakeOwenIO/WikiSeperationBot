from ast import While
import discord
from datetime import datetime
from bs4 import BeautifulSoup
from discord.ext import commands
from urllib.request import urlopen

# Command prefix
client = commands.Bot(command_prefix = '-', case_insensitive=True, help_command=None)
client.launch_time = datetime.utcnow()

# Set the play status
@client.event
async def on_ready():
    # Setting `Playing ` status
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Wikipedia"))
    print('Bot is ready.')

# Checks if a link is in parentheses
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

# Test if a page has already been opened
def is_in_list(list, testValue):
    for i in list:
        if (i == testValue):
            return True

# Finds first link
def find_link(soup):
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
    
    return firstLink

# Wiki
@client.command(pass_context = True)

# Note: * is used to make var a tuple so that it reads whitespace
async def wiki(ctx, *startingWikiPage): 

    # Initialize counter, starting page title and pageList
    seperationCounter = 0
    ogPageTitle = " ".join([str(s) for s in list(startingWikiPage)])
    pageList = []
    infiniteLoop = False

    # Join tuple with underscore
    startingWikiPage = ('_'.join(str(x) for x in startingWikiPage))

    # Create first wiki page
    startingWikiPage = 'https://en.wikipedia.org/wiki/' + str(startingWikiPage)

    # Open the page
    page = urlopen(startingWikiPage)
    soup = BeautifulSoup(page, "lxml")

    # Find the first link in the page
    firstLink = find_link(soup)
    pageList.append(firstLink['title'])

    # Send page title and update counter
    await ctx.send(firstLink['title'])
    seperationCounter += 1

    firstLinkURL = 'https://en.wikipedia.org' + firstLink['href']

    while firstLink['title'] != 'Philosophy':
        
        # open the page
        page = urlopen(firstLinkURL)
        soup = BeautifulSoup(page, "lxml")

        # Find the first link on the page
        firstLink = find_link(soup)
        
        # Test if its an infinite loop
        if (is_in_list(pageList, firstLink['title']) == True):
            await ctx.send("This wiki page is not related to Philosophy")
            infiniteLoop = True
            break
        else:
            # Add to the counter, update the link, and send the page
            seperationCounter += 1
            pageList.append(firstLink['title'])
            firstLinkURL = 'https://en.wikipedia.org' + firstLink['href']
            await ctx.send(firstLink['title'])

        
    if(infiniteLoop == False):
        # send final message
        await ctx.send("There are " + str(seperationCounter) + " degrees of seperation between " + '"' + ogPageTitle + '"' + " and Philosophy.")
    



#Run Token
client.run('')
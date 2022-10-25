import requests
import discord
import json

#Discord token can be acquired from the discord app as just a regular user.
TOKEN = ""

intents = discord.Intents.default()

intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have loggen in as {}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

#checks if player is active and reports back in chat, to be active message needs to start with "!"
    elif message.content.startswith('!'):
        cmd = message.content.split()[0].replace("!", "")
        link = 'https://armory.warmane.com/api/character/{}/Icecrown/summary'.format(cmd)
        apidata = requests.get(link, headers={'User-Agent': 'Custom'})

        jdata = json.loads(apidata.text)

        if jdata.get("online") is False:
            await message.channel.send(cmd + " is offline \u274C")
        else:
            await message.channel.send(cmd+ " is online \u2705")

#checks if guild is active and reports back in chat, to be active message needs to start with "#"        
    elif message.content.startswith('#'):
        guildrequest = message.content.split()[0].replace("#", "")
        guildweb = "http://armory.warmane.com/api/guild/{}/Icecrown/summary".format(guildrequest)
        apidata = requests.get(guildweb, headers={'User-Agent': 'Custom'})

        jdata = json.loads(apidata.text)

        results = []

        counter= 0

        await message.channel.send("Checking online players for guild {}".format(guildrequest))

        for i in jdata["roster"]:
            if i["online"]==True:
                await message.channel.send(i["name"] + " is online \u2705")
                counter+=1

        await message.channel.send("There are {} online players from {}".format(counter,guildrequest))
        
        
client.run(TOKEN)
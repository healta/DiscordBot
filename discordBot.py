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
    print("We have loggen in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

#checks if player is active and reports back in chat, to be active message needs to start with "!"
    elif message.content.startswith('!'):
        cmd = message.content.split()[0].replace("!", "")
        link = 'https://armory.warmane.com/api/character/random/Icecrown/summary'
        properlink = link.replace("random", cmd)
        apidata = requests.get(properlink, headers={'User-Agent': 'Custom'})
        disc = (apidata.text)
        jdata = json.loads(disc)

        if jdata.get("online") is False:
            await message.channel.send(cmd + " is offline :(")
        else:
            await message.channel.send(cmd+ " is online :)")
        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]

#checks if guild is active and reports back in chat, to be active message needs to start with "#"        
    elif message.content.startswith('#'):
        guildrequest = message.content.split()[0].replace("#", "")
        guildweb = "http://armory.warmane.com/api/guild/random/Icecrown/summary"
        guildwebproper = guildweb.replace("random", guildrequest)
        apidata = requests.get(guildwebproper, headers={'User-Agent': 'Custom'})
        disc = apidata.text
        jdata = json.loads(disc)

        for elementos in jdata.keys():
            print (elementos)
            for elementos2 in jdata[elementos].keys():
                print(elementos2)

        await message.channel.send(results)

client.run(TOKEN)
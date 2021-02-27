import discord
from discord.ext import commands
from info import TOKEN
import os
import time
import asyncio
import math
import asyncio
from discord import Color
from ro_py import Client
from ro_py.thumbnails import ThumbnailSize, ThumbnailType
import json



intents = discord.Intents.all()
upTime = time.time()
client =  commands.Bot(command_prefix='-', intents=intents)
client.remove_command('help')


roblox = Client("_eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4MjEzMGQ3Zi1jOTVlLTQ5ZTgtYmM1NC0zMjZhZDZmNGNjMjMiLCJzdWIiOjEwMjE1MjQ5NDN9.9jIBpe17md6nplRiqtVqoyc3KeidaxN-_3_ahBkXqrY")

support_channel = ""

SUPPORT_SERVER = 813872488743567422
ticketClose = "🔒"
supportCategory = "TICKETS"

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Diamond's Assistant"))
    print("Bot is online.")


async def handleNewTicket(message):
    channel = message.channel
    ticketAuthor = message.author
    embed = discord.Embed(title="Ticket Received!", color=Color.green())
    embed.add_field(name="Welcome to the Support Center!", value="A member from our support team will be with you as soon as possible, however: \n\n Our staff team may be currently busy, and it can take up to a few hours for a response. \n\n Please note: This support bot is closed on the following holidays: \n\n -Christmas Day \n\n -Easter \n\n -New Years Day \n \n **Important notice: ** \n Customer Satisfaction is important here, if you encounter a bad experience please let a staff member know or fill out our feedback form. \n\n Thank you for contacting support, we will be with you shortly!\n\n Created a ticket on accident or want to close your ticket? React with the reaction below to close your ticket.")
    usermsg = await channel.send(embed=embed)
    await usermsg.add_reaction(ticketClose)
    GET_SUPPORT_SERVER = client.get_guild(SUPPORT_SERVER)
    category = discord.utils.get(GET_SUPPORT_SERVER.categories, name=supportCategory)

    with open("info.json", "r+")as f:
        data = json.load(f)
        data['tickets'] +=1
        numOfTickets = data['tickets']
        ticketsMade = data['tickets']
        global support_channel
        support_channel = await GET_SUPPORT_SERVER.create_text_channel(f'ticket-{ticketsMade}', overwrites=None, category=category, reason=None)
        ticketinfo = {f"ticket-{numOfTickets}":message.author.id, f"ticket-{numOfTickets}-creator":f"{message.author}", f"ticket-{numOfTickets}-INITMSG": f"{message.content}", f"ticket-{numOfTickets}-ID": support_channel.id }
        data.update(ticketinfo)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
        

    support_embed = discord.Embed(title="New ticket!", color=Color.green())
    support_embed.add_field(name="A new ticket has been received.", value=f"Ticket by: {ticketAuthor}" ,inline=False)
    support_embed.add_field(name="Intial message: ", value=f"{message.content}", inline=False)
    support_embed.add_field(name="How to claim: ", value='Type "-claim" to claim this ticket! \n\n **<@&813883789025083422>**',inline=False)
    await support_channel.send(embed=support_embed)
    tempmessage = await support_channel.send("<@&813883789025083422>")
    await tempmessage.delete()



async def entryHandler(message):
    await handleNewTicket(message)
    with open("info.json", "r+") as f:
        data = json.load(f)
        user = {f'{message.author}': True}
        data.update(user)
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
        active = data[f'{message.author}']



@client.event
async def on_message(message: discord.Message):
    newchannel = str(message.channel)
    if message.guild is None and not message.author.bot:
        with open("info.json", "r+") as f:
            data = json.load(f)
            user = {f'{message.author}': False}
            data.update(user)
            f.seek(0)
            json.dump(data,f,indent=4)
            f.truncate()
            active = data[f'{message.author}']
        await entryHandler(message)

            

            


    if message.guild.id == 813872488743567422 and newchannel.startswith('ticket-'):
        if message.content == "-claim":
            return
        elif message.content == "-close":
            return
        else:
            with open("info.json", "r+") as f:
                data = json.load(f)
                ticketNum = str(message.channel)
                currentTicket = data[ticketNum]
                ticketCreator = client.get_user(currentTicket)
                embed = discord.Embed(title=f"{message.author} - Support Team", color=Color.dark_green())
                embed.add_field(name="Message: ",value=f"{message.content}", inline=False)
                await ticketCreator.send(embed=embed)
              



    await client.process_commands(message)

@client.command(pass_context=True)
async def claim(ctx):
    channelname = str(ctx.channel)
    if ctx.guild.id == 813872488743567422 and channelname.startswith('ticket-'):
        embed = discord.Embed(title="Ticket Claimed", color=Color.green())
        embed.add_field(name="This ticket has been claimed!", value=f'{ctx.author} has claimed this ticket!',inline=False)
        embed.add_field(name="PTS is now enabled.", value="PTS is now enabled! Please do not talk in this ticket unless you have permission.",inline=False)
        msg = await ctx.send(embed=embed)
        await msg.pin()
    else:
        return
        


@client.command()
async def close(ctx, time):
    channelname = str(ctx.channel)
    if ctx.guild.id == 813872488743567422 and channelname.startswith('ticket-'):
        embed = discord.Embed(title="Ticket closing...", color=Color.dark_red())
        embed.add_field(name=f"Ticket scheduled to close.", value=f'{ctx.author} has scheduled to close this ticket.', inline=False)
        embed.add_field(name=f"Time till close: ", value=f"This ticket will close in {time} seconds.")
        await ctx.channel.send(embed=embed)
        newtime = int(time)
        await asyncio.sleep(newtime)
        channel = ctx.channel
        await channel.delete()




@client.command()
async def whois(ctx, username):
    user = await roblox.get_user_by_username(username)
    embed = discord.Embed(title=f"Info for {user.name}")
    embed.add_field(
        name="Username",
        value="`" + user.name + "`"
    )
    embed.add_field(
        name="Display Name",
        value="`" + user.display_name + "`"
    )
    embed.add_field(
        name="User ID",
        value="`" + str(user.id) + "`"
    )

    avatar_image = await user.thumbnails.get_avatar_image(
    shot_type=ThumbnailType.avatar_headshot,  # headshot
    size=ThumbnailSize.size_420x420,  # high resolution thumbnail
    is_circular=False  # square thumbnail
    )


    embed.set_thumbnail(
    url=avatar_image
    )



    await ctx.send(embed=embed)




client.run(TOKEN)
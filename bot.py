import discord, time
from discord.ext import commands
from discord_slash import SlashCommand
from datetime import datetime

client = commands.Bot(command_prefix='!', allowed_mentions = discord.AllowedMentions(everyone = True))
GENERAL = 340347114699620362
AFK_CHANNEL = 286379083430887424
TCOV_CHANNEL = 859247446387064849
DREW = 271371937131921410
TCOV = 279334952359821334
print(client.guilds)
guild = client.guilds[0]
DnD_role = discord.utils.get(guild.roles, id=795761634802794596)
START = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="lofi in my underwear"))

# move command
@client.command()
async def move(ctx, member: discord.Member, channel):  
    guild = member.guild
    if channel in ["afk","away"]:
        channel = client.get_channel(AFK_CHANNEL)
    elif channel in ["here","back","general"]:
        channel = client.get_channel(GENERAL)
    elif channel == "tcov":
        channel = client.get_channel(TCOV_CHANNEL)
    else:
        channel = None

    if channel == None:
        await ctx.send('{} is an invalid voice channel'.format(channel))
    else:
        await member.move_to(channel)
    await ctx.message.delete()

# Evaluate all messages
@client.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        await message.channel.send("No talk me angy.")
        await message.channel.send("https://pbs.twimg.com/media/EHBAIUgWkAA1jK2?format=jpg&name=small")
    else:
        await client.process_commands(message)
        
# troll tcov when streaming league
@client.event
async def on_voice_state_update(member, prev, cur):

    # If a user is connected before and after the update
    if prev.channel and cur.channel:  
        if prev.self_stream != cur.self_stream:
            # cur.self_stream will return True whether they're currently streaming
            if cur.self_stream and member.id == TCOV:
                await client.get_channel(GENERAL).send('Come watch Tcov run it down')
    
    # If they are new to the voice chat
    elif not prev.channel and cur.channel:
        # if it is drew
        if member.id == DREW:
            msg = '{} Attention everyone. Drew is here.'.format(DnD_role.mention) 
            await client.get_channel(GENERAL).send(msg)
            # Send join timestamp to DB
            global START
            START = time.time()
            
    # if they are leaving the channel
    elif prev.channel and not cur.channel:
        # if it is drew
        if member.id == DREW:
            msg = '{} Drew left!'.format(DnD_role.mention) 
            await client.get_channel(GENERAL).send(msg)
            # Send leave timestamp to DB
            # Format time for viewable information
            END = time.time()
            elapsed_time = END - START
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            msg = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            await client.get_channel(GENERAL).send("Drew was in discord for " + msg)
        


client.run('ODY0NjU2MTYzNzE1MTUzOTIw.YO4nzQ.eG8b7W2-g5yRIfntyBSOtNwj-uI')
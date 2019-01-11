import os
import os.path
import random
import asyncio
import aiohttp
import discord
import json
import datetime

from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import find

import cdobtserverdata
import cdobtuserdata

############################################################
TOKEN = ""
OWNER_ID = 420838696732983297
############################################################

def BOT_PREFIX(bot, message):
    if not message.guild:
        return cdobtuserdata.get_user_data_by_key(message.author.id, "prefix")
    else:
        return cdobtserverdata.get_server_data_by_key(message.guild.id, "prefix")
        
cdobt = commands.Bot(command_prefix=BOT_PREFIX)
cdobt.remove_command('help')

daysdict = { 
    "mon": {
        "0000": "Kzarka (EU)",
        "0100": "D. Bheg (NA)",
        "0300": "R. Nose (EU)",
        "0415": "Kzarka (NA)",
        "0615": "Mudster (NA)",
        "0700": "Kzarka (EU)",
        "0800": "Kzarka (NA)",
        "1000": "Dim Tree (EU)",
        "1100": "R. Nose (NA)",
        "1400": "R. Nose (EU)",
        "1500": "Kzarka (NA)",
        "1700": "Mudster (EU)",
        "1800": "Dim Tree (NA)",
        "2015": "D. Bheg (EU)",
        "2200": "R. Nose (NA)",
        "2215": "Dim Tree (EU)"
    },
    "tue": {
        "0000": "Mudster (EU)",
        "0100": "Mudster (NA)",
        "0300": "Kzarka (EU)",
        "0415": "D. Bheg (NA)",
        "0615": "Dim Tree (NA)",
        "0700": "Dim Tree (EU)",
        "0800": "Mudster (NA)",
        "1000": "Kzarka (EU)",
        "1100": "Kzarka (NA)",
        "1400": "Mudster (EU)",
        "1500": "Dim Tree (NA)",
        "1700": "R. Nose (EU)",
        "1800": "Kzarka (NA)",
        "2015": "Dim Tree (EU)",
        "2200": "Mudster (NA)",
        "2215": "D. Bheg (EU)"
    },
    "wed": {
        "0000": "R. Nose (EU)",
        "0100": "R. Nose (NA)",
        "0300": "Dim Tree (EU)",
        "0415": "Dim Tree (NA)",
        "0615": "D. Bheg (NA)",
        "0700": "Kzarka (EU)",
        "0800": "R. Nose (NA)",
        "1000": "Mudster (EU)",
        "1100": "Dim Tree (NA)",
        "1400": "Kzarka (EU)",
        "1500": "Kzarka (NA)",
        "1700": "Dim Tree (EU)",
        "1800": "Mudster (NA)",
        "2015": "R. Nose (EU)",
        "2200": "Kzarka (NA)",
        "2215": "Kzarka (EU)"
    },
    "thu": {
        "0000": "Dim Tree (EU)",
        "0100": "Dim Tree (NA)",
        "0300": "R. Nose (EU)",
        "0415": "R. Nose (NA)",
        "0615": "Kzarka (NA)",
        "0700": "Mudster (EU)",
        "0800": "Dim Tree (NA)",
        "1000": "Kzarka (EU)",
        "1100": "R. Nose (NA)",
        "1400": "Dim Tree (EU)",
        "1500": "Mudster (NA)",
        "1700": "Kzarka (EU)",
        "1800": "Kzarka (NA)",
        "2015": "Dim Tree (EU)",
        "2200": "Dim Tree (NA)",
        "2215": "R. Nose (EU)"
    },
    "fri": {
        "0000": "D. Bheg (EU)",
        "0100": "Kzarka (NA)",
        "0300": "Mudster (EU)",
        "0415": "Dim Tree (NA)",
        "0615": "R. Nose (NA)",
        "0700": "R. Nose (EU)",
        "0800": "D. Bheg (NA)",
        "1000": "Dim Tree (EU)",
        "1100": "Mudster (NA)",
        "1400": "Kzarka (EU)",
        "1500": "R. Nose (NA)",
        "1700": "D. Bheg (EU)",
        "1800": "Dim Tree (NA)",
        "2015": "Kzarka (EU)",
        "2200": "Kzarka (NA)",
        "2215": "Dim Tree (EU)"
    },
    "sat": {
        "0000": "Mudster (EU)",
        "0100": "D. Bheg (NA)",
        "0300": "D. Bheg (EU)",
        "0415": "Kzarka (NA)",
        "0615": "Dim Tree (NA)",
        "0700": "Dim Tree (EU)",
        "0800": "Mudster (NA)",
        "1000": "R. Nose (EU)",
        "1100": "D. Bheg (NA)",
        "1400": "D. Bheg (EU)",
        "1500": "Dim Tree (NA)",
        "1700": "Kzarka (EU)",
        "1800": "R. Nose (NA)",
        "2015": "R. Nose (EU)",
        "2200": "D. Bheg (NA)",
        "2215": "Kzarka (EU)"
    },
    "sun": {
        "0000": "R. Nose (EU)",
        "0100": "Kzarka (NA)",
        "0300": "Dim Tree (EU)",
        "0415": "R. Nose (NA)",
        "0615": "Kzarka (NA)",
        "0700": "Kzarka (EU)",
        "0800": "R. Nose (NA)",
        "1000": "Kzarka (EU)",
        "1100": "Dim Tree (NA)",
        "1400": "R. Nose (EU)",
        "1500": "Kzarka (NA)",
        "1700": "D. Bheg (EU)",
        "1800": "Kzarka (NA)",
        "2015": "Kzarka (EU)",
        "2200": "R. Nose (NA)",
        "2215": "Mudster (EU)"
    }
}
def is_owner():
    global OWNER_ID
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)
 
@cdobt.event
async def on_message(message):
    if message.guild is not None:
        if not os.path.isfile("servers/"+str(message.guild.id)+".json"):
            cdobtserverdata.init_server_data(message.guild.id)  
    else:
        if not os.path.isfile("users/"+str(message.author.id)+".json"):
            cdobtuserdata.init_user_data(message.author.id) 
    if cdobt.user.mention in message.content:
        await message.channel.send("Please type " + BOT_PREFIX(cdobt, message) + "help to view the commands.")
    await cdobt.process_commands(message) 
    
@cdobt.command(pass_context = True)
@is_owner()
async def guilds(ctx):
    s = ""
    count = 0
    guilds = cdobt.guilds
    
    embed = discord.Embed(title="guilds", description="", color=0xf44242)
    for guild in guilds:
        count += 1
        s += guild.name+"\n"
        embed.add_field(name=str(count)+"). "+guild.name, value="Owner: "+guild.owner.name+"#"+guild.owner.discriminator)
        embed.add_field(name="guild ID: "+str(guild.id), value="Owner ID: "+str(guild.owner.id), inline=True)
    await ctx.send(embed=embed) 
    
@cdobt.command(pass_context = True)
async def enable(ctx):
    if ctx.guild is not None:
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.message.add_reaction("❌")
            return
    try:
        if ctx.guild is not None:
            cdobtserverdata.update_server_data_channelid(ctx.guild.id, ctx.channel.id)
        else:
            cdobtuserdata.update_user_data_channelid(ctx.message.author.id, ctx.channel.id)
        await ctx.message.add_reaction("✅")
    except Exception: 
        await ctx.message.add_reaction("❌")
        pass
  
@cdobt.command(pass_context = True)
async def disable(ctx):
    if ctx.guild is not None:
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.message.add_reaction("❌")
            return
    try:
        if ctx.guild is not None:
            cdobtserverdata.update_server_data_channelid(ctx.guild.id, 0)
        else:
            cdobtuserdata.update_user_data_channelid(ctx.message.author.id, 0)
        await ctx.message.add_reaction("✅")
    except Exception: 
        await ctx.message.add_reaction("❌")
        pass
        
@cdobt.command(pass_context = True)
async def alert(ctx, alerttime):  
    if ctx.guild is not None:
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.message.add_reaction("❌")
            return
    try: 
        if alerttime.isdigit():
            alerttime = int(alerttime)
            if alerttime >= 5 and alerttime <= 60:
                if ctx.guild is not None:
                    cdobtserverdata.update_server_data_alerttime(ctx.guild.id, alerttime)
                else:
                    cdobtuserdata.update_user_data_alerttime(ctx.message.author.id, alerttime)
                await ctx.message.add_reaction("✅")
    except Exception: 
        await ctx.message.add_reaction("❌")
        pass

@cdobt.command(pass_context = True)
async def prefix(ctx, prefix):  
    if ctx.guild is not None:
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.message.add_reaction("❌")
            return
    try: 
        if not prefix.isspace():
                if ctx.guild is not None:
                    cdobtserverdata.update_server_data_prefix(ctx.guild.id, prefix)
                else:
                    cdobtuserdata.update_user_data_prefix(ctx.message.author.id, prefix)
                await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("❌")
    except Exception: 
        await ctx.message.add_reaction("❌")
        pass

        
@cdobt.command(pass_context = True)
async def changelog(ctx):  
    embed = discord.Embed(title="Changelog:", description="09/01/2019 (assuming I updated this date the last time I made changes)", color=0x89a4d4)
    embed.add_field(name="Fixed:", value="Incorrect boss was shown as upcoming before 00:00 UTC (it was showing the first boss of the previous day instead of the next day.. woops).", inline=False)
    embed.add_field(name="Added:", value="DM alerts! The bot now works in direct messages in the same way it works in guilds.", inline=False)
    embed.add_field(name="Added:", value="Custom prefixes! Change it to whatever works for you, the initial prefix is still 'bt!'", inline=False)
    embed.add_field(name="Added:", value="A changelog. :D", inline=False)
#    embed.add_field(name="Improved:", value="Remade the system for saving and loading individual server settings. (shut up syzygy)", inline=False)
    await ctx.send(embed=embed) 
    await ctx.message.add_reaction("✅")      
 
@cdobt.command(pass_context=True)
async def help(ctx):
    prefix = BOT_PREFIX(cdobt, ctx.message)
    embed = discord.Embed(title="Prefix: "+prefix, description="", color=0x89a4d4)
    embed.add_field(name=prefix+"prefix <prefix>", value="Changes the command prefix.", inline=False)
    embed.add_field(name=prefix+"next", value="Shows the next boss spawn and how much time is remaining.", inline=False)
    embed.add_field(name=prefix+"enable", value="Enables boss spawn alerts. Enter this command in the channel where you want alerts to be posted, alerts can only be active in one channel at a time. By default one message will be posted 15 minutes before the spawn and one when the boss spawns.", inline=False)
    embed.add_field(name=prefix+"disable", value="Disables boss spawn alerts.", inline=False)
    embed.add_field(name=prefix+"alert <time in minutes>", value="The bot will post a pre-spawn alert this many minutes before the boss spawns. (between 5 and 60 minutes, default is 15)", inline=False)
    embed.add_field(name=prefix+"changelog", value="Shows the last changelog.", inline=False)
    await ctx.send(embed=embed)  
    await ctx.message.add_reaction("✅")
    
@cdobt.command(pass_context = True)
async def next(ctx):
        bossandremaining = await date_time_check()
        color = 0x89a4d4
        if bossandremaining["boss"].startswith("Kzarka"):
            color = 0xf44242
        elif bossandremaining["boss"].startswith("D. Bheg"): 
            color = 0xbd43f2
        elif bossandremaining["boss"].startswith("Mudster"):
            color = 0x40f7f4
        elif bossandremaining["boss"].startswith("Dim Tree"):
            color = 0x2de527
        elif bossandremaining["boss"].startswith("R. Nose"):
            color = 0xff9d0a
        try:
            embed = discord.Embed(title=bossandremaining["boss"], description="upcoming in "+str(bossandremaining["remaining"])+" minutes...", color=color)
            await ctx.send(embed=embed) 
            await ctx.message.add_reaction("✅")
        except Exception: 
            await ctx.message.add_reaction("❌")
            pass
                
async def send_server_alerts(remaining, message):
    if remaining == None:
        return
    else:
        file_list=os.listdir("servers/")
        for file in file_list:
            sep = '.'
            filename = file.split(sep, 1)[0]
            data = cdobtserverdata.get_server_data(filename)
            if data["channelid"]:
                channel = cdobt.get_channel(data["channelid"])
                
                color = 0x89a4d4         
                if message.startswith("Kzarka"):
                    color = 0xf44242
                elif message.startswith("D. Bheg"): 
                    color = 0xbd43f2
                elif message.startswith("Mudster"):
                    color = 0x40f7f4
                elif message.startswith("Dim Tree"):
                    color = 0x2de527
                elif message.startswith("R. Nose"):
                    color = 0xff9d0a
                try:
                    if remaining == 0:
                        embed = discord.Embed(title=message, description="has spawned!", color=color)
                        await channel.send(embed=embed)   
                    elif remaining == data["alerttime"]:
                        embed = discord.Embed(title=message, description="upcoming in "+str(remaining)+" minutes...", color=color)
                        await channel.send(embed=embed)                      
                except Exception: 
                    pass

async def send_user_alerts(remaining, message):
    if remaining == None:
        return
    else:
        file_list=os.listdir("users/")
        for file in file_list:
            sep = '.'
            filename = file.split(sep, 1)[0]
            data = cdobtuserdata.get_user_data(filename)
            if data["channelid"]:
                channel = cdobt.get_channel(data["channelid"])
                
                color = 0x89a4d4         
                if message.startswith("Kzarka"):
                    color = 0xf44242
                elif message.startswith("D. Bheg"): 
                    color = 0xbd43f2
                elif message.startswith("Mudster"):
                    color = 0x40f7f4
                elif message.startswith("Dim Tree"):
                    color = 0x2de527
                elif message.startswith("R. Nose"):
                    color = 0xff9d0a
                try:
                    if remaining == 0:
                        embed = discord.Embed(title=message, description="has spawned!", color=color)
                        await channel.send(embed=embed)   
                    elif remaining == data["alerttime"]:
                        embed = discord.Embed(title=message, description="upcoming in "+str(remaining)+" minutes...", color=color)
                        await channel.send(embed=embed)                      
                except Exception: 
                    pass
              
async def date_time_check():
    global daysdict 
    
    days = [ "mon", "tue", "wed", "thu", "fri", "sat", "sun" ] #this is a super lazy way to do this
    times = [ "0000", "0100", "0300", "0415", "0615", "0700", "0800", "1000", "1100", "1400", "1500", "1700", "1800", "2015", "2200", "2215" ]  
    timessimple = [ 0, 100, 300, 415, 615, 700, 800, 1000, 1100, 1400, 1500, 1700, 1800, 2015, 2200, 2215 ]  #because python doesn't just ignore leading zeros... there's better looking ways to do this but, again, I'm pretty lazy
    
    currentday = datetime.datetime.utcnow().strftime("%a").lower()
    currentdatetime = datetime.datetime.utcnow() 
    curhourminute = currentdatetime.strftime("%H%M")   
    
    curtimesimple = 0    
    
    if str(curhourminute).startswith("000"):
        curtimesimple = abs(int(curhourminute)) % 10
    elif str(curhourminute).startswith("00"):
        curtimesimple = abs(int(curhourminute)) % 100
    elif str(curhourminute).startswith("0"):
        curtimesimple = abs(int(curhourminute)) % 1000
    else:
        curtimesimple = int(curhourminute)  
        
    closesttime = min(timessimple, key=lambda x:abs(x-int(curhourminute))) 

    for day in daysdict:
        if currentday == day:
            closestindex = timessimple.index(closesttime)
            nextbosstime = ""
            nextbossday = ""
     
            if curtimesimple > closesttime:
                if closestindex == len(times)-1:
                    nextbosstime = times[0]
                    nextbossday = days[days.index(day)+1]
                else:
                    nextbosstime = times[timessimple.index(closesttime)+1]
                    nextbossday = days[days.index(day)]
            else:
                nextbosstime = times[timessimple.index(closesttime)]
                nextbossday = day
                
            timeleftdelta = datetime.datetime.strptime(nextbosstime, "%H%M") - datetime.datetime.strptime(str(curhourminute), "%H%M")
            hours = int(strf_delta(timeleftdelta, "{hours}"))
            minutes = int(strf_delta(timeleftdelta, "{minutes}"))
            
            if hours > 0:
                for x in range(hours):
                    minutes += 60    
                    
            return {"boss":get_nested(daysdict, nextbossday, nextbosstime), "remaining":minutes}
                    
def get_nested(data, *args): #https://stackoverflow.com/a/48005385    
    if args and data:
        element  = args[0]
        if element:
            value = data.get(element)
            return value if len(args) == 1 else get_nested(value, *args[1:])
            
def strf_delta(tdelta, fmt): #https://stackoverflow.com/a/8907269
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
  
async def background_subroutine():
    await cdobt.wait_until_ready()
#    cdobtserverdata.fix_old_server_data()
    lastremaining = 0
    while not cdobt.is_closed():
        bossandremaining = await date_time_check()
        await cdobt.change_presence(status=discord.Status.online, activity=discord.Game(name=bossandremaining["boss"]+" in "+str(bossandremaining["remaining"])+" minutes..."))
        if bossandremaining["remaining"] != lastremaining:
            await send_server_alerts(bossandremaining["remaining"], bossandremaining["boss"])
            await send_user_alerts(bossandremaining["remaining"], bossandremaining["boss"])
            lastremaining = bossandremaining["remaining"]
        await asyncio.sleep(60)
    
@cdobt.event
async def on_ready():
    await cdobt.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Booting..."))
    cdobt.loop.create_task(background_subroutine()) 
    print("CDO Boss Timer Bot by Merry#9999 :3")
    print("Logging in as "+cdobt.user.name+"...")
cdobt.run(TOKEN)

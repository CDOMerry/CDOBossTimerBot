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


############################################################
BOT_PREFIX = "bt!"
TOKEN = "NTI3OTMzMjE5MDc3ODgxODg0.DwbDEg.Qa4Vm6ETiexqFkN9rvb_Qk93sXc"
OWNER_ID = 420838696732983297
############################################################


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
    global OWNER_ID
    if message.guild is None:
        if message.author != cdobt.user and message.author.id != OWNER_ID:
            print("Message received from: " + message.author.name + ": " + message.content)
            await cdobt.get_user(OWNER_ID).send(message.author.name + ": "+ message.content)  
    else:
        if not os.path.isfile("servers/"+str(message.guild.id)+".json"):
            cdobtserverdata.init_server_data(message.guild.id)            
    await cdobt.process_commands(message) 

@cdobt.command(pass_context = True)
@is_owner()
async def dm(ctx, member : discord.Member = None, *, message):
    if not member:
        return
    try:
        await member.send(message)
        print("Message sent to: " + member.name + ": " + message)
        await ctx.message.add_reaction("✅")
    except Exception: 
        await ctx.message.add_reaction("❌")
        pass
    
@cdobt.command(pass_context = True)
async def enable(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.message.add_reaction("❌")
        return
    try:
        cdobtserverdata.update_server_data_channelid(ctx.guild.id, ctx.channel.id)
        await ctx.message.add_reaction("✅")
    except Exception: 
        await ctx.message.add_reaction("❌")
        pass
  
@cdobt.command(pass_context = True)
async def disable(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.message.add_reaction("❌")
        return
    try:
        cdobtserverdata.update_server_data_channelid(ctx.guild.id, 0)
        await ctx.message.add_reaction("✅")
    except Exception: 
        await ctx.message.add_reaction("❌")
        pass
        
@cdobt.command(pass_context = True)
async def alert(ctx, alerttime):  
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.message.add_reaction("❌")
        return
    try: 
        if alerttime.isdigit():
            alerttime = int(alerttime)
            if alerttime >= 5 and alerttime <= 60:
                cdobtserverdata.update_server_data_alerttime(ctx.guild.id, alerttime)
                await ctx.message.add_reaction("✅")
    except Exception: 
        await ctx.message.add_reaction("❌")
        pass
        
#@cdobt.command(pass_context = True) #this is really annoying and doesn't really server a purpose, might be better if we were to make a role for each boss and ping the role depending on which boss spawned? idk, either way I'll add dm alerts soon and there will be literally no point to mentioning roles.
#async def mention(ctx, rolename):      
#    if not ctx.message.author.guild_permissions.administrator:
#        await ctx.message.add_reaction("❌")
#        return
#    try:
#        data = cdobtserverdata.get_server_data(ctx.guild.id) 
#        for role in ctx.guild.roles:
#            if role.name == rolename:
#                cdobtserverdata.update_server_data_isenabled(ctx.guild.id, role.id) 
#        await ctx.message.add_reaction("✅")
#    except Exception: 
#        await ctx.message.add_reaction("❌")
#        pass            
    
@cdobt.command(pass_context=True)
async def help(ctx):
    global BOT_PREFIX
    embed = discord.Embed(title="Prefix: "+BOT_PREFIX, description="", color=0x89a4d4)
    embed.add_field(name=BOT_PREFIX+"next", value="Displays the next boss spawn and how much time is remaining.", inline=False)
    embed.add_field(name=BOT_PREFIX+"enable", value="Enables boss spawn alerts. Enter this command in the channel where you want alerts to be posted, alerts can only be active in one channel at a time. By default one message will be posted 15 minutes before the spawn and one when the boss spawns.", inline=False)
    embed.add_field(name=BOT_PREFIX+"disable", value="Disables boss spawn alerts.", inline=False)
    embed.add_field(name=BOT_PREFIX+"alert <time in minutes>", value="The bot will post a pre-spawn alert this many minutes before the boss spawns. (between 5 and 60 minutes, default is 15)", inline=False)
#    embed.add_field(name=BOT_PREFIX+"mention <role name>", value="Enables role pings when the pre-spawn alert is posted.", inline=False)
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
                
async def send_alerts(remaining, message):
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
                        if data["isenabled"]:
                            role = channel.guild.get_role(data["isenabled"])
                            if role is not None:
                                await channel.send(role.mention)                          
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
                    nextbossday = days[days.index(day)-1]
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
    lastremaining = 0
    while not cdobt.is_closed():
        bossandremaining = await date_time_check()
        await cdobt.change_presence(status=discord.Status.online, activity=discord.Game(name=bossandremaining["boss"]+" in "+str(bossandremaining["remaining"])+" minutes..."))
        if bossandremaining["remaining"] != lastremaining:
            if bossandremaining["remaining"] == 0:
                await send_alerts(0, bossandremaining["boss"])
            else:
                await send_alerts(bossandremaining["remaining"], bossandremaining["boss"])
            lastremaining = bossandremaining["remaining"]
        await asyncio.sleep(60)
    
@cdobt.event
async def on_ready():
    await cdobt.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Booting..."))
    cdobt.loop.create_task(background_subroutine()) 
    print("CDO Boss Timer Bot by Merry#9999 :3")
    print("Logging in as "+cdobt.user.name+"...")

cdobt.run(TOKEN)
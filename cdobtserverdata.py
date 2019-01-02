import os
import os.path
import random
import asyncio
import aiohttp
import discord
import json

from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import find

def get_server_data_by_key(serverid, key):
    if key == "isenabled" or key == "channelid" or key == "alerttime":
        with open("servers/"+str(serverid)+".json", "r", encoding="utf-8") as jsonf:
            data = json.load(jsonf)
        return data.get(key)
        jsonf.close() 
    else:
        return None
        
def get_server_data(serverid):
    isenabled = get_server_data_by_key(serverid, "isenabled")
    channelid = get_server_data_by_key(serverid, "channelid")
    alerttime = get_server_data_by_key(serverid, "alerttime")
    return {"isenabled":isenabled, "channelid":channelid, "alerttime":alerttime}
    
def update_server_data(serverid, isenabled = 0, channelid = 0, alerttime = 15):
    data = {
        "isenabled": isenabled,
        "channelid": channelid,
        "alerttime": alerttime
    }
    with open("servers/"+str(serverid)+".json", "w", encoding="utf-8") as jsonf:
        json.dump(data, jsonf, sort_keys = True, indent = 2, ensure_ascii = False)
    jsonf.close() 

def update_server_data_isenabled(serverid, isenabled):
    data = get_server_data(serverid)
    update_server_data(serverid, isenabled, data["channelid"], data["alerttime"])
    
def update_server_data_channelid(serverid, channelid):
    data = get_server_data(serverid)
    update_server_data(serverid, data["isenabled"], channelid, data["alerttime"])
    
def update_server_data_alerttime(serverid, alerttime):
    data = get_server_data(serverid)
    update_server_data(serverid, data["isenabled"], data["channelid"], alerttime)
    
    
def init_server_data(serverid):
    data = {
        "isenabled": 0,
        "channelid": 0,
        "alerttime": 15
    }
    with open("servers/"+str(serverid)+".json", "w+", encoding="utf-8") as jsonf:
        json.dump(data, jsonf, sort_keys = True, indent = 2, ensure_ascii = False)
    jsonf.close() 
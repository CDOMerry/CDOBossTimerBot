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
    if key == "prefix" or key == "channelid" or key == "alerttime":
        with open("servers/"+str(serverid)+".json", "r", encoding="utf-8") as jsonf:
            data = json.load(jsonf)
        return data.get(key)
        jsonf.close() 
    else:
        return None
        
def get_server_data(serverid):
    prefix = get_server_data_by_key(serverid, "prefix")
    channelid = get_server_data_by_key(serverid, "channelid")
    alerttime = get_server_data_by_key(serverid, "alerttime")
    return {"prefix":prefix, "channelid":channelid, "alerttime":alerttime}
    
def update_server_data(serverid, prefix = "bt!", channelid = 0, alerttime = 15):
    data = {
        "prefix": prefix,
        "channelid": channelid,
        "alerttime": alerttime
    }
    with open("servers/"+str(serverid)+".json", "w", encoding="utf-8") as jsonf:
        json.dump(data, jsonf, sort_keys = True, indent = 2, ensure_ascii = False)
    jsonf.close() 

def fix_old_server_data():
    file_list=os.listdir("servers/")
    for file in file_list:
        with open("servers/"+file, "r", encoding="utf-8") as jsonf:
            data = json.load(jsonf)
            jsonf.close() 
            newdata = {
                "prefix": "bt!",
                "channelid": data.get("channelid"),
                "alerttime": data.get("alerttime")
            }
            with open("servers/"+file, "w+", encoding="utf-8") as jsonf:
                json.dump(newdata, jsonf, sort_keys = True, indent = 2, ensure_ascii = False)
            jsonf.close() 
    
def update_server_data_prefix(serverid, prefix):
    data = get_server_data(serverid)
    update_server_data(serverid, prefix, data["channelid"], data["alerttime"])
    
def update_server_data_channelid(serverid, channelid):
    data = get_server_data(serverid)
    update_server_data(serverid, data["prefix"], channelid, data["alerttime"])
    
def update_server_data_alerttime(serverid, alerttime):
    data = get_server_data(serverid)
    update_server_data(serverid, data["prefix"], data["channelid"], alerttime)
    
def init_server_data(serverid):
    data = {
        "prefix": "bt!",
        "channelid": 0,
        "alerttime": 15
    }
    with open("servers/"+str(serverid)+".json", "w+", encoding="utf-8") as jsonf:
        json.dump(data, jsonf, sort_keys = True, indent = 2, ensure_ascii = False)
    jsonf.close() 

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

def get_user_data_by_key(userid, key):
    if key == "prefix" or key == "channelid" or key == "alerttime":
        with open("users/"+str(userid)+".json", "r", encoding="utf-8") as jsonf:
            data = json.load(jsonf)
        return data.get(key)
        jsonf.close() 
    else:
        return None
        
def get_user_data(userid):
    prefix = get_user_data_by_key(userid, "prefix")
    channelid = get_user_data_by_key(userid, "channelid")
    alerttime = get_user_data_by_key(userid, "alerttime")
    return {"prefix":prefix, "channelid":channelid, "alerttime":alerttime}
    
def update_user_data(userid, prefix = "bt!", channelid = 0, alerttime = 15):
    data = {
        "prefix": prefix,
        "channelid": channelid,
        "alerttime": alerttime
    }
    with open("users/"+str(userid)+".json", "w", encoding="utf-8") as jsonf:
        json.dump(data, jsonf, sort_keys = True, indent = 2, ensure_ascii = False)
    jsonf.close() 

def update_user_data_prefix(userid, prefix):
    data = get_user_data(userid)
    update_user_data(userid, prefix, data["channelid"], data["alerttime"])
    
def update_user_data_channelid(userid, channelid):
    data = get_user_data(userid)
    update_user_data(userid, data["prefix"], channelid, data["alerttime"])
    
def update_user_data_alerttime(userid, alerttime):
    data = get_user_data(userid)
    update_user_data(userid, data["prefix"], data["channelid"], alerttime)
    
    
def init_user_data(userid):
    data = {
        "prefix": "bt!",
        "channelid": 0,
        "alerttime": 15
    }
    with open("users/"+str(userid)+".json", "w+", encoding="utf-8") as jsonf:
        json.dump(data, jsonf, sort_keys = True, indent = 2, ensure_ascii = False)
    jsonf.close() 
